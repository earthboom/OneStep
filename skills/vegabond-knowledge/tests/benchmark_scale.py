"""Build an isolated Markdown corpus and measure the production search CLI.

Run 'build DIR' once, then 'measure DIR OUTPUT --script PATH' for each version.
The measurements include interpreter startup. Expected ranking misses are data.
"""
import argparse
import json
import os
import math
import random
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CASES = HERE / "scale_korean_cases.json"
SCRIPT = HERE.parent / "scripts" / "search.py"
TOPICS = (
    ("camera", "camera clipping against walls", "adjust the near plane"),
    ("reverse", "reverse parking alarm", "check the warning speaker"),
    ("music", "music loudness calibration", "measure the mixed audio"),
    ("restart", "restart a stopped worker", "restore the pending queue"),
    ("fade", "fade a menu overlay", "check the alpha ramp"),
    ("offset", "offset a spectator view", "check the viewport origin"),
    ("module", "module dependency cycle", "check dependency direction"),
    ("format", "format exported tables", "check column width"),
    ("archive", "archive retention", "check the cleanup interval"),
    ("timeout", "queue timeout", "inspect the wait budget"),
    ("layout", "panel layout measurement", "measure the outer margin"),
    ("atlas", "sprite atlas padding", "compare border pixels"),
)


