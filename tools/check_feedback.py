"""Check a strategy report pair in this OneStep checkout's feedback inbox."""

import argparse
import json
from pathlib import Path
import re
import stat


def file_state(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return "missing"
    except OSError as exc:
        return f"unavailable: {exc}"
    if not stat.S_ISREG(info.st_mode):
        return "not a regular file"
    return "present" if info.st_size else "empty"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="English report filename, e.g. YYYY-MM-DD-topic.md")
    args = parser.parse_args()
    if (not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/\\:*?\"<>|\x00-\x1f]+\.md", args.report)
            or args.report.casefold().endswith(".kr.md")):
        parser.error("supply the dated English report filename only")

    inbox = Path(__file__).resolve().parents[1] / "feedback"
    report = inbox / args.report
    paths = [report, report.with_suffix(".kr.md")]
    files = {str(path): file_state(path) for path in paths}
    present = all(state == "present" for state in files.values())
    print(json.dumps({"pair_present": present, "files": files}, indent=2))
    return 0 if present else 1


if __name__ == "__main__":
    raise SystemExit(main())
