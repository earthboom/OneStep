"""Read heading-selected Markdown sections from known project paths."""

import argparse
from pathlib import Path
import re
import sys


HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*)$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def headings_in(lines):
    headings = {}
    fence = None
    for number, line in enumerate(lines, start=1):
        marker = FENCE.match(line)
        if fence is not None:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
        elif heading := HEADING.match(line):
            level = len(heading[1])
            title = re.sub(r"[ \t]+#+[ \t]*$", "", heading[2]).strip()
            headings[number] = (level, title)
    return headings


def matching_lines(lines, heading_pattern):
    """Return original line numbers and text for matching ATX sections."""
    headings = headings_in(lines)
    top_level = [number for number, (level, _) in headings.items() if level == 1]
    document_title = None
    if len(headings) > 1 and len(top_level) == 1 and top_level[0] == next(iter(headings)):
        document_title = top_level[0]

    selected = []
    active_level = None
    active_title = False
    for number, line in enumerate(lines, start=1):
        if number in headings:
            level, title = headings[number]
            if active_level is not None and (active_title or level <= active_level):
                active_level = None
                active_title = False
            if active_level is None and heading_pattern.search(title):
                active_level = level
                active_title = number == document_title
        if active_level is not None:
            selected.append((number, line))
    return selected


def project_markdown(project, name):
    supplied = Path(name)
    if supplied.name.lower().endswith(".kr.md"):
        raise ValueError(f"Human-only translation: {name}")
    path = (project / supplied).resolve(strict=True)
    relative = path.relative_to(project)
    if path.name.lower().endswith(".kr.md"):
        raise ValueError(f"Human-only translation: {name}")
    if path.suffix.lower() not in {".md", ".markdown"} or not path.is_file():
        raise ValueError(f"Expected a Markdown source: {name}")
    return path, relative.as_posix()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--section", action="append", nargs=2, metavar=("FILE", "HEADING_REGEX"), required=True)
    parser.add_argument("--max-chars", type=int, default=12000)
    args = parser.parse_args()
    if args.max_chars < 1:
        parser.error("--max-chars must be positive")

    project = args.project.resolve()
    output = []
    spans = []
    missed = []
    try:
        for name, pattern in args.section:
            path, relative = project_markdown(project, name)
            expression = re.compile(pattern, re.IGNORECASE)
            lines = path.read_text(encoding="utf-8-sig").splitlines()
            selected = matching_lines(lines, expression)
            if not selected:
                missed.append(f"{relative}: no matching Markdown heading for {pattern!r}")
                continue
            output.extend([relative, *(f"{number}: {line}" for number, line in selected), ""])
            spans.append(f"{relative}:{selected[0][0]}-{selected[-1][0]}")
    except (OSError, ValueError, re.error) as error:
        parser.error(str(error))

    for message in missed:
        print(message, file=sys.stderr)
    rendered = "\n".join(output)
    if len(rendered) > args.max_chars:
        parser.error(f"Selected sections exceed --max-chars ({len(rendered)}/{args.max_chars}). "
                     f"Narrow the selectors for {', '.join(spans)}.")
    print(rendered, end="")
    return int(bool(missed))


if __name__ == "__main__":
    sys.exit(main())
