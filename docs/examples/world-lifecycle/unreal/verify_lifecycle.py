"""Run fresh Unreal processes and verify the observed town/forest lifecycle."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
INSTALL = Path(r"C:\Program Files\Epic Games\UE_5.8")
LEGACY = ROOT.parent / "fixtures" / "legacy-v1.json"
PROJECT = ROOT / "WorldLifecycle.uproject"
CANONICAL = "forest-wolf-v2"


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def digest(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def events_from(log):
    events = []
    for line in log.splitlines():
        found = re.search(r"\bLogWorldLifecycle: Display: ([a-z-]+)(.*)$", line)
        if found:
            fields = dict(token.split("=", 1) for token in found[2].split())
            fields["event"] = found[1]
            events.append(fields)
    return events


def verify(events, mode, persisted=None):
    names = [entry["event"] for entry in events]
    session = events[0] if events else {}
    require(session.get("event") == "session" and session.get("game") == "1"
            and session.get("standalone") == "1" and session.get("map") == "/Game/Maps/Town",
            "Expected a standalone game world in the town map")
    require(names[-2:] == ["complete", "end"], "Probe did not finish cleanly")
    if mode == "lifecycle":
        require(names == ["session", "restore", "request", "visible", "hit", "request-out",
                          "unloaded", "patrol", "request", "visible", "save", "rejected", "complete", "end"],
                f"Unexpected lifecycle {names}")
        restored, first, hit = events[1], events[3], events[4]
        unloaded, patrol, revisit, saved, rejected = events[6], events[7], events[9], events[10], events[11]
        require(all(entry["npc"] == CANONICAL for entry in
                    (restored, first, hit, unloaded, patrol, revisit, saved, rejected)),
                "Logical NPC identity changed during the journey")
        require(restored["schema"] == "1" and restored["npc"] == CANONICAL
                and (restored["hp"], restored["quest"], restored["patrol"]) == ("100", "0", "0"),
                "Legacy fixture failed to migrate")
        require((first["hp"], first["quest"], first["patrol"]) == ("100", "0", "0"), "Wrong initial projection")
        require(all((entry["hp"], entry["quest"]) == ("60", "1") for entry in
                    (hit, unloaded, patrol, revisit, saved, rejected)),
                "Combat or offscreen authority failed to preserve HP and quest state")
        require(unloaded["registered"] == unloaded["loaded"] == unloaded["presentation"] == "0",
                "Forest held a streaming registration, loaded level or present actor after return")
        require(patrol["loaded"] == patrol["presentation"] == "0"
                and float(patrol["worldSeconds"]) - float(unloaded["worldSeconds"]) >= 0.24
                and (hit["patrol"], unloaded["patrol"], patrol["patrol"]) == ("0", "0", "1"),
                "Expected one world-clock patrol increment while absent")
        require((revisit["hp"], revisit["quest"], revisit["patrol"]) == ("60", "1", patrol["patrol"]),
                "Revisited actor did not rehydrate")
        require(first["instance"] != revisit["instance"], "Revisit reused a level instance")
        for index, entry in enumerate((first, revisit), start=1):
            request = events[2] if index == 1 else events[8]
            require(int(request["visit"]) == index and request["package"] == "/Game/Maps/Forest"
                    and request["blocking"] == "0", "Expected a nonblocking forest package request")
            require(int(entry["visit"]) == index and entry["loaded"] == entry["visible"] == "1"
                    and entry["presentation"] == "1" and int(entry["actors"]) >= 99
                    and (entry["viewHp"], entry["viewQuest"], entry["viewPatrol"]) ==
                        (entry["hp"], entry["quest"], entry["patrol"]),
                    "A real streamed level and rehydrated actor were expected")
            require(float(entry["latencyMs"]) > 0 and float(entry["maxTickGapMs"]) > 0
                    and int(entry["tickGaps"]) >= 1, "Missing stream timing observations")
        require(rejected["reason"] == "unsupported-schema" and rejected["hp"] == saved["hp"]
                and rejected["quest"] == saved["quest"] and rejected["patrol"] == saved["patrol"],
                "A rejected read changed the active state")
        return {"schemaVersion": 2, "npcId": CANONICAL, "hp": 60,
                "questStage": 1, "patrolSteps": int(patrol["patrol"])}
    require(names == ["session", "restore", "request", "visible", "complete", "end"],
            f"Unexpected fresh restore lifecycle {names}")
    restored, visible = events[1], events[3]
    for entry in (restored, visible):
        require((entry["npc"], int(entry["hp"]), int(entry["quest"]), int(entry["patrol"])) ==
                (CANONICAL, persisted["hp"], persisted["questStage"], persisted["patrolSteps"]),
                "Fresh process lost saved gameplay state")
    require(restored["schema"] == "2" and (visible["viewHp"], visible["viewQuest"], visible["viewPatrol"]) ==
            (visible["hp"], visible["quest"], visible["patrol"]), "Fresh v2 load did not project NPC state")


def play(engine, out, mode, save, unsupported, renderer):
    out.mkdir()
    temp = out / "temp"
    temp.mkdir()
    log = out / "game.log"
    command = [str(engine / "Binaries" / "Win64" / "UnrealEditor.exe"), str(PROJECT),
               "/Game/Maps/Town", "-game", "-windowed", "-ResX=960", "-ResY=540", "-unattended",
               "-nosplash", "-nop4", "-nosound", "-NoAnalytics", "-NoZenAutoLaunch",
               "-DDC=(InstalledEnginePak,InstalledLocal)", f"-LocalDataCachePath={ROOT / 'Scratch' / 'DDC'}",
               f"-abslog={log}", "-ExecCmds=t.MaxFPS 0", f"-WorldProbe={mode}",
               f"-WorldSave={save}", f"-LegacyFixture={LEGACY}", f"-RejectedFixture={unsupported}",
               f"-{renderer}"]
    env = dict(os.environ, TMP=str(temp), TEMP=str(temp))
    with subprocess.Popen(command, env=env, cwd=ROOT) as child:
        try:
            exit_code = child.wait(timeout=120)
        except subprocess.TimeoutExpired:
            child.kill()
            raise
    require(exit_code == 0 and log.is_file(), f"Unreal exit {exit_code}; inspect {log}")
    content = log.read_text(encoding="utf-8-sig", errors="replace")
    runtime = next((line.split("Engine Version:", 1)[1].strip() for line in content.splitlines()
                    if "LogInit: Engine Version:" in line), None)
    require(runtime, "Unreal runtime version missing")
    host = next((line.split("LogInit: OS: ", 1)[1] for line in content.splitlines() if "LogInit: OS: " in line), None)
    adapter = re.search(r"LogD3D11RHI: Creating D3DDevice using adapter:\n[^\n]*Description\s*:\s*([^\n]+)", content)
    require(renderer != "d3d11" or adapter, "D3D11 device creation was not observed")
    return {"exitCode": exit_code, "processId": child.pid, "engineVersion": runtime,
            "host": host, "d3d11Adapter": adapter[1].strip() if adapter else None,
            "command": command, "events": events_from(content)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, default=INSTALL)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--renderer", choices=("nullrhi", "d3d11"), default="nullrhi")
    parser.add_argument("--name", default="verify", help="Fresh Scratch directory name")
    args = parser.parse_args()
    require(re.fullmatch(r"[\w-]+", args.name) and args.runs > 0, "Invalid run options")
    engine = args.engine / "Engine"
    out = ROOT / "Scratch" / args.name
    out.mkdir(parents=True)
    unsupported = out / "unsupported.json"
    invalid = json.loads(LEGACY.read_text(encoding="utf-8"))
    invalid["schemaVersion"] = 99
    unsupported.write_text(json.dumps(invalid), encoding="utf-8")
    binary = ROOT / "Binaries" / "Win64" / "UnrealEditor-WorldLifecycle.dll"
    legacy_sha_before = digest(LEGACY)
    summary = {"rendererArgument": args.renderer, "runs": [], "inputsSha256": {
        "legacy-v1.json": legacy_sha_before, "Town.umap": digest(ROOT / "Content" / "Maps" / "Town.umap"),
        "Forest.umap": digest(ROOT / "Content" / "Maps" / "Forest.umap"), "module": digest(binary)}}
    for number in range(1, args.runs + 1):
        slot = out / f"run-{number}-save-v2.json"
        run = play(engine, out / f"run-{number}", "lifecycle", slot, unsupported, args.renderer)
        expected = verify(run["events"], "lifecycle")
        persisted = json.loads(slot.read_text(encoding="utf-8-sig"))
        require(persisted == expected, f"Wrong canonical disk save {persisted}")
        run["savedV2"] = persisted
        summary["runs"].append(run)
        print(f"Lifecycle process {number} passed", flush=True)
    restart = play(engine, out / "restart", "restore", slot, unsupported, args.renderer)
    verify(restart["events"], "restore", persisted)
    summary["restart"] = restart
    summary["legacyV1Sha256After"] = digest(LEGACY)
    require(summary["legacyV1Sha256After"] == legacy_sha_before, "Legacy fixture bytes changed")
    result = out / "result.json"
    result.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Fresh v2 restart passed; {result}", flush=True)


if __name__ == "__main__":
    main()
