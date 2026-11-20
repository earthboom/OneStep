# Crossing Tactics

Build the game with MSVC C++17 and run it from this directory in PowerShell.

```powershell
cmd /c build.cmd
.\out\tactics.exe
```

The build script uses the MSVC compiler already on PATH when available. Otherwise it loads Visual Studio 2026 Community from its standard path. Set `ONESTEP_VCVARS64` to your installation’s `vcvars64.bat` when needed.

Type `list` to see available encounters and `start core` to begin. `P` marks your unit, `E` marks the enemy, and dots mark empty cells. Use `move left`, `move right`, `strike`, and `guard`. A strike requires an adjacent enemy. After each valid action the enemy attacks from an adjacent cell or advances one cell. Guard absorbs up to 2 damage and counters for 1 when the player survives an adjacent attack. If the player's action defeats the enemy, the turn reports that the enemy cannot act. `status` shows the board, health and turn. `start ID` begins a fresh encounter, and `quit` exits.

To replay Bulwark's winning sequence through stdin:

```powershell
@('list','start bulwark','move left','guard','guard','strike','strike','quit') | .\out\tactics.exe
```

## Encounter files

The game scans lowercase `.enc` files in `packs` by default. Pass a directory as the only argument to use another configuration. An absent directory or a directory without encounter files provides the built-in Crossing encounter. Harrier and Bulwark are optional, so leaving either file out removes only that encounter.

Each file has a lower-case ID in its filename, such as `bulwark.enc`. IDs begin with a letter and allow lowercase letters, digits and hyphens up to 24 characters. `core` is reserved. Use ASCII and one `key=value` pair per line. Blank lines and full-line comments beginning with `#` are permitted. The fields are `name` (up to 48 printable characters), `board` (4–12 cells with exactly one `P` and one `E`), `player_hp`, `enemy_hp`, `player_damage` and `enemy_damage` (all four integers from 1 to 20). Invalid files fail startup with a diagnostic, exit code 2 and an empty stdout so a faulty catalog never becomes playable.

## Verification

```powershell
cmd /c build.cmd
python -B verify.py --fault
```

The check launches the executable with neither pack, Harrier only, Bulwark only, and both. It exercises ordering, rejection, absence, content diagnostics, victory, defeat and restarting. `--only b` runs just the Bulwark-only configuration. The optional `--fault` also builds a temporary copy with a deliberately broken dependency. The [workflow record](WORKFLOW.md) links the baseline, extension and final runtime evidence.
