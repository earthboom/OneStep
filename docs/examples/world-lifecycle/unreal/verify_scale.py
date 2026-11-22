"""Run and check the standalone D3D11 forest-scale experiment."""

import argparse
from copy import deepcopy
import gzip
import json
import math
import os
from pathlib import Path
import re
from statistics import median
import subprocess

from verify_lifecycle import INSTALL, LEGACY, PROJECT, ROOT, digest, require


MODES = ("resident-full", "streamed-full", "resident-scheduled", "streamed-scheduled")
ORDERS = (MODES, tuple(reversed(MODES)), (MODES[2], MODES[0], MODES[3], MODES[1]))
LEGACY_V2 = LEGACY.with_name("legacy-v2.json")
CHECKPOINTS = ("town", "chunk0", "chunk2", "beforeCombat", "combat", "detached", "afterGc", "offscreen", "revisit")
LOGICAL_TICKS = (24, 48, 72, 96, 96, 96, 96, 120, 144)
CHUNK_ROUTE = (-1, 0, 2, 5, 5, -1, -1, -1, 5)
TRANSITIONS = ("preload", "enter0", "travel2", "travel5", "returnTown", "reenter5")
TRANSITION_CHUNKS = (-1, 0, 2, 5, -1, 5)
GROUPS = ("startup", "transition", "warmup", "steady", "cleanup")
ADAPTER = re.compile(r"LogD3D11RHI: Creating D3DDevice using adapter:\n[^\n]*Description\s*:\s*([^\n]+)")


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def measure(values):
    ordered = sorted(values)
    require(ordered, "Empty sample group")
    return {"n": len(ordered), **{key: ordered[math.ceil(len(ordered) * percentile) - 1]
            for key, percentile in (("p50", 0.50), ("p95", 0.95), ("p99", 0.99), ("max", 1.0))}}


def payload(source):
    return {"schemaVersion": 2, "npcId": "forest-wolf-v2", "hp": max(0, source["hp"] - 40),
            "questStage": 1, "patrolSteps": source["patrolSteps"] + 3}


