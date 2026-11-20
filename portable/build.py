"""Build the portable project kit and the equivalent web knowledge document."""

from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ENTRY = "agents/vegabond-agent.md"
SCOUT = "skills/vegabond-scout/SKILL.md"
LIBRARY_DOMAINS = ("knowledge/game", "knowledge/code", "records/code")
LIBRARY_USE = """## Finding game-development knowledge and incident records

For game work, search the working project's instructions and sources first.
Then use the bundled reference library. Start with knowledge/game/index.md for
game design and techniques, knowledge/code/index.md for engineering and Unreal
APIs, or records/code/index.md for symptoms, causes and prevention. Look up the
exact API symbol, its English or Korean aliases, or the observed symptom. Compare
the matching detail's conditions and Evidence before applying it. Cite its ID
and distinguish a documented contract or historical result from a check run here.
Keep new project-specific facts and incidents in the working project's stores.

In a local project, these paths are under onestep-strategy/. With Python and
PyYAML, the following command searches both bundled stores from the project root:

    python onestep-strategy/skills/vegabond-knowledge/scripts/search.py search --project onestep-strategy --query "메모리 풀링" --portable-library

Without the helper, search the three Markdown indexes and follow a matching ID.
If a term is absent from an index, search the detail text for the term or a synonym.
In OneStep-Web.txt use the same index and detail paths as section headings.
"""
ADAPTER = f"""## OneStep

For each new substantive task, read onestep-strategy/{ENTRY}
and onestep-strategy/{SCOUT} relative to this project root.
Use onestep-strategy as the root for paths to OneStep procedures. Resolve
relative Markdown links from their containing document. Read only the procedures
needed for the task. Use this working project's instructions, sources and
stores first. Treat the bundled strategy as reference material. Report any
required checks you cannot perform.
"""
WEB = """Use OneStep-Web.txt for each new substantive task. Start with the sections
agents/vegabond-agent.md and skills/vegabond-scout/SKILL.md, then use the
operation and specialist sections Scout selects. Use this project's instructions,
files and user request first. Resolve OneStep paths as section names in this
document. For game tasks consult the keyword indexes in knowledge/game/index.md,
knowledge/code/index.md and records/code/index.md. Retrieve the matching detail
by ID and use its Evidence and applicability conditions. Report missing
sources or tools and distinguish performed checks from checks needing access."""


def sources():
    paths = [ROOT / ENTRY, ROOT / SCOUT]
    for pattern in ("agents/references/*.md", "skills/vegabond-*/SKILL.md",
                    "skills/vegabond-*/references/*.md"):
        paths.extend(sorted(ROOT.glob(pattern)))
    paths.extend(ROOT / name for name in ("feedback/README.md", "feedback/template.md",
                                         "templates/cpp/CPP_IMPLEMENTATION.md"))
    for path in dict.fromkeys(paths):
        if path.name.endswith(".kr.md"):
            continue
        content = path.read_text(encoding="utf-8")
        if path == ROOT / ENTRY:
            content += "\n" + LIBRARY_USE
        yield path.relative_to(ROOT).as_posix(), content


