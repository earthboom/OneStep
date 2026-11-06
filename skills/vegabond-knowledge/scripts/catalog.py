"""Build and check project-local English catalogs without reading translations."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import quote, unquote

try:
    import yaml
except ImportError:
    yaml = None


if yaml is not None:
    class MetadataLoader(yaml.SafeLoader):
        pass

    def unique_mapping(loader, node, deep=False):
        loader.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            try:
                duplicate = key in result
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(None, None, "Invalid metadata key", key_node.start_mark) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(None, None, f"Duplicate metadata key: {key}", key_node.start_mark)
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    MetadataLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


START = "<!-- onestep-catalog:start -->"
END = "<!-- onestep-catalog:end -->"
HEADER = "| ID / title / kind | Summary | Scope / context | Keywords | Status / checked | Detail |"
RECORD_HEADER = "| ID / title / kind | Summary / trigger / symptom | Scope / context | Keywords | Status / checked / cause / prevention | Detail |"
SEPARATOR = "| --- | --- | --- | --- | --- | --- |"
FIELDS = ("id", "title", "summary", "kind", "scope", "keywords", "status", "checked_at")
RECORD_FIELDS = ("trigger", "symptom", "cause_status", "prevention", "prevention_status")
CAUSE_STATES = {"unknown", "suspected", "confirmed"}
PREVENTION_STATES = {"none", "proposed", "verified", "invalidated"}
STATES = {"knowledge": {"active", "enforced", "superseded"},
          "records": {"open", "resolved", "superseded"}}
KINDS = {"knowledge": {"reference", "method", "convention", "lesson"},
         "records": {"error", "suggestion", "hypothesis"}}
SECTIONS = {
    "knowledge": ("Guidance", "Applicability and exceptions", "Checks", "Evidence"),
    "records": ("Expected and observed", "Cause and resolution", "Recheck and prevention", "Evidence"),
}
LINK = re.compile(r"\[[^\]\n]*\]\((<[^>\n]+>|[^)\n]+)\)")


def human_file(path):
    return path.name.lower().endswith(".kr.md")


def cell(value):
    return " ".join(str(value).split()).replace("|", r"\|")


def visible_markdown(text):
    lines = []
    fence = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if fence == marker:
                fence = None
            elif fence is None:
                fence = marker
        elif fence is None:
            lines.append(line)
    return re.sub(r"(`+).*?\1", "", "\n".join(lines), flags=re.S)


def headings(body):
    result = {}
    current = None
    fence = None
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if fence == marker:
                fence = None
            elif fence is None:
                fence = marker
            if current:
                result[current].append(line)
            continue
        match = re.match(r"^##\s+(.+?)\s*#*\s*$", line) if fence is None else None
        if match:
            current = match.group(1).casefold()
            result.setdefault(current, [])
        elif current:
            result[current].append(line)
    return result


class Catalogs:
    def __init__(self, project, command, strict=False):
        self.project = project.resolve()
        self.command = command
        self.strict = strict
        self.messages = []
        self.entries = {}
        self.ids = {}
        self.plans = {}
        self.references = []
        self.written = []
        self.domains = []
        self.source_registry = None

    def relative(self, path):
        return path.relative_to(self.project).as_posix()

    def issue(self, code, path, message, level="error"):
        self.messages.append({"level": level, "code": code,
                              "path": self.relative(path), "message": message})

    def safe(self, path):
        if human_file(path):
            self.issue("translation_input", path, "Translations are not canonical inputs.")
            return False
        if not path.resolve().is_relative_to(self.project) or path.is_symlink():
            self.issue("outside_project", path, "Canonical input/output must remain inside the project without symlinks.")
            return False
        return True

    def read(self, path):
        if not self.safe(path):
            return None
        try:
            return path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            self.issue("read_failed", path, str(exc))
            return None

    def translation(self, path):
        if not path.with_name(path.stem + ".kr.md").is_file():
            self.issue("missing_translation", path, "Generate the human translation from English; do not open it.",
                       "warning" if self.command == "build" else "error")

    def local_target(self, source, href):
        href = href.strip()
        if href.startswith("<"):
            href = href[1:href.find(">")]
        else:
            href = re.split(r"\s+[\"']", href, maxsplit=1)[0]
        if href.startswith("#"):
            return None
        drive = bool(re.match(r"^[A-Za-z]:[/\\]", href))
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", href) and not drive:
            return None
        target_text = unquote(href.split("#", 1)[0].split("?", 1)[0])
        if not target_text:
            return None
        target = Path(target_text)
        target = target if target.is_absolute() else source.parent / target
        if human_file(target):
            self.issue("translation_reference", source, "Canonical references must not use a human translation.")
            return None
        resolved = target.resolve()
        if not resolved.is_relative_to(self.project):
            self.issue("external_local_reference", source, "External local reference requires separate verification.", "warning")
            return None
        if resolved == self.project / "knowledge/sources.md" and "#" in href:
            from sources import SourceError, SourceRegistry
            try:
                if self.source_registry is None:
                    self.source_registry = SourceRegistry(self.project)
                    self.translation(self.source_registry.path)
                ident, _ = self.source_registry.require(unquote(href.split("#", 1)[1]))
                self.issue("source_unverified", source,
                           f"{ident}: registration checked; resolve separately to check source access and identity.", "warning")
            except SourceError as exc:
                self.issue("source_reference", source, str(exc))
        return target

    def links(self, path, text):
        for href in LINK.findall(visible_markdown(text)):
            target = self.local_target(path, href)
            if target is not None:
                self.references.append((path, target))

    def entry(self, path, store):
        key = path.resolve()
        if key in self.entries:
            return self.entries[key]
        text = self.read(path)
        if text is None:
            return None
        self.translation(path)
        entry = {"path": path, "store": store, "meta": None, "legacy": False}
        self.entries[key] = entry
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            self.links(path, text)
            entry["legacy"] = True
            self.issue("legacy_entry", path, "Metadata is unknown; preserve prior catalog information and inspect before use.",
                       "error" if self.strict else "warning")
            return entry
        closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if closing is None:
            self.issue("invalid_header", path, "YAML header has no closing delimiter.")
            return entry
        body = "\n".join(lines[closing + 1:])
        self.links(path, body)
        try:
            meta = yaml.load("\n".join(lines[1:closing]), Loader=MetadataLoader)
        except yaml.YAMLError as exc:
            self.issue("invalid_header", path, str(exc))
            return entry
        if not isinstance(meta, dict):
            self.issue("invalid_header", path, "YAML header must be a mapping.")
            return entry
        missing = [field for field in FIELDS if field not in meta]
        if missing:
            self.issue("missing_fields", path, ", ".join(missing))
            return entry
        invalid = []
        for field in ("id", "title", "summary", "kind", "scope", "status"):
            if not isinstance(meta[field], str) or not meta[field].strip():
                invalid.append(field)
        if invalid:
            self.issue("invalid_fields", path, ", ".join(invalid))
            return entry
        validation_start = len(self.messages)
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", meta["id"]):
            self.issue("invalid_id", path, "Use a stable ID containing letters, digits, dots, underscores or hyphens.")
        if meta["status"] not in STATES[store]:
            self.issue("invalid_status", path, f"Expected one of {sorted(STATES[store])}.")
        if meta["kind"] not in KINDS[store]:
            self.issue("invalid_kind", path, f"Expected one of {sorted(KINDS[store])}.")
        keywords = meta["keywords"]
        if not isinstance(keywords, list) or not keywords or any(not isinstance(x, str) or not x.strip() for x in keywords):
            self.issue("invalid_keywords", path, "keywords must be a nonempty list of strings.")
        checked = meta["checked_at"]
        if checked is not None:
            try:
                if type(checked) is dt.date:
                    meta["checked_at"] = checked.isoformat()
                elif isinstance(checked, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", checked):
                    meta["checked_at"] = dt.date.fromisoformat(checked).isoformat()
                else:
                    raise ValueError("not a date")
            except ValueError:
                self.issue("invalid_checked_at", path, "Use YYYY-MM-DD or null; do not infer a check date.")
        if store == "records":
            present = set(RECORD_FIELDS).intersection(meta)
            if not present:
                self.issue("legacy_record_fields", path,
                           "Retrieval/prevention fields are unrecorded; preserve this entry and normalize only during authorized edits.",
                           "error" if self.strict else "warning")
            elif len(present) != len(RECORD_FIELDS):
                self.issue("missing_record_fields", path, ", ".join(field for field in RECORD_FIELDS if field not in meta))
            else:
                invalid_record = []
                for field in ("trigger", "symptom", "prevention"):
                    value = meta[field]
                    if value is None and field != "symptom":
                        continue
                    if not isinstance(value, str) or not value.strip():
                        invalid_record.append(field)
                for field, states in (("cause_status", CAUSE_STATES), ("prevention_status", PREVENTION_STATES)):
                    if not isinstance(meta[field], str) or meta[field] not in states:
                        invalid_record.append(field)
                if isinstance(meta["prevention_status"], str) and meta["prevention_status"] in PREVENTION_STATES:
                    absent = meta["prevention"] is None
                    if (meta["prevention_status"] == "none") != absent:
                        invalid_record.append("prevention must be null exactly when prevention_status is none")
                    if meta["prevention_status"] == "verified" and meta["checked_at"] is None:
                        invalid_record.append("verified prevention requires a checked_at evidence date")
                if invalid_record:
                    self.issue("invalid_record_fields", path, ", ".join(invalid_record))
        if "context" in meta:
            context = meta["context"]
            if not isinstance(context, (str, dict)) or (isinstance(context, dict) and any(
                    not isinstance(key, str) or not isinstance(value, str) for key, value in context.items())):
                self.issue("invalid_context", path, "Optional context must be a string or a flat mapping of strings; quote versions.")
        sections = headings(body)
        for name in SECTIONS[store]:
            if not "\n".join(sections.get(name.casefold(), [])).strip():
                self.issue("missing_section", path, name)
        old = self.ids.get(meta["id"].casefold())
        if old is not None and old != key:
            self.issue("duplicate_id", path, f"Also used by {self.relative(old)}")
        self.ids[meta["id"].casefold()] = key
        if not any(item["level"] == "error" for item in self.messages[validation_start:]):
            entry["meta"] = meta
        return entry

    def catalog_parts(self, path, store):
        if not path.exists():
            label = " archive" if path.name == "archive.md" else ""
            return f"# {path.parent.name} {store}{label}\n\n", "", []
        text = self.read(path)
        if text is None:
            return "", "", []
        self.links(path, text)
        if START in text or END in text:
            if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
                self.issue("invalid_catalog_markers", path, "Expected one ordered managed block.")
                return "", "", []
            prefix, rest = text.split(START, 1)
            inside, suffix = rest.split(END, 1)
        else:
            lines = text.splitlines(keepends=True)
            start = next((i for i, line in enumerate(lines) if line.lstrip().startswith("|")
                          and re.search(r"\b(detail|link)s?\b", line, re.I)), None)
            if start is None:
                prefix, inside, suffix = text.rstrip() + "\n\n", "", ""
            else:
                finish = start
                while finish < len(lines) and lines[finish].lstrip().startswith("|"):
                    finish += 1
                prefix = "".join(lines[:start])
                inside = "".join(lines[start:finish])
                suffix = "".join(lines[finish:])
                if suffix.strip() == "No entries yet.":
                    suffix = "\n"
        rows = []
        header = None
        for line in inside.splitlines():
            if not line.lstrip().startswith("|"):
                header = None
                continue
            refs = LINK.findall(line)
            if not refs:
                if not re.fullmatch(r"[| :\-]+", line):
                    header = line
                continue
            target = self.local_target(path, refs[-1])
            if target is None:
                continue
            if target.suffix.lower() != ".md" or target.name.lower() in {"index.md", "archive.md"}:
                self.issue("invalid_catalog_target", path, "Catalog rows must point to canonical detail files.")
                continue
            store_root = self.project / store
            if not target.resolve().is_relative_to(store_root.resolve()):
                self.issue("invalid_catalog_target", path, "A related detail must belong to the same store.")
                continue
            if not target.is_file():
                self.issue("broken_catalog_link", path, f"Missing detail: {self.relative(target)}")
                continue
            rows.append((target, header or HEADER, line))
        return prefix, suffix, rows

    def row(self, entry, directory):
        meta = entry["meta"]
        context = meta.get("context")
        scope = meta["scope"]
        if context:
            scope += "; " + (json.dumps(context, ensure_ascii=False, sort_keys=True, default=str)
                              if isinstance(context, dict) else context)
        summary = meta["summary"]
        state = f"{meta['status']} / {meta['checked_at'] or 'unknown'}"
        if entry["store"] == "records":
            if all(field in meta for field in RECORD_FIELDS):
                summary += f"; Trigger: {meta['trigger'] or 'unknown'}; Symptom: {meta['symptom']}"
                state += f"; Cause: {meta['cause_status']}; Prevention [{meta['prevention_status']}]: {meta['prevention'] or 'not established'}"
            else:
                summary += "; Trigger/symptom: unrecorded"
                state += "; Cause/prevention: unrecorded"
        values = [f"{meta['id']} / {meta['title']} [{meta['kind']}]", summary, scope,
                  ", ".join(meta["keywords"]), state]
        target = quote(os.path.relpath(entry["path"], directory).replace(os.sep, "/"), safe="/._-")
        return "| " + " | ".join(cell(x) for x in values) + f" | [{cell(meta['id'])}]({target}) |"

    def render(self, path, prefix, suffix, structured, legacy):
        header = RECORD_HEADER if path.relative_to(self.project).parts[0] == "records" else HEADER
        lines = [START, "Generated from canonical English metadata; edit detail files, not these rows.", "", header, SEPARATOR]
        lines.extend(self.row(entry, path.parent) for entry in sorted(structured, key=lambda x: x["meta"]["id"].casefold()))
        if legacy:
            lines += ["", "## Legacy entries", "", "Prior index text below is unverified metadata, not an inferred rule or status."]
            groups = {}
            for header, row in legacy:
                groups.setdefault(header, set()).add(row)
            for header, rows in sorted(groups.items()):
                columns = len(re.split(r"(?<!\\)\|", header.strip().strip("|")))
                lines += ["", header, "| " + " | ".join("---" for _ in range(columns)) + " |", *sorted(rows)]
        lines += [END]
        return prefix.rstrip() + "\n\n" + "\n".join(lines) + "\n" + suffix.lstrip("\r\n")

    def domain(self, store, directory):
        if not self.safe(directory / "index.md"):
            return
        self.domains.append(self.relative(directory))
        parts = {}
        references = {}
        for name in ("index.md", "archive.md"):
            path = directory / name
            parts[name] = self.catalog_parts(path, store)
            for target, header, row in parts[name][2]:
                references.setdefault(target.resolve(), []).append((name, header, row, target))
        local = {}
        for current, dirs, names in os.walk(directory, followlinks=False):
            current = Path(current)
            retained = []
            for name in dirs:
                path = current / name
                if name.startswith("."):
                    continue
                if path.is_symlink() or not path.resolve().is_relative_to(self.project):
                    self.issue("outside_project", path, "Do not traverse linked directories; use explicit catalog references.")
                else:
                    retained.append(name)
            dirs[:] = retained
            for name in sorted(names):
                path = current / name
                if path.suffix.lower() != ".md" or human_file(path) or name.lower() in {"index.md", "archive.md"}:
                    continue
                entry = self.entry(path, store)
                if entry is not None:
                    local[path.resolve()] = entry
        for key, refs in references.items():
            if key not in local:
                entry = self.entry(refs[0][3], store)
                if entry is not None:
                    local[key] = entry
        buckets = {"index.md": [], "archive.md": []}
        legacy = {"index.md": [], "archive.md": []}
        for key, entry in local.items():
            if entry["meta"] is not None:
                name = "archive.md" if entry["meta"]["status"] == "superseded" else "index.md"
                buckets[name].append(entry)
            elif entry["legacy"]:
                refs = references.get(key, [])
                if refs:
                    for name, header, row, _ in refs:
                        legacy[name].append((header, row))
                else:
                    target = quote(os.path.relpath(entry["path"], directory).replace(os.sep, "/"), safe="/._-")
                    row = f"| legacy / {cell(entry['path'].stem)} | Metadata unavailable; inspect before use. | unknown | unknown | unknown | [file]({target}) |"
                    legacy["index.md"].append((HEADER, row))
        for name in buckets:
            path = directory / name
            if name == "archive.md" and not path.exists() and not buckets[name] and not legacy[name]:
                continue
            prefix, suffix, _ = parts[name]
            self.plans[path] = self.render(path, prefix, suffix, buckets[name], legacy[name])
            self.translation(path)
        routing = self.project / store / "index.md"
        if not routing.is_file():
            self.issue("missing_routing", directory / "index.md", "The knowledge skill must create the store's domain routing index.",
                       "warning" if self.command == "build" else "error")
        else:
            routing_text = self.read(routing)
            if routing_text is not None:
                self.links(routing, routing_text)
                destinations = [self.local_target(routing, ref) for ref in LINK.findall(routing_text)]
                if directory / "index.md" not in destinations:
                    self.issue("missing_domain_route", directory / "index.md", "Add this domain to the store routing index.",
                               "warning" if self.command == "build" else "error")
                self.translation(routing)

    def run(self, stores, domains):
        found = set()
        for store in stores:
            base = self.project / store
            if not base.is_dir():
                continue
            if not self.safe(base / "index.md"):
                continue
            for directory in sorted(base.iterdir()):
                if not directory.is_dir() or directory.name.startswith("."):
                    continue
                if domains and directory.name not in domains:
                    continue
                found.add(directory.name)
                self.domain(store, directory)
        for missing in set(domains) - found:
            self.issue("missing_domain", self.project, f"No selected store contains domain {missing}.")
        if not self.domains and not domains:
            self.issue("no_stores", self.project, "No domain stores found; nothing created.", "warning")
        # Resolve existence only after all selected catalog outputs are known.
        planned = {path.resolve() for path in self.plans} if self.command == "build" else set()
        for source, target in self.references:
            if not target.is_file() and target.resolve() not in planned:
                self.issue("broken_reference", source, f"Missing file: {self.relative(target)}")
        if self.command == "check":
            for path, expected in self.plans.items():
                if not path.is_file():
                    self.issue("missing_catalog", path, "Run build within authorized write scope.")
                else:
                    actual = self.read(path)
                    if actual is not None and actual != expected:
                        self.issue("stale_catalog", path, "Catalog differs from its canonical metadata; run build.")
        elif not any(x["level"] == "error" for x in self.messages):
            for path, expected in self.plans.items():
                if path.is_file() and self.read(path) == expected:
                    continue
                temporary = None
                try:
                    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent,
                                                     prefix=".catalog-", suffix=".tmp", delete=False) as stream:
                        temporary = Path(stream.name)
                        stream.write(expected)
                    os.replace(temporary, path)
                    self.written.append(self.relative(path))
                except OSError as exc:
                    self.issue("write_failed", path, str(exc))
                    break
                finally:
                    if temporary is not None and temporary.exists():
                        temporary.unlink()
        errors = sum(x["level"] == "error" for x in self.messages)
        return {"ok": errors == 0, "command": self.command, "domains": self.domains,
                "structured_entries": sum(x["meta"] is not None for x in self.entries.values()),
                "legacy_entries": sum(x["legacy"] for x in self.entries.values()),
                "catalogs_written": self.written, "errors": errors,
                "warnings": len(self.messages) - errors, "diagnostics": self.messages[:20],
                "diagnostics_total": len(self.messages)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check"))
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--store", choices=("knowledge", "records", "both"), default="both")
    parser.add_argument("--domain", action="append", default=[])
    parser.add_argument("--strict", action="store_true", help="Treat legacy prose and pre-extension record headers as errors instead of warnings.")
    args = parser.parse_args()
    if not args.project.is_dir():
        parser.error("--project must name an existing directory")
    if any(not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", name) for name in args.domain):
        parser.error("--domain must be a lowercase directory name, not a path")
    if yaml is None:
        print(json.dumps({"ok": False, "error": "PyYAML is required; use an existing runtime with it. Nothing installed or written."}))
        return 2
    stores = ("knowledge", "records") if args.store == "both" else (args.store,)
    result = Catalogs(args.project, args.command, args.strict).run(stores, args.domain)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
