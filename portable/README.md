# Use OneStep in another project

## Local projects

1. Extract [OneStep-Project.zip](OneStep-Project.zip) into a separate folder.
2. Copy the `onestep-strategy` folder into the destination project root. Copy the entry files for your tools alongside it: `AGENTS.md` for Codex, `CLAUDE.md` for Claude Code and `GEMINI.md` for Gemini CLI. If the project already has an instruction file, append the corresponding kit text to it. Use the active instruction file if the tool has a custom filename or an override such as `AGENTS.override.md`.
3. Open a fresh AI session in the destination project. To check discovery, ask “Which OneStep operation and specialist would you use to revise this project's deliverable? Give the source paths and one check specific to the deliverable.” Check the tool's file reads and the proposed check against the installed material.

The copy method needs an archive extractor and project write access. You can move or commit the resulting project with its strategy folder and entry files. Only the optional catalog and retrieval scripts require Python 3.9+ and PyYAML. Project facts, evidence archives, test fixtures and personal source bindings are outside the kit. Knowledge procedures use the destination project's available sources.

To merge all three standard entry files automatically, use Python 3.8+ from the extracted kit:

```powershell
py -3 install.py "D:\Work\My Project"
```

```sh
python3 install.py "$HOME/Work/My Project"
```

Rerunning the same kit keeps existing UTF-8 instructions and skips identical entries. For a new release, move the old `onestep-strategy` folder aside, install the new folder and review any local edits before retiring the old copy. If an entry uses another encoding, merge the text in your editor. For another agent, append the same entry text wherever it accepts persistent project instructions.

## ChatGPT Projects and Gemini Gems

Upload [OneStep-Web.txt](OneStep-Web.txt) as a project source in ChatGPT or a Knowledge file in a Gemini Gem. Put the following in the project's or Gem's instructions:

> For each new substantive task, follow OneStep-Web.txt. Start with agents/vegabond-agent.md and skills/vegabond-scout/SKILL.md, then use the sections Scout selects. Prioritize this project's materials and report any required checks you could not perform.

For a check, give the AI a manuscript excerpt to revise or a document to review. Ask it to name the selected operation, cite the relevant section and show a correction in the supplied material. Replace the uploaded file when adopting a new release. Builds, playtests and other external checks depend on the tools available in that session.

## Find game development references

The ZIP and web upload both include the reviewed game and engineering references and four game-development incident records. The local entry instructions and web introduction route the AI to the bundled library after it consults the working project. Search the game, code and incident indexes by API name, concept or symptom, then read the matched ID's detail for scope, checks and evidence. For example, ask “Find `TVector::Equals` in the OneStep incident records. Why might a component stop short of an easing endpoint? Cite the record ID and propose a check for this project.”

With Python 3.9+ and PyYAML, run this from the destination project root:

```text
python onestep-strategy/skills/vegabond-knowledge/scripts/search.py search --project onestep-strategy --query "메모리 풀링" --portable-library
```

For a plain text lookup open `knowledge/game/index.md`, `knowledge/code/index.md` or `records/code/index.md` under `onestep-strategy/`. In the web upload, those same paths are section headings. The source registry describes cited historical observations. Use the destination project's own evidence for current runtime claims.

## Refresh the distribution

From the OneStep checkout, with Python and PyYAML, run `python portable/build.py` and then `python portable/test_portable.py`. The reviewed paths are listed in `portable/game-library.txt`. Refresh the canonical catalogs after changing entries and before building the distribution. Distribute the two generated files.
