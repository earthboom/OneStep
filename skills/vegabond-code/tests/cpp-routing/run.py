"""Prepare blind, linked fixtures or check their recorded C++ guide reads."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


SUITE = Path(__file__).resolve().parent
CHECKOUT = SUITE.parents[3]
CODE_SKILL = "skills/vegabond-code/SKILL.md"
CPP_GUIDE = "templates/cpp/CPP_IMPLEMENTATION.md"
CPP_TEMPLATE = "templates/cpp/AGENTS.md"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fingerprints():
    files = [SUITE / name for name in ("cases.json", "rubric.json", "read_doc.py")]
    files.extend(CHECKOUT / name for name in (CODE_SKILL, CPP_GUIDE))
    return {path.relative_to(CHECKOUT).as_posix(): sha256(path.read_bytes()).hexdigest() for path in files}


def prepare(parent):
    parent = parent.resolve(strict=True)
    if not parent.is_dir() or parent == CHECKOUT or CHECKOUT in parent.parents:
        raise ValueError("Use an existing writable parent outside the OneStep checkout.")
    cases = read_json(SUITE / "cases.json")["cases"]
    run = Path(tempfile.mkdtemp(prefix="onestep-cpp-routing-", dir=parent))
    for case in cases:
        project = run / case["id"]
        if project.parent != run:
            raise ValueError(f"Invalid case ID: {case['id']}")
        project.mkdir()
        for relative, content in case["files"].items():
            path = project / relative
            if project not in path.resolve().parents:
                raise ValueError(f"Fixture path escapes case: {relative}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        (project / "read_doc.py").write_bytes((SUITE / "read_doc.py").read_bytes())
        (project / "request.md").write_text(case["request"] + "\n", encoding="utf-8")
        subprocess.run([sys.executable, str(CHECKOUT / "link_project.py"), str(project)],
                       cwd=project, check=True, capture_output=True, text=True, encoding="utf-8")
    (run / "run.json").write_text(json.dumps(fingerprints(), indent=2) + "\n", encoding="utf-8")
    return {"run": str(run), "projects": [str(run / case["id"]) for case in cases]}


def check(run):
    run = run.resolve(strict=True)
    rubric = read_json(SUITE / "rubric.json")
    if read_json(run / "run.json") != fingerprints():
        raise ValueError("OneStep guidance or evaluation inputs changed. Prepare a fresh run.")

    guide_path = CHECKOUT / CPP_GUIDE
    results = {}
    for case_id, expected in rubric["cases"].items():
        project = run / case_id
        trace = project / "doc_reads.jsonl"
        rows = [(Path(row["path"]), row["mode"]) for row in
                map(json.loads, trace.read_text(encoding="utf-8").splitlines())] if trace.is_file() else []
        failures = []
        for entry in (project / "AGENTS.md", CHECKOUT / CODE_SKILL):
            if (entry, "full") not in rows:
                failures.append(f"Missing instruction read: {entry.name}")
        if any(path.name.lower().endswith(".kr.md") for path, _ in rows):
            failures.append("Attempted to read a human-only translation.")
        if any(path == CHECKOUT / CPP_TEMPLATE for path, _ in rows):
            failures.append("Opened the standalone C++ template instead of using linked guidance.")
        guide_reads = [mode for path, mode in rows if path == guide_path]
        sections = set(expected["guide_sections"])
        delivered = set(guide_reads) - {"outline"}
        if delivered != sections or (not sections and guide_reads):
            failures.append("C++ guide reads do not match the selected sections.")
        results[case_id] = {"guide_reads": guide_reads, "failures": failures, "review": expected["review"]}
    return {"routing_ok": all(not case["failures"] for case in results.values()), "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("--parent", type=Path, default=Path(tempfile.gettempdir()))
    check_parser = commands.add_parser("check")
    check_parser.add_argument("run", type=Path)
    args = parser.parse_args()
    try:
        result = prepare(args.parent) if args.command == "prepare" else check(args.run)
    except subprocess.CalledProcessError as error:
        parser.exit(2, (error.stderr or str(error)) + "\n")
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f"{error}\n")
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result.get("routing_ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
