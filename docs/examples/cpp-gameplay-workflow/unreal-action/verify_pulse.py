"""Stage physical encounter inventories and verify played Unreal game worlds."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent
ENGINE = Path(r"C:\Program Files\Epic Games\UE_5.8")
PROJECT = "PulseArena.uproject"
EXPECTED = {"practice": (0.5, 2), "A": (0.75, 4), "B": (0.95, 7)}
CONFIGURATIONS = {"core": (), "a-only": ("A",), "b-only": ("B",), "both": ("A", "B")}
PULSE = re.compile(r"Pulse id=(\S+) accepted=([01]) time=([\d.]+) ready=([\d.]+) score=(\d+)")


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def fingerprint(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def snapshot():
    files = [ROOT / PROJECT, Path(__file__).resolve()]
    for directory in ("Config", "Content", "Source"):
        files.extend(path for path in (ROOT / directory).rglob("*") if path.is_file())
    return {path.relative_to(ROOT).as_posix(): fingerprint(path) for path in sorted(files)}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def verify_world(log, directory, packs):
    expected_ids = ("practice", *packs)
    require(re.search(r"Session game=1 local=1 net=0 map=(?:/Engine/Maps/)?Entry\s*$", log, re.M),
            "Expected a standalone local game world in Engine Entry")
    catalog = re.search(r"Catalog path=(.+)$", log, re.M)
    require(catalog and Path(catalog[1].strip()).resolve() == directory.resolve(),
            "Game read a different encounter directory")
    registrations = re.findall(
        r"Registered id=(\S+) cooldown=([\d.]+) targets=(\d+) source=(\S+)", log
    )
    expected_registrations = [
        (key, f"{EXPECTED[key][0]:.3f}", str(EXPECTED[key][1]), "builtin" if i == 0 else f"{key}.json")
        for i, key in enumerate(expected_ids)
    ]
    require(registrations == expected_registrations, f"Unexpected registrations {registrations}")
    require(re.findall(r"Selected id=(\S+)", log) == list(packs), "Tab did not visit authored encounters in order")
    require("Skipped invalid encounter" not in log, "Fixture supplied invalid authored content")
    pulses = PULSE.findall(log)
    require([event[0] for event in pulses] == [key for key in expected_ids for _ in range(3)],
            f"Unexpected pulse order {pulses}")
    results = {}
    for i, key in enumerate(expected_ids):
        cooldown, targets = EXPECTED[key]
        events = [
            {"accepted": accepted == "1", "worldTime": float(world_time),
             "nextReady": float(ready), "score": int(score)}
            for _, accepted, world_time, ready, score in pulses[3 * i:3 * i + 3]
        ]
        first, early, late = events
        require([event["accepted"] for event in events] == [True, False, True], f"{key} pulse outcomes {events}")
        require([event["score"] for event in events] == [targets, targets, targets * 2], f"{key} score mutations")
        first_interval = early["worldTime"] - first["worldTime"]
        last_interval = late["worldTime"] - first["worldTime"]
        require(0.08 <= first_interval < cooldown <= last_interval, f"{key} wrong time-window samples {events}")
        require(abs(first["nextReady"] - (first["worldTime"] + cooldown)) < 0.00001
                and first["nextReady"] == early["nextReady"]
                and abs(late["nextReady"] - (late["worldTime"] + cooldown)) < 0.00001,
                f"{key} wrong deadlines {events}")
        results[key] = events
    require("Probe complete" in log, "Scripted player did not finish")
    require(f"EndPlay encounters={len(expected_ids)} pending=0" in log, "Missing controller cleanup")
    return results


def play(engine, output, packs):
    stage = output / "Project"
    destination = stage / "Content" / "Encounters"
    destination.mkdir(parents=True)
    shutil.copy2(ROOT / PROJECT, stage)
    shutil.copytree(ROOT / "Config", stage / "Config")
    binaries = stage / "Binaries" / "Win64"
    binaries.mkdir(parents=True)
    for path in (ROOT / "Binaries" / "Win64").iterdir():
        if path.suffix in (".dll", ".modules", ".target"):
            shutil.copy2(path, binaries)
    binary = binaries / "UnrealEditor-PulseArena.dll"
    require(binary.is_file(), "Build the Win64 Development PulseArenaEditor target first")
    for pack in packs:
        shutil.copy2(ROOT / "Content" / "Encounters" / f"{pack}.json", destination)
    files = sorted(path.name for path in destination.iterdir())
    require(files == [f"{pack}.json" for pack in packs], f"Unexpected staged files {files}")
    log_path = output / "game.log"
    command = [
        str(engine / "Engine" / "Binaries" / "Win64" / "UnrealEditor.exe"),
        str(stage / PROJECT), "/Engine/Maps/Entry", "-game", "-nullrhi", "-unattended", "-nosplash",
        "-nop4", "-nosound", "-DDC=(InstalledEnginePak,InstalledLocal)", "-NoZenAutoLaunch",
        f"-LocalDataCachePath={ROOT / 'Scratch' / 'DDC'}", "-NoAnalytics", "-log", f"-abslog={log_path}",
        "-ExecCmds=t.MaxFPS 60", "-PulseSmoke",
    ]
    scratch = stage / "Temp"
    scratch.mkdir()
    environment = dict(os.environ, TEMP=str(scratch), TMP=str(scratch))
    info = {"command": command, "contentDirectory": str(destination),
            "inventory": {name: fingerprint(destination / name) for name in files},
            "gameModuleSha256": fingerprint(binary), "tempDirectory": str(scratch)}
    evidence_path = output / "result.json"
    write_json(evidence_path, info)
    result = subprocess.run(command, cwd=stage, env=environment, timeout=90,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    info["exitCode"] = result.returncode
    write_json(evidence_path, info)
    require(result.returncode == 0 and log_path.is_file(), f"Game failed to produce evidence in {output}")
    info["pulses"] = verify_world(log_path.read_text(encoding="utf-8-sig", errors="replace"), destination, packs)
    write_json(evidence_path, info)
    print(f"{output.name}: {' '.join(info['pulses'])} passed", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("baseline", "matrix"))
    parser.add_argument("--engine", type=Path, default=ENGINE)
    parser.add_argument("--name", default=None, help="Fresh evidence directory name")
    parser.add_argument("--baseline", default="baseline", help="Baseline evidence directory named for the matrix comparison")
    args = parser.parse_args()
    name = args.name or args.phase
    require(bool(re.fullmatch(r"[\w-]+", name)) and bool(re.fullmatch(r"[\w-]+", args.baseline)),
            "Evidence directory names must contain only letters, digits, underscores or hyphens")
    output = ROOT / "Evidence" / name
    source = snapshot()
    if args.phase == "baseline":
        require("Content/Encounters/A.json" in source and "Content/Encounters/B.json" not in source,
                "The baseline must precede creation of B")
        output.mkdir(parents=True)
        write_json(output / "source.json", source)
        play(args.engine.resolve(), output / "a-only", ("A",))
        return

    baseline = ROOT / "Evidence" / args.baseline
    before = json.loads((baseline / "source.json").read_text(encoding="utf-8"))
    require("pulses" in json.loads((baseline / "a-only" / "result.json").read_text(encoding="utf-8")),
            "Build and play the A baseline before extending")
    changes = {name: {"before": before.get(name), "after": source.get(name)}
               for name in sorted(set(before) | set(source)) if before.get(name) != source.get(name)}
    require(set(changes) == {"Content/Encounters/B.json"}
            and changes["Content/Encounters/B.json"]["before"] is None,
            f"The authored extension changed gameplay files besides a new B.json: {changes}")
    output.mkdir(parents=True)
    write_json(output / "extension.json", changes)
    for configuration, packs in CONFIGURATIONS.items():
        play(args.engine.resolve(), output / configuration, packs)


if __name__ == "__main__":
    main()
