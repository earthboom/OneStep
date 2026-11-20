"""Return a Markdown excerpt and record what was shown to the performer."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--outline", action="store_true")
    mode.add_argument("--section", help="Exact level-two heading, without the Markdown prefix")
    args = parser.parse_args()
    path = args.path.resolve()
    label = args.section or ("outline" if args.outline else "full")
    trace = Path(__file__).with_name("doc_reads.jsonl")

    if path.name.lower().endswith(".kr.md"):
        with trace.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"path": path.as_posix(), "mode": "blocked-translation"}) + "\n")
        parser.error("Human-only translation")
    content = path.read_text(encoding="utf-8-sig")
    lines = content.splitlines()
    if args.outline:
        content = "\n".join(line for line in lines if line.startswith("#"))
    if args.section:
        heading = f"## {args.section}"
        if heading not in lines:
            parser.error(f"Section not found: {args.section}")
        start = lines.index(heading)
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        content = "\n".join(lines[start:end])

    with trace.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"path": path.as_posix(), "mode": label}) + "\n")
    print(content)


if __name__ == "__main__":
    main()
