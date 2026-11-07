"""Materialize blind task inputs in an isolated, disposable project.

No answer key is read or copied. All generated facts/records are synthetic.
"""

import argparse
import json
from pathlib import Path
import re
import sys
import uuid

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from catalog import Catalogs, yaml


CASES = Path(__file__).with_name("cases.json")


def inside(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"fixture path escapes its project: {relative}")
    return path


def write(root, relative, text, human_pair=False):
    path = inside(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(text)
    if human_pair:
        # Test-only existence stub; it is deliberately not a canonical input.
        path.with_name(path.stem + ".kr.md").write_text(
            "# 합성 평가용 사람 전용 파일\n\n정본 입력은 영어 파일이며 이 파일은 조회하지 않습니다.\n", encoding="utf-8")
    return path


def prepare(root, case):
    root = root.resolve()
    if root.exists():
        raise ValueError(f"refusing to overwrite an existing fixture project: {root}")
    root.mkdir(parents=True)
    write(root, "request.md", "# Synthetic evaluation request\n\n" + case["request"] +
          "\n\nThis is a synthetic project. Use only its supplied evidence; do not contact services or change source files.\n")
    for relative, text in case["files"].items():
        write(root, relative, text)
    domains = {"knowledge": set(), "records": set()}
    for entry in case["entries"]:
        ident, domain, store = entry["id"], entry["domain"], entry.get("store", "knowledge")
        if not re.fullmatch(r"[A-Za-z0-9._-]+", ident) or not re.fullmatch(r"[a-z0-9-]+", domain) or store not in domains:
            raise ValueError("invalid fixture entry identity")
        domains[store].add(domain)
        meta = dict(id=ident, title=entry["title"], summary=entry["summary"],
                    kind="reference" if store == "knowledge" else "error", scope=entry["scope"],
                    keywords=entry["keywords"], status="active" if store == "knowledge" else "resolved", checked_at=None)
        if "context" in entry:
            meta["context"] = entry["context"]
        if store == "records":
            meta.update({key: entry[key] for key in ("trigger", "symptom", "cause_status", "prevention", "prevention_status")})
        first, second, third = ("Guidance", "Applicability and exceptions", "Checks") if store == "knowledge" else (
            "Expected and observed", "Cause and resolution", "Recheck and prevention")
        source = inside(root, entry["source"])
        if not source.is_file():
            raise ValueError(f"missing fixture source: {entry['source']}")
        body = (f"\n# {entry['title']}\n\n## {first}\n\n{entry['guidance']}\n\n## {second}\n\n"
                f"{entry['scope']}. Synthetic fixture assertions only; no real incident or universal guarantee.\n\n"
                f"## {third}\n\nInspect the linked source and actual requested boundary before applying. "
                "No runtime or real-user verification was performed for this synthetic entry.\n\n"
                f"## Evidence\n\n[Synthetic input](../../{entry['source']}). "
                "This is authored evaluation data, not an external-source check.\n")
        write(root, f"{store}/{domain}/{ident}.md", "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n" + body, True)
    for store, selected in domains.items():
        write(root, f"{store}/index.md", "# Synthetic domains\n\n" +
              "\n".join(f"[{domain}]({domain}/index.md)" for domain in sorted(selected)) + "\n", True)
    checker = Catalogs(root, "build")
    result = checker.run(("knowledge", "records"), [])
    if not result["ok"]:
        raise ValueError(json.dumps(result))
    for relative in result["catalogs_written"]:
        path = root / relative
        path.with_name(path.stem + ".kr.md").write_text("# 합성 평가 목록의 사람 전용 파일\n", encoding="utf-8")
    return dict(id=case["id"], skill=case["skill"], project=str(root), request=str(root / "request.md"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True, help="OneStep checkout owning the disposable .cache directory")
    parser.add_argument("--case", action="append", default=[])
    args = parser.parse_args()
    try:
        if yaml is None:
            raise ValueError("Use the existing catalog runtime with PyYAML")
        project = args.project.resolve()
        if not project.is_dir():
            raise ValueError("project must exist")
        destination = project / ".cache/onestep/information-needs" / uuid.uuid4().hex[:12]
        for ancestor in (project / ".cache", project / ".cache/onestep", destination.parent):
            if ancestor.is_symlink() or getattr(ancestor, "is_junction", lambda: False)() or not ancestor.resolve().is_relative_to(project):
                raise ValueError("linked or outside-project cache directory")
        cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
        chosen = [c for c in cases if not args.case or c["id"] in args.case]
        if args.case and set(args.case) - {c["id"] for c in chosen}:
            raise ValueError("unknown case ID")
        print(json.dumps({"synthetic": True, "cases": [prepare(destination / c["id"], c) for c in chosen]}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
