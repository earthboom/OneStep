"""Resolve one registered source through an explicitly configured local root."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

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
                if not isinstance(item["project"], str) or not re.fullmatch(r"[a-z][a-z0-9-]*", item["project"]):
                    raise SourceError(f"{ident}: invalid project ID.")
                relative = item["path"]
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

    def resolve(self, ident):
        key, item = self.require(ident)
        result = {"ok": False, "source_id": key, "project": item["project"],
                  "relative_path": item["path"], "expected_sha256": item["sha256"]}
        try:
            if self.local.is_symlink():
                raise SourceError("Local settings cannot be a symbolic link.")
            if not self.local.exists():
                return {**result, "status": "unconfigured"}
            roots = json.loads(self.read_internal(self.local), object_pairs_hook=unique_mapping)
            if not isinstance(roots, dict):
                raise SourceError("Local settings must map project IDs to absolute roots.")
            for name, value in roots.items():
                if not re.fullmatch(r"[a-z][a-z0-9-]*", name) or not isinstance(value, str) or not Path(value).is_absolute():
                    raise SourceError("Local settings require project IDs and absolute roots.")
            if item["project"] not in roots:
                return {**result, "status": "unconfigured"}
            root = Path(roots[item["project"]]).resolve()
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
            return {**result, "status": status, "ok": status == "matched"}
        except FileNotFoundError:
            return {**result, "status": "missing"}
        except (json.JSONDecodeError, UnicodeError) as exc:
            raise SourceError(f"Invalid local settings: {exc}") from exc
        except OSError as exc:
            return {**result, "status": "unavailable", "message": str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("resolve",))
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    try:
        result = SourceRegistry(args.project).resolve(args.id)
        code = 0 if result["ok"] else 1
    except SourceError as exc:
        result, code = {"ok": False, "status": "invalid", "message": str(exc)}, 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