def verify(run, mode, source, save=None):
    require(run["mode"] == mode and not run["failure"], f"Wrong mode or failed route {run['failure']}")
    require(run["sourceSchema"] == source["schemaVersion"] and run["canonicalNpc"] == "forest-wolf-v2",
            "Loader did not preserve source schema and canonical NPC")
    require(run["windowed"] and (run["viewportX"], run["viewportY"]) == (960, 540)
            and run["vsync"] == run["maxFps"] == 0, "Runtime viewport, VSync or frame-cap settings differ")
    checks = run["checkpoints"]
    if mode == "restore":
        require([entry["name"] for entry in checks] == ["reopened"], "Expected one fresh process restore")
        actual = tuple(checks[0][key] for key in ("hp", "quest", "patrol"))
        require(actual == (source["hp"], source["questStage"], source["patrolSteps"]), "Reopened the wrong v2 state")
        return

    require([entry["name"] for entry in checks] == list(CHECKPOINTS), "Unexpected gameplay checkpoint order")
    require([entry["scheduleTick"] for entry in checks] == list(LOGICAL_TICKS), "Route lost simulation ticks")
    require([entry["chunk"] for entry in checks] == list(CHUNK_ROUTE), "Route visited a wrong chunk")
    require(all(second["worldSeconds"] >= first["worldSeconds"] for first, second in zip(checks, checks[1:])),
            "World clock moved backward")
    require(checks[7]["worldSeconds"] - checks[5]["worldSeconds"] >= 0.8, "Offscreen patrol advanced early")
    streamed = mode.startswith("streamed-")
    scheduled = mode.endswith("-scheduled")
    finished = payload(source)
    for index, row in enumerate(checks):
        local = row["chunk"] >= 0
        expected = int(local) if streamed else 8
        require(row["residentChunks"] == row["visibleChunks"] == row["registeredChunks"] == expected,
                f"Wrong actual residency at {row['name']}")
        require(row["geometryActors"] == expected * 773, f"Wrong world geometry count at {row['name']}")
        require(row["logicalNpcs"] == 2048 and row["activeViews"] == (256 if local else 0), "Population or binding incorrect")
        require(0 < row["recentlyRenderedViews"] <= 256 if local else row["recentlyRenderedViews"] == 0,
                "No recently rendered NPCs in an active viewport")
        require(bool(row["instance"]) == local, "Expected a concrete instance only in visible chunk")
        require(row["hp"] == (source["hp"] if index < 4 else finished["hp"]), "Wolf HP drift or reset")
        require(row["quest"] == (source["questStage"] if index < 4 else 1), "Wolf quest drift or reset")
        require(row["patrol"] == (source["patrolSteps"] if index < 7 else finished["patrolSteps"]), "Wolf patrol drift or reset")
        require(row["wolfViewBound"] == (row["chunk"] == 5), "Wolf projection was not bound in the correct chunk")
        if row["wolfViewBound"]:
            require((row["viewHp"], row["viewQuest"], row["viewPatrol"]) == (row["hp"], row["quest"], row["patrol"]),
                    "Bound wolf projection is stale")
        require(all(row[key] > 0 for key in ("privateBytes", "workingBytes", "peakPrivateBytes", "peakWorkingBytes")),
                "Invalid memory checkpoint")
        require(row["privateBytes"] <= row["peakPrivateBytes"] and row["workingBytes"] <= row["peakWorkingBytes"],
                "Current process memory exceeds OS-reported peak")
    require((checks[4]["instance"] != checks[8]["instance"]) == streamed, "Revisit used the wrong chunk instance")
    require(checks[5]["populationHash"] == checks[6]["populationHash"] != checks[7]["populationHash"],
            "Population changed during cleanup or failed to progress while absent")
    require(all("Chunk" + str(row["chunk"]) + "_LevelInstance" in row["instance"] for row in checks if row["chunk"] >= 0),
            "The scene transition used a wrong package")
    require(save == finished, "Scale save did not serialize the expected v2 state")

    steps = run["transitions"]
    require([row["name"] for row in steps] == list(TRANSITIONS), "Missing observed streaming activation")
    require([row["targetChunk"] for row in steps] == list(TRANSITION_CHUNKS), "Wrong transition targets")
    require(all(row["ms"] > 0 for row in steps), "Invalid transition clock")
    for row in steps:
        minimum = int(row["targetChunk"] >= 0) if streamed else 8
        maximum = 2 if streamed else 8
        require(minimum <= row["peakObservedLoadedChunks"] <= maximum, "Invalid transition residency")

    frames = run["frames"]
    for group, route, ms, work in frames:
        require(group in GROUPS and route in TRANSITIONS and math.isfinite(ms) and ms > 0 and work >= 0,
                "Invalid native frame row")
    for route in TRANSITIONS:
        samples = [row for row in frames if row[0] == "steady" and row[1] == route]
        require(len(samples) >= 5, f"Too few steady samples in {route}")
        expected = 0 if scheduled and route in ("preload", "returnTown") else 256 if scheduled else 2048
        require(all(row[3] == expected for row in samples), f"Wrong actual NPC work in {mode}/{route}")
    require(sum(row[0] == "cleanup" for row in frames) == 1, "Missing isolated GC sample")
    require(run["observations"] > 0, "No real observer work occurred")


def run_game(engine, directory, mode, fixture, slot):
    directory.mkdir()
    temp = directory / "temp"
    temp.mkdir()
    log = directory / "game.log"
    output = directory / "run.json"
    command = [str(engine / "Binaries/Win64/UnrealEditor.exe"), str(PROJECT), "/Game/Maps/Town", "-game",
               "-windowed", "-ResX=960", "-ResY=540", "-d3d11", "-unattended", "-nosplash", "-nop4",
               "-nosound", "-NoAnalytics", "-NoZenAutoLaunch", "-DDC=(InstalledEnginePak,InstalledLocal)",
               f"-LocalDataCachePath={ROOT / 'Scratch/DDC'}", "-ExecCmds=r.VSync 0,t.MaxFPS 0",
               f"-abslog={log}", f"-WorldScale={mode}", f"-LegacyFixture={fixture}",
               f"-ScaleOutput={output}", f"-ScaleSave={slot}"]
    with subprocess.Popen(command, cwd=ROOT, env=dict(os.environ, TEMP=str(temp), TMP=str(temp))) as child:
        try:
            exit_code = child.wait(timeout=120)
        except subprocess.TimeoutExpired:
            child.kill()
            raise
    require(exit_code == 0 and output.is_file() and log.is_file(), f"Unreal exit {exit_code}; inspect {directory}")
    result = json.loads(output.read_text(encoding="utf-8"))
    text = log.read_text(encoding="utf-8-sig", errors="replace")
    adapter = ADAPTER.search(text)
    version = re.search(r"LogInit: Engine Version: ([^\n]+)", text)
    host = re.search(r"LogInit: OS: ([^\n]+)", text)
    require(adapter and version and host and "session game=1 standalone=1 map=/Game/Maps/Town" in text,
            "Expected rendered standalone world on a real D3D11 device")
    require("r.VSync 0,t.MaxFPS 0" in text, "Missing explicit render and frame-cap settings")
    result.update(processId=child.pid, exitCode=exit_code, rhiAdapter=adapter[1].strip(),
                  engineVersion=version[1].strip(), host=host[1].strip(), command=command)
    return result


