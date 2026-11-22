import argparse
import gzip
import hashlib
import json
import math
import statistics
from pathlib import Path

parser = argparse.ArgumentParser(description="Verify the four-round Unity Player matrix and preserve its raw samples.")
parser.add_argument("source", type=Path, help="Work/scale-* directory reported by Run-Scale.ps1")
parser.add_argument("out", type=Path, help="Destination for the summary and compressed raw reports")
options = parser.parse_args()
files = sorted(path for path in options.source.glob("*.json") if not path.name.endswith(".save.json"))
records = [(path, json.loads(path.read_text(encoding="utf-8-sig"))) for path in files]
ordered = sorted(records, key=lambda record: record[1]["utc"])
modes = ["resident-full", "stream-full", "resident-coarse", "stream-coarse"]
assert len(ordered) == 16, len(ordered)
assert len({entry["pid"] for _, entry in ordered}) == 16
assert [entry["mode"] for _, entry in ordered] == [
    "resident-full", "stream-full", "stream-coarse", "resident-coarse",
    "stream-full", "resident-coarse", "resident-full", "stream-coarse",
    "resident-coarse", "stream-coarse", "stream-full", "resident-full",
    "stream-coarse", "resident-full", "resident-coarse", "stream-full",
]
anchors = {}
run_summaries = []
workload = {"logicalNpcs": 2048, "forestChunks": 8, "objectsPerChunk": 700, "visibleBindings": 256, "ticks": 552}
phases = ["preload", "transition", "steady"]
frame_budget = 1000 / 60
stages = ["townBefore", "chunk0", "chunk2", "chunk5", "townAfterUnload", "revisited5"]

def quantiles(values):
    ordered_values = sorted(values)

    def rank(fraction):
        return ordered_values[math.ceil(len(ordered_values) * fraction) - 1]

    return {"count": len(values), "p50": rank(.5), "p95": rank(.95), "p99": rank(.99),
            "max": ordered_values[-1], "over16_67Ms": sum(value > frame_budget for value in values)}

for path, run in ordered:
    round_num = int(path.name.split("-")[0])
    fixture = 1 if round_num in (1, 3) else 2
    stream = run["mode"].startswith("stream-")
    coarse = run["mode"].endswith("-coarse")
    assert run["passed"] and run["engine"] == "6000.0.77f1"
    assert run["fixtureVersion"] == fixture and run["fixture"] == f"legacy-v{fixture}.json"
    assert run["graphicsApi"] == "Direct3D11" and not run["batchMode"]
    assert (run["width"], run["height"], run["vSync"], run["targetFrameRate"]) == (1280, 720, 0, -1)
    assert (run["logicalNpcs"], run["ticks"], run["geometryObjectsPerChunk"]) == (2048, 552, 700)
    assert (run["loads"], run["unloads"], run["finalLoadedChunks"], run["peakLoadedChunks"]) == ((4, 3, 1, 2) if stream else (8, 0, 8, 8))
    assert (run["npcUpdates"], run["otherNpcUpdates"]) == ((184320, 86016) if coarse else (1130496, 1032192))
    for key in ("inputUnchanged", "invalidCandidatesRejected", "wolfRoundTrip"):
        assert run[key]
    assert run["originalTargetViewDestroyed"] == stream
    samples = run["frameSamples"]
    assert abs(run["renderedFrames"] - len(samples)) <= 1
    assert run["nonBackgroundPixels"] >= 10000
    assert all(row["phase"] in phases and row["milliseconds"] > 0 for row in samples)
    checks = {row["stage"]: row for row in run["checkpoints"]}
    assert list(checks) == ["initial", "townBefore", "chunk0", "chunk2", "chunk5", "combat", "townArrival", "townAfterUnload", "revisited5"]
    assert [row["tick"] for row in checks.values()] == [0, 72, 168, 264, 360, 360, 384, 456, 552]
    for row in checks.values():
        visible = row["currentChunk"] >= 0
        assert row["boundViews"] == (256 if visible else 0)
        assert row["loadedChunks"] == (int(visible) if stream else 8)
        assert row["npcs"][1]["id"] == 1297
    assert checks["combat"]["wolfHp"] == (60 if fixture == 1 else 20)
    assert checks["initial"]["wolfPatrol"] == fixture - 1
    assert checks["townArrival"]["targetViewId"] == checks["townAfterUnload"]["targetViewId"] == 0
    assert (checks["combat"]["targetViewId"] != checks["revisited5"]["targetViewId"]) == stream
    combat, town_arrival, town_after, revisited = [checks[key]["npcs"][1] for key in ("combat", "townArrival", "townAfterUnload", "revisited5")]
    assert combat["hp"] == town_arrival["hp"] == town_after["hp"] == revisited["hp"] == 65
    assert (combat["patrolSteps"], town_arrival["patrolSteps"], town_after["patrolSteps"], revisited["patrolSteps"]) == (60, 64, 76, 92)
    saved = json.loads(run["savedJson"])
    assert saved == {"schemaVersion": 2, "npcId": "forest-wolf-v2", "hp": (60 if fixture == 1 else 20), "questStage": 1, "patrolSteps": 13 + fixture}
    trace = [(row["tick"], row["npcDigest"], row["npcs"], row["wolfHp"], row["wolfQuest"], row["wolfPatrol"]) for row in checks.values()]
    assert anchors.setdefault(fixture, trace) == trace
    timings = {phase: quantiles([row["milliseconds"] for row in samples if row["phase"] == phase]) for phase in phases}
    timings["all"] = quantiles([row["milliseconds"] for row in samples])
    timings["steadyByStage"] = {stage: quantiles([row["milliseconds"] for row in samples if row["phase"] == "steady" and row["stage"] == stage]) for stage in stages}
    assert all(result["count"] == 72 for result in timings["steadyByStage"].values())
    memory = run["memorySamples"]
    assert len(memory) > 30 and all(row["privateBytes"] > 0 and row["workingSetBytes"] > 0 for row in memory)
    assert all(a["elapsedMs"] < b["elapsedMs"] for a, b in zip(memory, memory[1:]))
    by_stage = {row["stage"]: row for row in memory}
    assert by_stage["townAfterUnload"]["tick"] == 456
    memory_metrics = {
        "beforePreloadPrivateBytes": by_stage["beforePreload"]["privateBytes"],
        "afterPreloadPrivateBytes": by_stage["afterPreload"]["privateBytes"],
        "preloadElapsedMs": by_stage["afterPreload"]["elapsedMs"],
        "townAfterUnloadPrivateBytes": by_stage["townAfterUnload"]["privateBytes"],
        "townAfterUnloadWorkingSetBytes": by_stage["townAfterUnload"]["workingSetBytes"],
        "sampledPeakPrivateBytes": max(row["privateBytes"] for row in memory),
        "sampledPeakWorkingSetBytes": max(row["workingSetBytes"] for row in memory),
    }
    run_summaries.append({
        "round": round_num, "mode": run["mode"], "pid": run["pid"], "fixtureVersion": fixture,
        "npcUpdates": run["npcUpdates"], "offscreenNpcUpdates": run["otherNpcUpdates"],
        "loads": run["loads"], "unloads": run["unloads"], "finalLoadedChunks": run["finalLoadedChunks"], "peakLoadedChunks": run["peakLoadedChunks"],
        "timingsMs": timings, "memory": memory_metrics, "transitions": run["transitions"],
    })

