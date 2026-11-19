"""Run from an unpacked OneStep project kit. Requires only Python 3.8+."""

import argparse
import os
from pathlib import Path
import shutil
import tempfile


KIT = Path(__file__).resolve().parent
ADAPTERS = ("AGENTS.md", "CLAUDE.md", "GEMINI.md")
STRATEGY = "onestep-strategy"


def install(project):
    project = project.resolve(strict=True)
    source = KIT / STRATEGY
    target = project / STRATEGY
    if not source.is_dir() or not project.is_dir() or project == KIT:
        raise ValueError("Extract the kit and select an existing, separate project directory.")

    # Preflight all conflicts before adding anything to the working project.
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        raise ValueError(f"Choose a project without a conflicting path: {target}")
    if target.is_dir():
        for item in source.rglob("*"):
            installed = target / item.relative_to(source)
            matches = installed.is_dir() if item.is_dir() else installed.is_file()
            if matches and item.is_file() and not installed.is_symlink():
                matches = item.read_text(encoding="utf-8") == installed.read_text(encoding="utf-8")
            if installed.is_symlink() or not matches:
                raise ValueError(f"Different strategy at {installed}. Move the old {STRATEGY} folder aside and retry.")

    updates = []
    for name in ADAPTERS:
        path = project / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f"Merge the kit instructions manually into {path}.")
        block = (KIT / name).read_text(encoding="utf-8").strip()
        original = path.read_bytes() if path.exists() else b""
        current = original.decode("utf-8-sig")
        if "\x00" in current:
            raise ValueError(f"Merge the kit instructions manually into {path} (non-UTF-8 file).")
        if block in current.replace("\r\n", "\n"):
            continue
        newline = "\r\n" if "\r\n" in current else "\n"
        text = ("\n\n" if current else "") + block + "\n"
        updates.append((path, original, text.replace("\n", newline).encode("utf-8")))

    with tempfile.TemporaryDirectory(dir=project) as temporary:
        stage = Path(temporary)
        if not target.exists():
            snapshot = stage / STRATEGY
            shutil.copytree(source, snapshot)
            snapshot.rename(target)
        for path, original, addition in updates:
            replacement = stage / path.name
            replacement.write_bytes(original + addition)
            if path.exists():
                if path.read_bytes() != original:
                    raise ValueError(f"File changed during installation: {path}. Retry.")
                shutil.copymode(path, replacement)
            os.replace(replacement, path)
    print(f"Installed OneStep. Updated {len(updates)} instruction file(s).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Existing destination project directory")
    try:
        install(parser.parse_args().project)
    except (OSError, ValueError) as error:
        parser.exit(1, f"OneStep: {error}\n")