def check_oracle(run, source, saved):
    cases = {
        "wolf_reset": lambda data: data["checkpoints"][7].update(hp=100),
        "wrong_residency": lambda data: data["checkpoints"][5].update(residentChunks=4),
        "stale_active_views": lambda data: data["checkpoints"][7].update(activeViews=256),
        "patrol_duplicated": lambda data: data["checkpoints"][8].update(patrol=11),
        "missing_transition": lambda data: data["transitions"].pop(2),
        "false_work_count": lambda data: next(row for row in data["frames"] if row[0] == "steady").__setitem__(3, 511),
    }
    checked = {}
    for label, change in cases.items():
        bad = deepcopy(run)
        change(bad)
        try:
            verify(bad, run["mode"], source, saved)
        except ValueError as reason:
            checked[label] = str(reason)
        else:
            raise ValueError(f"Oracle accepted {label}")
    return checked


def summarize(run, raw, name):
    run["id"] = name
    frames = run.pop("frames")
    raw.append({"id": name, "mode": run["mode"], "frames": frames})
    run["stats"] = {group: measure([row[2] for row in frames if row[0] == group]) for group in GROUPS}
    run["steadyByRoute"] = {route: measure([row[2] for row in frames if row[:2] == ["steady", route]])
                             for route in TRANSITIONS}
    steady = [row for row in frames if row[0] == "steady"]
    run["steadyWorkPerFrame"] = sum(row[3] for row in steady) / len(steady)
    run["checkpointsMiB"] = {row["name"]: {name: row[name + "Bytes"] / 1048576
                            for name in ("private", "working", "peakWorking", "peakPrivate")}
                            for row in run["checkpoints"]}


