"""Connect a project to this OneStep checkout. Python 3.8+, standard library."""

import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile


CHECKOUT = Path(__file__).resolve().parent
POINTER = ".onestep/checkout.local.json"
START = "<!-- onestep:checkout:start -->"
END = "<!-- onestep:checkout:end -->"
RULE = f"""{START}
## OneStep

For each new substantive task, read `{POINTER}` in this project root.
Its `checkout` value locates the OneStep folder. Resolve relative values from
this project root. If the file is absent, use the sibling folder `../OneStep`.
From that checkout read `agents/vegabond-agent.md` and
`skills/vegabond-scout/SKILL.md`, then follow the selected procedures.
Resolve OneStep links in their source documents. Keep the current working
directory, deliverables, project rules and private records in this project.

Consult this project's sources first. For game development also search the
checkout's `knowledge/game/index.md`, `knowledge/code/index.md` and
`records/code/index.md` by API symbol, Korean or English term, or symptom.
Read the matching detail and its evidence before applying it. With Python and
PyYAML you can run the checkout's `skills/vegabond-knowledge/scripts/search.py`
with `search --project "<resolved checkout>" --query "<term>" --no-cache`.
Use the current files on disk. If the checkout cannot be read, report the
path and access issue so the connection can be repaired.
{END}"""

# Frozen copy of the original ZIP entry for migrating an unedited installation.
ZIP_RULE = """## OneStep

For each new substantive task, read onestep-strategy/agents/vegabond-agent.md
and onestep-strategy/skills/vegabond-scout/SKILL.md relative to this project root.
Use onestep-strategy as the root for paths to OneStep procedures. Resolve
relative Markdown links from their containing document. Read only the procedures
needed for the task. Use this working project's instructions, sources and
stores first. Treat the bundled strategy as reference material. Report any
required checks you cannot perform."""


def read_file(path):
    if path.is_symlink() or path.resolve() != path:
        raise ValueError(f"Cannot update a linked file or directory: {path}")
    if not path.exists():
        return b""
    if not path.is_file():
        raise ValueError(f"Expected a regular file: {path}")
    return path.read_bytes()


def merge_rule(data):
    text = data.decode("utf-8-sig")
    if "\x00" in text:
        raise ValueError("Project instructions must use UTF-8 for automatic merging.")
    newline = "\r\n" if "\r\n" in text else "\n"
    rule = RULE.replace("\n", newline)
    if START in text or END in text:
        if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
            raise ValueError("OneStep markers are incomplete or duplicated. Check the project instructions.")
        first, last = text.index(START), text.index(END) + len(END)
        text = text[:first] + rule + text[last:]
    elif ZIP_RULE.replace("\n", newline) in text:
        text = text.replace(ZIP_RULE.replace("\n", newline), rule, 1)
    else:
        text += (newline * 2 if text else "") + rule + newline
    return (b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b"") + text.encode("utf-8")


def connect(project, check):
    project = project.resolve(strict=True)
    if not project.is_dir() or project == CHECKOUT or CHECKOUT in project.parents:
        raise ValueError("Choose a working project separate from the OneStep checkout.")
    for relative in ("agents/vegabond-agent.md", "skills/vegabond-scout/SKILL.md",
                     "knowledge/game/index.md", "knowledge/code/index.md", "records/code/index.md"):
        if not (CHECKOUT / relative).is_file():
            raise ValueError(f"Incomplete OneStep checkout: {CHECKOUT / relative}")

    override = project / "AGENTS.override.md"
    entry_files = ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]
    if read_file(override).strip():
        entry_files.append(override.name)
    changes = []
    for name in entry_files:
        path = project / name
        original = read_file(path)
        updated = merge_rule(original)
        if original != updated:
            changes.append((path, original, updated))

    pointer = project / POINTER
    prior_pointer = read_file(pointer)
    if pointer.exists():
        config = json.loads(prior_pointer.decode("utf-8-sig"))
        if not isinstance(config, dict) or set(config) != {"checkout"} or not isinstance(config["checkout"], str) or not config["checkout"].strip():
            raise ValueError(f"Invalid checkout pointer: {pointer}")
        bound = (project / config["checkout"]).resolve()
    else:
        bound = (project / "../OneStep").resolve()
    if check:
        if changes or bound != CHECKOUT or not bound.is_dir():
            raise ValueError("Connection differs from this checkout. Rerun the same command without --check.")
        print(f"Connected: {project} -> {bound}")
        return

    try:
        location = Path(os.path.relpath(CHECKOUT, project)).as_posix()
    except ValueError:  # Different Windows drives.
        location = CHECKOUT.as_posix()
    binding = (json.dumps({"checkout": location}, ensure_ascii=False) + "\n").encode("utf-8")
    ignore = pointer.parent / ".gitignore"
    ignored = read_file(ignore)
    if b"/checkout.local.json" not in ignored.splitlines():
        changes.insert(0, (ignore, ignored, ignored + (b"\n" if ignored else b"") + b"/checkout.local.json\n"))
    if prior_pointer != binding:
        changes.append((pointer, prior_pointer, binding))
    # Preflight all inputs first. Replace one file atomically and retry safely if interrupted.
    if changes:
        pointer.parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=project) as scratch:
            for index, (path, before, after) in enumerate(changes):
                if read_file(path) != before:
                    raise ValueError(f"File changed during setup. Rerun after checking {path}.")
                staged = Path(scratch) / str(index)
                staged.write_bytes(after)
                if path.exists():
                    shutil.copymode(path, staged)
                os.replace(staged, path)
    print(f"Connected: {project} -> {CHECKOUT} ({len(changes)} files updated)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Existing game, writing or other working project")
    parser.add_argument("--check", action="store_true", help="Verify the connection without writing")
    args = parser.parse_args()
    try:
        connect(args.project, args.check)
    except (OSError, ValueError) as error:
        parser.exit(1, f"OneStep: {error}\n")
