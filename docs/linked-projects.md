# Use one Git checkout across projects

Clone OneStep once in a convenient folder. For each existing game, novel or document project, run the linker from the checkout. These examples start in the parent folder:

```sh
git clone https://github.com/earthboom/OneStep.git OneStep
python3 OneStep/link_project.py "My Game"
python3 OneStep/link_project.py "My Novel"
python3 OneStep/link_project.py "My Game" --check
```

On Windows use `py -3` in place of `python3`. The target can also be an absolute path on another drive. Only the setup command needs Python 3.8+. Open a new AI session in the working project after setup, with read access to the checkout.

The linker merges a marked block into `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and a nonempty `AGENTS.override.md` if present. When using a custom instruction filename, append the same marked block there. It replaces the original, unedited ZIP instructions in these files. If you customized the old ZIP rule, merge it with the new block in your editor to eliminate conflicting paths.

Each new substantive task starts with the shared agent and Scout and reads the relevant skills. For game tasks the AI consults the local project's sources, then the checkout's game/code indexes and problem records. For example, ask “Why can a component stop short of its easing endpoint? Look up TVector::Equals and cite the incident ID.” Verify the file read and the returned ID, `R-CODE-UE-TRANSFORM-TOLERANCE`. The working project owns its deliverables and private data.

**On another PC**, share the instruction files and `.onestep/.gitignore` in the working project's Git repository. The machine-specific path in `.onestep/checkout.local.json` is ignored. With the two repositories beside each other and the checkout named `OneStep`, the shared instructions resolve `../OneStep` immediately. For any other layout, or after moving the checkout, run its linker again. `--check` tests the active binding and instruction blocks without writing files.

**To update all connected projects**, run `git -C OneStep pull --ff-only` from the parent folder. Start a fresh task/session to read the new files. The linker uses the checkout as it exists on disk, including local edits. Other PCs receive commits published to their Git remote.

**Web chats** need a source they can access. In ChatGPT with GitHub access, authorize this repository and instruct the project to read `agents/vegabond-agent.md` and `skills/vegabond-scout/SKILL.md` from it. Alternatively, upload `portable/OneStep-Web.txt` to a ChatGPT project or Gemini Gem and replace it when you update. [Web setup](../portable/README.md) · [ChatGPT GitHub access](https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt)