def compatibility(engine, root, migrated_slot, migrated, raw):
    restore_from_v1 = run_game(engine, root / "reopen-v1-migration", "restore", migrated_slot, migrated_slot)
    verify(restore_from_v1, "restore", migrated)
    old_v2 = json.loads(LEGACY_V2.read_text(encoding="utf-8-sig"))
    v2_slot = root / "v2-slot.json"
    v2_run = run_game(engine, root / "prechange-v2", "streamed-scheduled", LEGACY_V2, v2_slot)
    new_v2 = json.loads(v2_slot.read_text(encoding="utf-8-sig"))
    verify(v2_run, "streamed-scheduled", old_v2, new_v2)
    summarize(v2_run, raw, "prechange-v2")
    restore_from_v2 = run_game(engine, root / "reopen-v2", "restore", v2_slot, v2_slot)
    verify(restore_from_v2, "restore", new_v2)
    return [restore_from_v1, v2_run, restore_from_v2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--engine", type=Path, default=INSTALL)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--name", default="scale-rerun")
    ap.add_argument("--mode", choices=MODES, help="Isolate a single configuration for a smoke run")
    ap.add_argument("--skip-compat", action="store_true", help="Skip post-matrix compatibility launches for a smoke run")
    ap.add_argument("--compat-from", help="Run compatibility alone using a completed Scratch matrix name")
    args = ap.parse_args()
    require(args.rounds > 0 and re.fullmatch(r"[\w-]+", args.name), "Invalid run options")
    root = ROOT / "Scratch" / args.name
    root.mkdir(parents=True)
    engine = args.engine / "Engine"
    raw = []
    inputs = [LEGACY, LEGACY_V2]
    fixtures_before = {path.name: digest(path) for path in inputs}
    source = json.loads(LEGACY.read_text(encoding="utf-8-sig"))
    maps = sorted((ROOT / "Content/Maps/Scale").glob("Chunk*.umap"))
    require(len(maps) == 8, "Expected eight independently authored chunk packages")
    report = {"engine": "Unreal", "renderer": "D3D11", "resolution": [960, 540], "fixturesBefore": fixtures_before,
              "moduleSha256": digest(ROOT / "Binaries/Win64/UnrealEditor-WorldLifecycle.dll"),
              "chunks": {path.name: {"bytes": path.stat().st_size, "sha256": digest(path)} for path in maps},
              "runs": [], "compatibility": [], "controls": {}, "modeMedians": {}}
    signature = None
    for index in range(0 if args.compat_from else args.rounds):
        modes = (args.mode,) if args.mode else ORDERS[index % len(ORDERS)]
        for mode in modes:
            name = f"round-{index + 1}-{mode}"
            slot = root / f"{name}.json"
            run = run_game(engine, root / name, mode, LEGACY, slot)
            last_save = json.loads(slot.read_text(encoding="utf-8-sig"))
            verify(run, mode, source, last_save)
            if signature is None:
                report["controls"] = check_oracle(run, source, last_save)
            observed = [(row["populationHash"], row["viewHash"]) for row in run["checkpoints"]]
            require(signature is None or observed == signature, "Unequal population or rendered actor poses at matched checkpoints")
            signature = observed
            summarize(run, raw, name)
            report["runs"].append(run)
            print(f"{name}: validated; steady P95={run['stats']['steady']['p95']:.3f} ms", flush=True)

    if args.compat_from:
        require(not args.skip_compat and not args.mode and re.fullmatch(r"[\w-]+", args.compat_from), "Invalid compatibility input")
        previous = ROOT / "Scratch" / args.compat_from
        archive = json.loads((previous / "scale-summary.json").read_text(encoding="utf-8"))
        require(archive["runs"] and archive["fixturesBefore"] == fixtures_before and
                archive["moduleSha256"] == report["moduleSha256"] and archive["chunks"] == report["chunks"],
                "Post-matrix compatibility requires the same build and unchanged fixtures")
        slot = previous / f"{archive['runs'][-1]['id']}.json"
        last_save = json.loads(slot.read_text(encoding="utf-8-sig"))
        require(last_save == payload(source), "Matrix slot does not match the verified v1 migration")
        report["compatibilityFrom"] = args.compat_from
    if not args.skip_compat:
        report["compatibility"] = compatibility(engine, root, slot, last_save, raw)

    report["fixturesAfter"] = {path.name: digest(path) for path in inputs}
    require(report["fixturesAfter"] == fixtures_before, "Pre-change artifact bytes changed")
    processes = [run["processId"] for run in report["runs"] + report["compatibility"]]
    require(len(set(processes)) == len(processes), "Expected distinct operating system processes")
    for mode in MODES:
        runs = [run for run in report["runs"] if run["mode"] == mode]
        if runs:
            report["modeMedians"][mode] = {
                "processes": len(runs),
                "wallMs": {group: {key: median(run["stats"][group][key] for run in runs)
                           for key in ("n", "p50", "p95", "p99", "max")} for group in GROUPS},
                "transitionMs": {name: median(next(row["ms"] for row in run["transitions"] if row["name"] == name)
                                 for run in runs) for name in TRANSITIONS},
                "checkpointsMiB": {name: {key: median(run["checkpointsMiB"][name][key] for run in runs)
                                   for key in ("private", "working", "peakWorking", "peakPrivate")} for name in CHECKPOINTS},
                "steadyWorkPerFrame": median(run["steadyWorkPerFrame"] for run in runs),
            }
    write_json(root / "scale-summary.json", report)
    with (root / "scale-frames.json.gz").open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as zipped:
            zipped.write(json.dumps({"columns": ["phase", "route", "wallMs", "npcEvaluations"], "runs": raw},
                         separators=(",", ":")).encode("utf-8"))
    print(f"Verified {len(report['runs'])} measured runs and {len(report['compatibility'])} compatibility processes in {root}")


if __name__ == "__main__":
    main()
