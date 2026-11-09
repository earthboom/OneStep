"""Resolve authorized source bindings or describe location-free source provenance."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

sys.dont_write_bytecode = True
import yaml


class SourceError(ValueError):
    pass


def unique_mapping(pairs):
    result = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise SourceError("Mapping keys must be unique strings.")
        result[key] = value
    return result


def validate_roots(roots):
    if not isinstance(roots, dict):
        raise SourceError("Local settings must map project IDs to absolute roots.")
    for name, value in roots.items():
        if (not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", name)
                or not isinstance(value, str) or not Path(value).is_absolute()):
            raise SourceError("Source roots require project IDs and absolute paths.")
    return roots


def parse_roots(values):
    roots = {}
    for value in values:
        name, sep, path = value.partition("=")
        if not sep or name in roots:
            raise SourceError("Use each --root project=absolute-path once; duplicate roots are invalid.")
        roots[name] = path
    return validate_roots(roots)


class SourceLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader, node):
    loader.flatten_mapping(node)
    return unique_mapping(loader.construct_pairs(node))


SourceLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)


class SourceRegistry:
    def __init__(self, project):
        self.project = Path(project).resolve()
        self.path = self.project / "knowledge/sources.md"
        self.local = self.path.with_name("sources.local.json")
        try:
            text = self.read_internal(self.path)
            match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
            if not match:
                raise SourceError("Source registry requires a YAML header.")
            data = yaml.load(match[1], Loader=SourceLoader)
            if not isinstance(data, dict) or set(data) != {"sources"} or not isinstance(data["sources"], dict):
                raise SourceError("Registry header must contain a sources mapping.")
            self.sources = data["sources"]
            folded = set()
            for ident, item in self.sources.items():
                if not re.fullmatch(r"SRC-[A-Z0-9]+(?:-[A-Z0-9]+)*", ident) or ident.casefold() in folded:
                    raise SourceError("Source IDs must be unique SRC- identifiers.")
                folded.add(ident.casefold())
                if not isinstance(item, dict) or set(item) != {"project", "path", "sha256"}:
                    raise SourceError(f"{ident}: expected project, path and sha256.")
                relative = item["path"]
                unbound = item["project"] is None and relative is None
                if not unbound:
                    if not isinstance(item["project"], str) or not re.fullmatch(r"[a-z][a-z0-9-]*", item["project"]):
                        raise SourceError(f"{ident}: invalid project ID; an unbound source requires both project and path null.")
                    if (not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative
                            or PurePosixPath(relative).is_absolute() or any(p in ("", ".", "..") for p in relative.split("/"))
                            or relative.lower().endswith(".kr.md")):
                        raise SourceError(f"{ident}: use a relative canonical path without traversal.")
                digest = item["sha256"]
                if digest is not None and (not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest)):
                    raise SourceError(f"{ident}: sha256 must be a lowercase digest or null.")
                if not re.search(r"^## " + re.escape(ident) + r"\s*$", text[match.end():], re.M):
                    raise SourceError(f"{ident}: missing source heading.")
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise SourceError(f"Cannot read source registry: {exc}") from exc

    def read_internal(self, path):
        if path.is_symlink() or not path.resolve().is_relative_to(self.project):
            raise SourceError("Registry and local settings must stay inside the working project.")
        return path.read_text(encoding="utf-8-sig")

    def require(self, ident):
        matches = [key for key in self.sources if key.casefold() == ident.casefold()]
        if len(matches) != 1:
            raise SourceError(f"Unregistered source ID: {ident}")
        key = matches[0]
        return key, self.sources[key]

    def describe(self, ident):
        key, item = self.require(ident)
        status = "unbound" if item["project"] is None else "not_checked"
        return {"ok": False, "source_id": key, "project": item["project"], "relative_path": item["path"],
                "expected_sha256": item["sha256"], "status": status,
                "access_status": status, "identity_status": "not_checked"}

    def resolve(self, ident, roots=None):
        result = self.describe(ident)
        item = self.sources[result["source_id"]]
        if item["project"] is None:
            return result
        overrides = validate_roots(roots or {})
        try:
            if item["project"] in overrides:
                root = Path(overrides[item["project"]]).resolve()
                result["root_source"] = "argument"
            else:
                if self.local.is_symlink():
                    raise SourceError("Local settings cannot be a symbolic link.")
                if not self.local.exists():
                    return {**result, "status": "unconfigured", "access_status": "unconfigured"}
                configured = validate_roots(json.loads(self.read_internal(self.local), object_pairs_hook=unique_mapping))
                if item["project"] not in configured:
                    return {**result, "status": "unconfigured", "access_status": "unconfigured"}
                root = Path(configured[item["project"]]).resolve()
                result["root_source"] = "local_settings"
            target = (root / item["path"]).resolve()
            if not target.is_relative_to(root) or target.name.lower().endswith(".kr.md"):
                raise SourceError("Resolved source escapes its configured root or refers to a translation.")
            result["path"] = str(target)
            digest = hashlib.sha256()
            with target.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            result["observed_sha256"] = digest.hexdigest()
            status = "unversioned" if item["sha256"] is None else (
                "matched" if digest.hexdigest() == item["sha256"] else "mismatch")
            return {**result, "status": status, "access_status": "available", "identity_status": status,
                    "ok": status == "matched"}
        except FileNotFoundError:
            return {**result, "status": "missing", "access_status": "missing"}
        except (json.JSONDecodeError, UnicodeError) as exc:
            raise SourceError(f"Invalid local settings: {exc}") from exc
        except OSError as exc:
            return {**result, "status": "unavailable", "access_status": "unavailable", "message": str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("resolve",))
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--id", action="append", required=True)
    parser.add_argument("--root", action="append", default=[], help="Authorized project=absolute-path for this call only")
    args = parser.parse_args()
    try:
        if len({ident.casefold() for ident in args.id}) != len(args.id):
            raise SourceError("Duplicate source IDs are invalid; each ID must be requested once.")
        roots = parse_roots(args.root)
        registry = SourceRegistry(args.project)
        results = []
        for ident in args.id:
            try:
                results.append(registry.resolve(ident, roots))
            except SourceError as exc:
                results.append({"ok": False, "source_id": ident, "status": "invalid", "message": str(exc),
                                "access_status": "not_checked", "identity_status": "not_checked"})
        code = 2 if any(r["status"] == "invalid" for r in results) else (0 if all(r["ok"] for r in results) else 1)
        result = results[0] if len(results) == 1 else {
            "ok": code == 0, "requested_ids": args.id, "completed": len(results), "results": results}
    except SourceError as exc:
        result, code = {"ok": False, "status": "invalid", "message": str(exc)}, 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
