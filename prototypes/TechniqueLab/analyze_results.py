"""Validate final engine evidence and summarize three independent player runs.

Run from any directory with Python 3.9+. Historical red/pilot files are not inputs.
"""
import hashlib
import json
import math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "Results"


def read(name):
    return json.loads((RESULTS / name).read_text(encoding="utf-8-sig"))


def validate(report):
    assert report["schemaVersion"] == 2 and report["finished"]
    assert report["phase"] == "finished" and report["failures"] == 0
    assert report["playing"] and len(report["checks"]) == 27
    assert all(c["passed"] for c in report["checks"])
    assert len({c["name"] for c in report["checks"]}) == 27
    assert len(report["frameResponses"]) == 3
    for response in report["frameResponses"]:
        assert response["frames"] == len(response["deltaSeconds"])
        assert abs(sum(response["deltaSeconds"]) - 2) < 0.00001
        assert response["absoluteError"] <= 0.0001
        assert abs(abs(response["exponentialFinal"] - response["expected"])
                   - response["absoluteError"]) < 0.000002
    assert len(report["benchmarks"]) == 30
    for row in report["benchmarks"]:
        raw, norm = row["rawTimedBatchMs"], row["normalizedMsPerInvocation"]
        repeats = row["invocationsPerSample"]
        assert len(raw) == len(norm) == row["samples"] == 31
        assert row["totalWorkPerSample"] == row["workPerInvocation"] * repeats
        assert row["stopwatchFrequency"] > 0
        assert all(math.isfinite(t) and t > 0 for t in raw)
        assert all(abs(a / repeats - b) < 1e-10 for a, b in zip(raw, norm))
        assert abs(median(norm) - row["medianMsPerInvocation"]) < 1e-10
        assert abs(sorted(norm)[math.ceil(len(norm) * .95) - 1]
                   - row["p95MsPerInvocation"]) < 1e-10
        if row["name"].startswith("shot."):
            calls = row["queriesPerSample"] / row["totalWorkPerSample"]
            expected = (1 if row["name"] == "shot.camera-only" else
                        2 if "cover=2," in row["group"] else 5)
            assert calls == expected, (row["group"], calls)
    for count in (32, 128, 512):
        rows = [b for b in report["benchmarks"]
                if b["name"].startswith("path.") and b["workPerInvocation"] == count]
        assert len({b["checksum"] for b in rows}) == 1, "Unequal distance answers"


def main():
    editor = read("editor-play-final.json")
    validate(editor)
    assert editor["editor"]
    build = read("build.json")
    assert build["result"] == "Succeeded" and build["errors"] == 0
    reports, manifests = [], []
    for number in range(1, 4):
        report = read(f"player-run-{number}.json")
        manifest = read(f"player-run-{number}-process.json")
        validate(report)
        assert not report["editor"] and report["mode"] == "Windows standalone"
        assert manifest["exitCode"] == 0 and not manifest["interactive"]
        for relative, digest in manifest["sourceSha256"].items():
            assert hashlib.sha256((ROOT / relative.replace("\\", "/")).read_bytes()).hexdigest().upper() == digest
        reports.append(report)
        manifests.append(manifest)
    assert len({r["buildGuid"] for r in reports}) == 1
    assert len({m["playerSha256"] for m in manifests}) == 1
    assert all(manifests[i]["utcEnd"] <= manifests[i + 1]["utcStart"] for i in range(2))
    player = ROOT / "Build/TechniqueLab.exe"
    if player.exists():
        assert hashlib.sha256(player.read_bytes()).hexdigest().upper() == manifests[0]["playerSha256"]
    assert read("green-error-sentinel.json")["failures"] == 1
    assert read("red-error-sentinel.json")["failures"] == 0
    summary = {"sessions": 3, "checksPerSession": 27, "seriesPerSession": 30,
               "buildGuid": reports[0]["buildGuid"], "playerSha256": manifests[0]["playerSha256"],
               "environment": {k: reports[0][k] for k in
                               ("unity", "os", "cpu", "processors", "memoryMB", "gpu", "graphicsApi")},
               "frames": [], "benchmarks": []}
    for cap in (30, 60, 144):
        frames = [next(f for f in r["frameResponses"] if f["requestedFPS"] == cap) for r in reports]
        summary["frames"].append({"requestedFPS": cap,
            "measuredFPS": [f["measuredFPS"] for f in frames],
            "naiveFinal": [f["naiveFinal"] for f in frames],
            "exponentialFinal": [f["exponentialFinal"] for f in frames],
            "maxAbsoluteError": max(f["absoluteError"] for f in frames)})
    for index, first in enumerate(reports[0]["benchmarks"]):
        rows = [r["benchmarks"][index] for r in reports]
        assert all((r["name"], r["group"], r["workPerInvocation"]) ==
                   (first["name"], first["group"], first["workPerInvocation"]) for r in rows)
        summary["benchmarks"].append({"name": first["name"], "group": first["group"],
            "workPerInvocation": first["workPerInvocation"],
            "medianRangeMs": [min(r["medianMsPerInvocation"] for r in rows), max(r["medianMsPerInvocation"] for r in rows)],
            "p95RangeMs": [min(r["p95MsPerInvocation"] for r in rows), max(r["p95MsPerInvocation"] for r in rows)],
            "rawTimedBatchMinimumMs": min(min(r["rawTimedBatchMs"]) for r in rows),
            "invocationsPerSample": [r["invocationsPerSample"] for r in rows],
            "nativeQueriesPerWork": first["queriesPerSample"] / first["totalWorkPerSample"],
            "groupGCCollections": [[r[f"groupGen{g}Collections"] for g in range(3)] for r in rows]})
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