def build(project, size):
    if not project.resolve().is_relative_to((ROOT / ".cache/onestep").resolve()):
        raise ValueError("Create the isolated project under .cache/onestep/")
    project.mkdir(parents=True, exist_ok=False)
    count = 0
    for store in ("knowledge", "records"):
        for source in (ROOT / store).rglob("*.md"):
            if source.name.lower().endswith(".kr.md"):
                continue
            dest = project / source.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
            dest.with_suffix(".kr.md").touch()
            if source.parent != ROOT / store and source.name.lower() not in {"index.md", "archive.md"}:
                count += 1
    if size < count:
        raise ValueError("size must cover all real entries")
    for i in range(size - count):
        record = bool(i % 2)
        store, prefix = ("records", "R") if record else ("knowledge", "K")
        tag, topic, check = TOPICS[(i // 2) % len(TOPICS)]
        ident = f"{prefix}-SCALE-{i:05d}"
        folder = project / store / "code" / f"batch-{i // 1000:02d}"
        folder.mkdir(parents=True, exist_ok=True)
        status, kind = ("resolved", "error") if record else ("active", "reference")
        lines = ["---", f"id: {ident}", f"title: {topic} in fixture {i}",
                 f"summary: {check} for component {i}.", f"scope: fixture component {i}",
                 f"kind: {kind}", f"status: {status}", f"keywords: [{tag}, {topic}]",
                 "checked_at: '2026-11-14'"]
        if record:
            lines.extend([f"trigger: {topic}", f"symptom: {tag} output out of bounds",
                          "cause_status: confirmed", f"prevention: {check}", "prevention_status: verified"])
        sections = (("Expected and observed", "Cause and resolution", "Recheck and prevention") if record
                    else ("Guidance", "Applicability and exceptions", "Checks"))
        lines.extend(["---", f"# {topic}", *[f"## {s}\n{check} for component {i}." for s in sections],
                      f"## Evidence\nSynthetic calibration {i}.", ""])
        (folder / f"{ident}.md").write_text("\n".join(lines), encoding="utf-8")
        (folder / f"{ident}.kr.md").touch()
    print(json.dumps(dict(entries=size, original=count, synthetic=size-count)))


def run(project, script, *args):
    start = time.perf_counter()
    proc = subprocess.run([sys.executable, "-B", "-X", "utf8", str(script), *args,
                           "--project", str(project)], stdout=subprocess.PIPE, check=False)
    wall = round(time.perf_counter() - start, 3)
    data = json.loads(proc.stdout)
    if proc.returncode not in (0, 1) or "index" not in data:
        raise RuntimeError(data)
    return dict(wall_seconds=wall, **data)


def update(project, script):
    target = project / "knowledge/code/batch-00/K-SCALE-00000.md"
    if not target.resolve().is_relative_to((ROOT / ".cache/onestep").resolve()):
        raise ValueError("Updates require an isolated benchmark fixture")
    original, stamp = target.read_bytes(), target.stat()
    marker = "OneStepCalibrationChangedMarker"
    if b"Synthetic calibration 0." not in original or marker.encode() in original:
        raise ValueError("Unexpected fixture content")
    try:
        with target.open("ab") as stream:
            stream.write(("\n" + marker + "\n").encode())
        result = run(project, script, "search", "--query", marker)
        if result["index"]["read_files"] != 1 or [h["id"] for h in result["results"]] != ["K-SCALE-00000"]:
            raise ValueError("Updated fixture must be the sole reparse and sole matching hit")
        return result
    finally:
        target.write_bytes(original)
        os.utime(target, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))


def measure(project, output, script):
    result = {}
    for name, args in (
        ("first", ["search", "--query", "R-CODE-UE-SPEED-REVERSE"]),
        ("judgments", ["evaluate", "--cases", str(CASES)]),
        ("warm_id", ["search", "--query", "R-CODE-UE-MUSIC-STOP"]),
        ("warm_broad", ["search", "--query", "카메라"]),
        ("warm_question", ["search", "--query", "뒤로 달리면 시점이 주인공을 앞질러요"]),
    ):
        result[name] = run(project, script, *args)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(name, result[name]["wall_seconds"], flush=True)


def sample_cases():
    # Keep the same case order and per-query filters for both client modes.
    fixed = json.loads(CASES.read_text(encoding="utf-8"))
    cases = fixed["cases"] + fixed["transfer_cases"]
    seen = {case["query"] for case in cases}
    suites = [HERE / "retrieval_cases.json", *sorted((HERE / "game-application").glob("*retrieval-cases.json")),
              *sorted((ROOT / "prototypes/TechniqueLab/Results").glob("*/retrieval-cases.json"))]
    rng = random.Random(20261123)
    pools = [json.loads(path.read_text(encoding="utf-8"))["cases"] for path in suites]
    for pool in pools:
        rng.shuffle(pool)
    while len(cases) < 50 and any(pools):
        for pool in pools:
            if pool and len(cases) < 50:
                case = pool.pop()
                if case["query"] not in seen:
                    cases.append(case)
                    seen.add(case["query"])
    if len(cases) != 50:
        raise ValueError("Expected 50 distinct queries")
    return cases


def search_options(case):
    args = ["--query", case["query"], "--limit", str(case.get("limit", 5))]
    for domain in case.get("domains", []):
        args.extend(["--domain", domain])
    for status in case.get("statuses", []):
        args.extend(["--status", status])
    for key in ("store", "scope"):
        if key in case:
            args.extend(["--" + key, case[key]])
    for key, value in case.get("context", {}).items():
        args.extend(["--context", f"{key}={value}"])
    if case.get("include_superseded"):
        args.append("--include-superseded")
    return args


def judge(case, result):
    ids = [hit["id"] for hit in result["results"]]
    concepts = {rule["id"] for rule in result["inferred_concepts"]}
    passed = (result["ok"] and not set(case.get("required", [])) - set(ids)
              and not set(case.get("forbidden", [])).intersection(ids)
              and not concepts.intersection(case.get("forbidden_concepts", []))
              and not (case.get("expect_empty") and result["total_matches"]))
    return ids, bool(passed)


def sample(project, output, script):
    rows = []
    for case in sample_cases():
        result = run(project, script, "search", *search_options(case))
        ids, passed = judge(case, result)
        rows.append(dict(name=case["name"], query=case["query"], passed=bool(passed), ids=ids,
                         seconds=result["wall_seconds"], helper_ms=result["elapsed_ms"],
                         index_ms=result["index"]["elapsed_ms"], backend=result["index"].get("backend"),
                         read_files=result["index"]["read_files"]))
        output.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        if len(rows) % 10 == 0:
            print("warm queries", len(rows), flush=True)


def sample_sessions(project, output, script, reference, rounds):
    cases = sample_cases()
    expected = json.loads(reference.read_text(encoding="utf-8"))
    if [c["query"] for c in cases] != [r["query"] for r in expected["queries"]]:
        raise ValueError("Query order differs from the frozen reference")
    runs = []
    for number in range(1, rounds + 1):
        rows = []
        # The first request owns process launch; later requests own encoding,
        # both pipe transfers and decoding the complete response at the caller.
        start = time.perf_counter()
        with subprocess.Popen([sys.executable, "-B", "-X", "utf8", str(script), "session",
                               "--project", str(project)], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
            try:
                for i, (case, prior) in enumerate(zip(cases, expected["queries"])):
                    if i:
                        start = time.perf_counter()
                    payload = json.dumps(search_options(case), ensure_ascii=False).encode("utf-8") + b"\n"
                    proc.stdin.write(payload)
                    proc.stdin.flush()
                    reply = proc.stdout.readline()
                    if not reply:
                        raise RuntimeError(f"Session ended before answering {case['name']}")
                    result = json.loads(reply)
                    seconds = time.perf_counter() - start
                    ids, passed = judge(case, result)
                    rows.append(dict(name=case["name"], query=case["query"], seconds=seconds, ids=ids,
                                     passed=passed, same_order=ids == prior["returned_ids"], bytes=len(reply),
                                     helper_ms=result["elapsed_ms"], index_ms=result["index"]["elapsed_ms"],
                                     entries=result["index"]["entries"], read_files=result["index"]["read_files"],
                                     backend=result["index"].get("backend")))
            finally:
                proc.stdin.close()
        if proc.returncode:
            raise RuntimeError(f"Session exited with status {proc.returncode}")
        times = sorted(row["seconds"] for row in rows)
        run_summary = dict(round=number, first_seconds=rows[0]["seconds"], p50=statistics.median(times),
                           p95=times[math.ceil(.95*len(times))-1], maximum=times[-1],
                           within_two_seconds=sum(t <= 2 for t in times), rows=rows)
        runs.append(run_summary)
        output.write_text(json.dumps(dict(reference=reference.name, runs=runs), ensure_ascii=False, indent=2),
                          encoding="utf-8")
        print(f"Round {number}: P95 {run_summary['p95']:.3f}s, max {times[-1]:.3f}s, "
              f"{run_summary['within_two_seconds']}/{len(rows)} within 2s", flush=True)
    return all(r["maximum"] <= 2 and all(row["same_order"] and row["passed"] and row["read_files"] == 0
               and row["entries"] == expected["corpus_entries"] and row["backend"] == "sqlite"
               for row in r["rows"]) for r in runs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("build")
    create.add_argument("project", type=Path)
    create.add_argument("--size", type=int, default=30000)
    for name in ("measure", "update", "sample"):
        bench = commands.add_parser(name)
        bench.add_argument("project", type=Path)
        bench.add_argument("output", type=Path)
        bench.add_argument("--script", type=Path, default=SCRIPT)
    sessions = commands.add_parser("sample-sessions")
    sessions.add_argument("project", type=Path)
    sessions.add_argument("output", type=Path)
    sessions.add_argument("--script", type=Path, default=SCRIPT)
    sessions.add_argument("--reference", type=Path, default=ROOT / "docs/research/2026-11-23-cold-index-measurements.json")
    sessions.add_argument("--rounds", type=int, default=5)
    args = parser.parse_args()
    if args.command == "build":
        build(args.project, args.size)
    elif args.output.exists():
        raise ValueError("Choose a new measurement output")
    elif args.command == "measure":
        measure(args.project, args.output, args.script)
    elif args.command == "sample":
        sample(args.project, args.output, args.script)
    elif args.command == "sample-sessions":
        if args.rounds < 1:
            parser.error("--rounds must be positive")
        raise SystemExit(not sample_sessions(args.project, args.output, args.script, args.reference, args.rounds))
    else:
        result = update(args.project, args.script)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(result["wall_seconds"])
