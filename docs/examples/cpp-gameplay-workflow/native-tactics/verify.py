"""Exercise the shipped command interface with physically staged encounter files."""

import argparse
import subprocess
import tempfile
from pathlib import Path
from shutil import copyfile

ROOT = Path(__file__).resolve().parent
PACKS = ROOT / "packs"
ENCOUNTER_NAMES = {"core": "Crossing", "harrier": "Harrier Yard", "bulwark": "Bulwark Gate"}


def play(executable, directory, commands):
    arguments = [str(executable)]
    if directory is not None:
        arguments.append(str(directory))
    return subprocess.run(
        arguments,
        cwd=ROOT,
        input="\n".join(commands) + "\n",
        text=True,
        capture_output=True,
        timeout=10,
    )


def expect(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}\nExpected {expected!r}\nObserved {actual!r}")


def expect_play(result, ids, states, events, label):
    expect(result.returncode, 0, f"{label} exit")
    expect(result.stderr, "", f"{label} stderr")
    lines = result.stdout.splitlines()
    expect([ln for ln in lines if ln.startswith("Encounter ")],
           [f"Encounter {id} | {ENCOUNTER_NAMES[id]}" for id in ids], f"{label} catalog")
    expect([ln for ln in lines if ln.startswith("State ")], states, f"{label} states")
    expect([ln for ln in lines if ln.startswith(("Player ", "Enemy ", "Rejected ", "Result "))],
           events, f"{label} event order")

    pending = None
    for line in lines:
        if line.startswith("Player "):
            expect(pending, None, f"{label}: previous action still pending")
            pending = "player"
        elif line.startswith("Enemy "):
            expect(pending, "player", f"{label}: enemy response before player action")
            pending = "enemy"
        elif line.startswith("Result "):
            expect(pending, "enemy", f"{label}: result before enemy response")
            pending = "result"
        elif line.startswith("State "):
            if pending == "player":
                raise AssertionError(f"{label}: state emitted before enemy response")
            pending = None
        elif line.startswith("Rejected "):
            expect(pending, None, f"{label}: rejection during a resolving turn")
    expect(pending, None, f"{label}: final turn missing state")


CORE_STATES = [
    "State turn=0 board=P...E player_hp=6 enemy_hp=3",
    "State turn=0 board=P...E player_hp=6 enemy_hp=3",
    "State turn=0 board=P...E player_hp=6 enemy_hp=3",
    "State turn=1 board=.P.E. player_hp=6 enemy_hp=3",
    "State turn=2 board=..PE. player_hp=4 enemy_hp=3",
    "State turn=3 board=..PE. player_hp=2 enemy_hp=1",
    "State turn=4 board=..P.. player_hp=2 enemy_hp=0",
    "State turn=4 board=..P.. player_hp=2 enemy_hp=0",
]
CORE_EVENTS = [
    "Rejected player cannot strike at this distance.",
    "Rejected player cannot move there.",
    "Player moves right.",
    "Enemy closes in.",
    "Player moves right.",
    "Enemy deals 2 damage.",
    "Player deals 2 damage.",
    "Enemy deals 2 damage.",
    "Player deals 2 damage.",
    "Enemy is defeated and cannot act.",
    "Result victory.",
    "Rejected encounter is over. Use start to play again.",
]
A_STATES = [
    "State turn=0 board=.P.E.. player_hp=7 enemy_hp=4",
    "State turn=1 board=..PE.. player_hp=5 enemy_hp=4",
    "State turn=2 board=..PE.. player_hp=5 enemy_hp=3",
    "State turn=3 board=..PE.. player_hp=3 enemy_hp=1",
    "State turn=4 board=..P... player_hp=3 enemy_hp=0",
]
A_EVENTS = [
    "Player moves right.",
    "Enemy deals 2 damage.",
    "Player guards.",
    "Enemy deals 0 damage. Guard counters for 1.",
    "Player deals 2 damage.",
    "Enemy deals 2 damage.",
    "Player deals 2 damage.",
    "Enemy is defeated and cannot act.",
    "Result victory.",
]


def scenario_core(executable, directory, ids):
    result = play(executable, directory, ["list", "start core", "strike", "move left",
                                         "move right", "move right", "strike", "strike", "guard", "quit"])
    expect_play(result, ids, CORE_STATES, CORE_EVENTS, "core")
    return result.stdout


def scenario_a(executable, directory, ids):
    result = play(executable, directory,
                  ["list", "start harrier", "move right", "guard", "strike", "strike", "quit"])
    expect_play(result, ids, A_STATES, A_EVENTS, "A")
    return result.stdout