# Each tuple starts with the tick, population digest, and selected NPC snapshots.
assert [trace[:3] for trace in anchors[1]] == [trace[:3] for trace in anchors[2]]

arms = {}
for mode in modes:
    runs = [run for run in run_summaries if run["mode"] == mode]
    timing_summary = {}
    for phase in ["all", "preload", "transition", "steady"]:
        timing_summary[phase] = {metric: statistics.median(item["timingsMs"][phase][metric] for item in runs)
                                 for metric in ("p50", "p95", "p99", "max", "count", "over16_67Ms")}
    timing_summary["steadyByStage"] = {
        stage: {metric: statistics.median(item["timingsMs"]["steadyByStage"][stage][metric] for item in runs)
                for metric in ("p50", "p95", "p99", "max", "over16_67Ms")} for stage in stages
    }
    memory_summary = {key: statistics.median(run["memory"][key] for run in runs) for key in runs[0]["memory"]}
    transition_summary = {row["stage"]: statistics.median(run["transitions"][i]["requestToReadyMs"] for run in runs)
                          for i, row in enumerate(runs[0]["transitions"])}
    arms[mode] = {"runCount": len(runs), "medianRunFrameTimingsMs": timing_summary, "medianRunMemory": memory_summary,
                  "medianTransitionReadyMs": transition_summary, "npcUpdates": runs[0]["npcUpdates"],
                  "offscreenNpcUpdates": runs[0]["offscreenNpcUpdates"]}

metadata = {
    "engine": "Unity 6000.0.77f1",
    "binary": "StandaloneWindows64 Mono",
    "rendering": "Direct3D11, 1280x720 offscreen RenderTexture from a manually rendered camera",
    "gpu": ordered[0][1]["graphics"], "cpu": ordered[0][1]["cpu"], "os": ordered[0][1]["os"],
    "command": ".\\Run-Scale.ps1",
    "percentile": "nearest rank per run; condition value is the median of four run statistics",
    "workload": workload,
    "assemblySha256": hashlib.sha256(Path("Build/WorldLifecycle_Data/Managed/Assembly-CSharp.dll").read_bytes()).hexdigest(),
    "sourceFixtureV1Sha256": hashlib.sha256(Path("../fixtures/legacy-v1.json").read_bytes()).hexdigest(),
    "sourceFixtureV2Sha256": hashlib.sha256(Path("../fixtures/legacy-v2.json").read_bytes()).hexdigest(),
    "packagedSceneSha256": {
        f"level{level}": hashlib.sha256(Path(f"Build/WorldLifecycle_Data/level{level}").read_bytes()).hexdigest()
        for level in range(2, 10)
    },
    "red": "NPC 0 must advance on ticks 5,10,15,20,25 even while absent.",
    "green": "Independent save and NPC schedule check passed; large Player matrix passed.",
}
options.out.mkdir(parents=True, exist_ok=True)
(options.out / "summary.json").write_text(json.dumps({"metadata": metadata, "arms": arms, "runs": run_summaries}, indent=2) + "\n", encoding="utf-8")
with (options.out / "raw.json.gz").open("wb") as outfile:
    with gzip.GzipFile(fileobj=outfile, mode="wb", filename="", mtime=0) as compressed:
        compressed.write((json.dumps({"runs": [run for _, run in ordered]}, separators=(",", ":")) + "\n").encode())
print(json.dumps({key: {"steady": data["medianRunFrameTimingsMs"]["steady"], "transition": data["medianRunFrameTimingsMs"]["transition"], "memory": data["medianRunMemory"]} for key, data in arms.items()}, indent=2))