def game_library():
    entries = {}
    indexes = {}
    routes = []
    source_ids = set()
    for line in (HERE / "game-library.txt").read_text(encoding="utf-8").splitlines():
        name = line.strip()
        if not name or name.startswith("#"):
            continue
        folder, _, filename = name.rpartition("/")
        if (folder not in LIBRARY_DOMAINS or not re.fullmatch(r"[KR]-[A-Z0-9-]+\.md", filename)
                or name in entries):
            raise ValueError(f"Invalid or duplicate library member: {name}")
        content = (ROOT / name).read_text(encoding="utf-8")
        ident = filename[:-3]
        meta = yaml.safe_load(content.split("---\n", 2)[1])
        if meta["id"] != ident:
            raise ValueError(f"Library ID mismatch: {name}")
        if ident == "K-GAME-TECH-GUIDE":
            # The topic map is portable. Route to the reviewed technical references.
            content = re.sub(r"\[([^\]]+)\]\(https://www\.youtube\.com/shorts/[^)]+\)", r"\1", content)
        entries[name] = content
        source_ids.update(m.upper() for m in re.findall(r"sources\.md#(src-[a-z0-9-]+)", content, re.I))

    for folder in LIBRARY_DOMAINS:
        # Reuse the canonical catalog rows, including symptoms and prevention states.
        name = folder + "/index.md"
        catalog = (ROOT / name).read_text(encoding="utf-8").splitlines()
        selected = {Path(p).stem for p in entries if p.rpartition("/")[0] == folder}
        rows = [row for row in catalog if row.startswith("| ") and row[2:].split(" / ", 1)[0] in selected]
        if len(rows) != len(selected) or {r[2:].split(" / ", 1)[0] for r in rows} != selected:
            raise ValueError(f"Rebuild the source catalog before packaging {folder}")
        header = next(i for i, line in enumerate(catalog) if line.startswith("| ID / title"))
        indexes[name] = "\n".join([catalog[0], "", *catalog[header:header + 2], *rows, ""])
        routes.append(f"- [{catalog[0].lstrip('# ')}](../{name})")

    for store in ("knowledge", "records"):
        indexes[f"{store}/index.md"] = "# Portable game library\n\n" + "\n".join(routes) + "\n"

    registry = yaml.safe_load((ROOT / "knowledge/sources.md").read_text(encoding="utf-8").split("---\n", 2)[1])
    # Package only cited historical identities. Active bindings and private source files stay local.
    provenance = {key: {"project": None, "path": None, "sha256": registry["sources"][key]["sha256"]}
                  for key in sorted(source_ids)}
    sources_yaml = yaml.safe_dump({"sources": provenance}, sort_keys=False)
    headings = [f"## {key}\n\nHistorical source only. Original unavailable in this kit." for key in provenance]
    indexes["knowledge/sources.md"] = f"---\n{sources_yaml}---\n\n# Evidence provenance\n\n" + "\n\n".join(headings) + "\n"
    return {**indexes, **entries}


def build():
    sections = dict(sources())
    sections.update(game_library())
    for required in (ENTRY, SCOUT, "skills/vegabond-create/SKILL.md",
                     "skills/vegabond-revise/SKILL.md", "skills/vegabond-research/SKILL.md"):
        if required not in sections:
            raise ValueError(f"Missing entry point: {required}")
    web = WEB + "\n\nProject stores, external evidence and executable helpers are supplied by the working environment.\n"
    for name, content in sections.items():
        web += f"\n===== {name} =====\n\n{content.rstrip()}\n"
    (HERE / "OneStep-Web.txt").write_bytes(web.encode("utf-8"))

    files = {f"onestep-strategy/{key}": value for key, value in sections.items()}
    helper = ROOT / "skills/vegabond-knowledge/scripts"
    for path in sorted(helper.iterdir()):
        if path.suffix in (".py", ".json") and path.is_file():
            files["onestep-strategy/" + path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
    for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        files[name] = ADAPTER
    files["install.py"] = (HERE / "install.py").read_text(encoding="utf-8")
    files["QUICKSTART.txt"] = """Extract this ZIP to a separate folder.
For a new project copy onestep-strategy and the three root Markdown files
into the project. For an existing project keep its instructions and append
the corresponding kit text to each active instruction file.
Alternatively, from the extracted kit run:
  Windows: py -3 install.py "path to project"
  macOS or Linux: python3 install.py "path to project"
Open the destination project in a new session.
"""
    # Fixed member order, timestamps, permissions and newlines across build hosts.
    with ZipFile(HERE / "OneStep-Project.zip", "w") as archive:
        for name, content in sorted(files.items()):
            info = ZipInfo(name)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content.encode("utf-8"), compress_type=ZIP_DEFLATED)


if __name__ == "__main__":
    build()