B_COMMANDS = ["list", "start bulwark", "move left", "guard", "guard", "strike", "strike", "quit"]
B_STATES = [
    "State turn=0 board=E...P. player_hp=5 enemy_hp=5",
    "State turn=1 board=.E.P.. player_hp=5 enemy_hp=5",
    "State turn=2 board=..EP.. player_hp=5 enemy_hp=5",
    "State turn=3 board=..EP.. player_hp=4 enemy_hp=4",
    "State turn=4 board=..EP.. player_hp=1 enemy_hp=1",
    "State turn=5 board=...P.. player_hp=1 enemy_hp=0",
]
B_EVENTS = [
    "Player moves left.",
    "Enemy closes in.",
    "Player guards.",
    "Enemy closes in.",
    "Player guards.",
    "Enemy deals 1 damage. Guard counters for 1.",
    "Player deals 3 damage.",
    "Enemy deals 3 damage.",
    "Player deals 3 damage.",
    "Enemy is defeated and cannot act.",
    "Result victory.",
]


def scenario_b(executable, directory, ids):
    result = play(executable, directory, B_COMMANDS)
    expect_play(result, ids, B_STATES, B_EVENTS, "B")
    return result.stdout


def check_bad_commands(executable, directory, ids):
    result = play(executable, directory, [
        "list", "strike", "status", "start core", "move up", "move", "strike twice", "",
        "start unavailable", "help", "status", "move right", "status", "quit",
    ])
    initial = CORE_STATES[0]
    after_move = CORE_STATES[3]
    expect_play(result, ids, [initial] * 7 + [after_move] * 2, [
        "Rejected start an encounter first.",
        "Rejected start an encounter first.",
        "Rejected unknown command or direction. Type help for commands.",
        "Rejected invalid arguments. Type help for commands.",
        "Rejected invalid arguments. Type help for commands.",
        "Rejected unknown command or direction. Type help for commands.",
        "Rejected unknown encounter unavailable.",
        "Player moves right.",
        "Enemy closes in.",
    ], "bad command and read-only commands")


def check_defeat_and_restart(executable, directory, ids):
    result = play(executable, directory, [
        "list", "start bulwark", "move left", "move left", "move left",
        "strike", "guard", "start bulwark", "quit",
    ])
    defeated = "State turn=3 board=.E.... player_hp=0 enemy_hp=2"
    expect_play(result, ids, [
        B_STATES[0], B_STATES[1], "State turn=2 board=.EP... player_hp=2 enemy_hp=5",
        "State turn=2 board=.EP... player_hp=2 enemy_hp=5", defeated, defeated, B_STATES[0],
    ], [
        "Player moves left.", "Enemy closes in.", "Player moves left.", "Enemy deals 3 damage.",
        "Rejected player cannot move there.",
        "Player deals 3 damage.", "Enemy deals 3 damage.", "Result defeat.",
        "Rejected encounter is over. Use start to play again.",
    ], "defeat, blocked cell and restart")
    return result.stdout


CONFIGURATIONS = {
    "neither": (),
    "a": ("harrier",),
    "b": ("bulwark",),
    "both": ("bulwark", "harrier"),
}


def stage_packs(directory, names):
    directory.mkdir()
    for name in names:
        file = name + ".enc"
        copyfile(PACKS / file, directory / file)
    physical = sorted(item.name for item in directory.iterdir())
    expect(physical, [name + ".enc" for name in names], "physical variant files")
    return physical


def run_configuration(executable, workspace, configuration):
    names = CONFIGURATIONS[configuration]
    directory = workspace / configuration
    print(f"Configuration {configuration} physical files:", stage_packs(directory, names), flush=True)
    ids = sorted(["core", *names])

    print(scenario_core(executable, directory, ids))
    for name, scenario in (("harrier", scenario_a), ("bulwark", scenario_b)):
        if name in names:
            print(scenario(executable, directory, ids))
        else:
            result = play(executable, directory, ["list", "start core", f"start {name}", "status", "quit"])
            expect_play(result, ids, [CORE_STATES[0]] * 3, [f"Rejected unknown encounter {name}."],
                        f"optional absence of {name}")
    if configuration == "both":
        check_bad_commands(executable, directory, ids)
    if "bulwark" in names:
        print(check_defeat_and_restart(executable, directory, ids))
    print(f"PASS {configuration}", flush=True)


def check_bad_content(executable, workspace):
    directory = workspace / "bad-content"
    stage_packs(directory, ("harrier",))
    original = (directory / "harrier.enc").read_text(encoding="ascii")
    file = directory / "invalid.enc"
    cases = [
        ("malformed row", original + "broken\n", "expected key=value"),
        ("invalid integer", original.replace("enemy_hp=4", "enemy_hp=4x"), "must be an integer"),
        ("outside range", original.replace("enemy_hp=4", "enemy_hp=0"), "must be an integer"),
        ("duplicate field", original + "enemy_damage=2\n", "duplicate field enemy_damage"),
        ("missing field", original.replace("enemy_damage=2", ""), "missing field enemy_damage"),
        ("wrong board marker", original.replace(".P.E..", ".P.PE."), "one P and one E"),
        ("sibling reference", original + "requires=bulwark\n", "unknown field requires"),
    ]
    for label, contents, diagnostic in cases:
        file.write_text(contents, encoding="ascii")
        result = play(executable, directory, ["list", "quit"])
        expect(result.returncode, 2, f"{label} exit")
        expect(result.stdout, "", f"{label} exposed partial catalog")
        if "invalid.enc: " not in result.stderr or diagnostic not in result.stderr:
            raise AssertionError(f"{label} diagnostic: {result.stderr!r}")
        print(f"PASS {label}: {result.stderr.strip()}")

    file.unlink()
    reserved = directory / "core.enc"
    reserved.write_text(original, encoding="ascii")
    result = play(executable, directory, ["list", "quit"])
    expect(result.returncode, 2, "reserved ID exit")
    expect(result.stdout, "", "reserved ID exposed partial catalog")
    expect(result.stderr, "Error loading encounters: core.enc: invalid or reserved encounter ID\n",
           "reserved ID diagnosis")
    print("PASS reserved ID")


def check_dependency_fault(executable, workspace):
    directory = workspace / "fault-packs"
    physical = stage_packs(directory, ("bulwark",))
    print("Dependency fault precondition physical files:", physical, flush=True)
    ids = ["bulwark", "core"]
    scenario_b(executable, directory, ids)
    print("PASS precondition: unmodified executable plays B in a B-only directory", flush=True)

    mutant = workspace / "fault-build"
    mutant.mkdir()
    copyfile(ROOT / "build.cmd", mutant / "build.cmd")
    source = (ROOT / "main.cpp").read_text(encoding="utf-8")
    anchor = "            catalog.emplace(id, ReadEncounter(path));"
    expect(source.count(anchor), 1, "fault injection site")
    fault = ('            if (id == "bulwark" && !fs::exists(directory / "harrier.enc")) {\n'
             '                continue;\n'
             '            }\n')
    (mutant / "main.cpp").write_text(source.replace(anchor, fault + anchor), encoding="utf-8")
    subprocess.run(["cmd", "/c", "build.cmd"], cwd=mutant, check=True, timeout=60)

    mutant_exe = mutant / "out" / "tactics.exe"
    both = workspace / "fault-masked"
    stage_packs(both, ("bulwark", "harrier"))
    scenario_b(mutant_exe, both, ["bulwark", "core", "harrier"])
    print("PASS fault masked by A when both physical files are present", flush=True)

    fault_result = play(mutant_exe, directory, B_COMMANDS)
    print(fault_result.stdout)
    expect(fault_result.returncode, 0, "controlled executable launch")
    try:
        expect_play(fault_result, ids, B_STATES, B_EVENTS, "B")
    except AssertionError as error:
        expect(str(error), "B catalog\nExpected ['Encounter bulwark | Bulwark Gate', "
               "'Encounter core | Crossing']\nObserved ['Encounter core | Crossing']",
               "fault detection reason")
        if "Rejected unknown encounter bulwark." not in fault_result.stdout:
            raise AssertionError("fault run never reached selection of B")
        print("PASS controlled fault rejected: B missing from catalog and selection with only B present")
    else:
        raise AssertionError("B-only check accepted the controlled sibling dependency")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", type=Path, default=ROOT / "out" / "tactics.exe")
    parser.add_argument("--baseline", action="store_true", help="Replay the A-only baseline")
    parser.add_argument("--only", choices=CONFIGURATIONS, help="Exercise only this pack configuration")
    parser.add_argument("--fault", action="store_true", help="Build and check a controlled sibling dependency fault")
    args = parser.parse_args()
    executable = args.exe.resolve()
    with tempfile.TemporaryDirectory(prefix="check-", dir=ROOT / "out") as temporary:
        workspace = Path(temporary)
        if args.baseline or args.only:
            run_configuration(executable, workspace, args.only or "a")
        else:
            for configuration in CONFIGURATIONS:
                run_configuration(executable, workspace, configuration)
            check_bad_content(executable, workspace)
            default = play(executable, None, ["list", "start core", "quit"])
            expect_play(default, ["bulwark", "core", "harrier"], CORE_STATES[:1], [], "default launch")
            print("PASS default launch from project root")
        if args.fault:
            check_dependency_fault(executable, workspace)


if __name__ == "__main__":
    main()
