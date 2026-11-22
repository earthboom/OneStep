"""Prepare anonymous viewing copies, then aggregate both independent score files."""

from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
from random import SystemRandom
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ARMS = ("before", "after")
READERS = ("reader1", "reader2")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def save(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sheet(items, cols, cell, output):
    width, height = cell
    canvas = Image.new("RGB", (cols * width, ((len(items) + cols - 1) // cols) * height), "#f7f7f5")
    draw = ImageDraw.Draw(canvas)
    for index, (label, path) in enumerate(items):
        with Image.open(path) as src:
            im = src.convert("RGB")
            im.thumbnail((width - 12, height - 28), Image.Resampling.LANCZOS)
        x, y = index % cols * width, index // cols * height
        canvas.paste(im, (x + (width - im.width) // 2, y + 23))
        draw.text((x + 7, y + 4), label, fill="#222222")
    canvas.save(output, quality=93)


def prepare():
    if (ROOT / "key.json").exists():
        raise ValueError("Anonymous key already exists")
    directory = ROOT / "blind"
    directory.mkdir(exist_ok=True)
    by_case = defaultdict(list)
    for arm in ARMS:
        rows = read(f"{arm}/run.json")
        assert {(r["id"], r["repeat"]) for r in rows} == {
            (f"{i:02}", j) for i in range(1, 9) for j in (1, 2)
        } and len(rows) == 16
        for row in rows:
            for stage in ("initial", "final"):
                by_case[row["id"]].append((arm, row["repeat"], stage, row[stage]))
    rand = SystemRandom()
    key = []
    for case, candidates in sorted(by_case.items()):
        paths = sorted({(arm, name) for arm, _, _, name in candidates})
        rand.shuffle(paths)
        labels = {}
        sheet_items = []
        for counter, (arm, name) in enumerate(paths):
            label = f"{case}-{chr(ord('A') + counter)}"
            labels[arm, name] = label
            target = directory / f"{label}.png"
            with Image.open(ROOT / arm / name) as im:
                rgb = im.convert("RGB")
                rgb.info.clear()
                rgb.save(target)
            sheet_items.append((label, target))
        sheet(sheet_items, 2, (690, 460), directory / f"{case}.jpg")
        for arm, rep, stage, name in candidates:
            key.append(dict(id=case, arm=arm, repeat=rep, stage=stage, file=name, label=labels[arm, name]))
    save("key.json", key)


def aggregate():
    key = read("key.json")
    labels = {r["label"] for r in key}
    reviews = {}
    for reader in READERS:
        entries = read(f"{reader}.json")
        assert len(entries) == len(labels)
        reviews[reader] = {r["label"]: r for r in entries}
        assert set(reviews[reader]) == labels
        for entry in entries:
            assert len(entry["marks"]) == 4 and set(entry["marks"]) <= {0, 1} and entry["note"].strip()
    results = {}
    for stage in ("initial", "final"):
        totals = {}
        chosen = [r for r in key if r["stage"] == stage]
        for arm in ARMS:
            rows = [r for r in chosen if r["arm"] == arm]
            by_case = {}
            for case in sorted({r["id"] for r in rows}):
                marks = [reviews[v][r["label"]]["marks"] for r in rows if r["id"] == case for v in READERS]
                by_case[case] = dict(hits=sum(map(sum, marks)), possible=16, all_pass=sum(all(m) for m in marks), decisions=4)
            totals[arm] = dict(cases=by_case, hits=sum(v["hits"] for v in by_case.values()),
                               all_pass=sum(v["all_pass"] for v in by_case.values()))
        pairs = []
        for case in sorted({r["id"] for r in chosen}):
            for rep in (1, 2):
                scores = [sum(sum(reviews[v][r["label"]]["marks"]) for v in READERS)
                          for arm in ARMS for r in chosen if (r["id"], r["repeat"], r["arm"]) == (case, rep, arm)]
                pairs.append(scores[1] - scores[0])
        results[stage] = {"totals": totals, "pairs_after_win_tie_loss":
                          [sum(x > 0 for x in pairs), pairs.count(0), sum(x < 0 for x in pairs)]}
    results["blind_candidates"] = len(labels)
    results["agreed_marks"] = sum(a == b for label in labels for a, b in zip(
        reviews[READERS[0]][label]["marks"], reviews[READERS[1]][label]["marks"]))
    results["total_marks_compared"] = 4 * len(labels)
    results["reader_final"] = {
        reader: {arm: sum(sum(reviews[reader][r["label"]]["marks"]) for r in key
                          if r["arm"] == arm and r["stage"] == "final") for arm in ARMS}
        for reader in READERS
    }
    results["repairs"] = {arm: sum(r["repair"] is not None for r in read(f"{arm}/run.json")) for arm in ARMS}
    results["files_sha256"] = {f"{arm}/{p.name}": sha256(p.read_bytes()).hexdigest()
                                for arm in ARMS for p in (ROOT / arm).glob("*.png")}
    save("metrics.json", results)
    compare = ROOT / "comparisons"
    compare.mkdir(exist_ok=True)
    for case in sorted({r["id"] for r in key}):
        items = []
        for rep in (1, 2):
            for arm in ARMS:
                r, = [r for r in key if (r["id"], r["arm"], r["repeat"], r["stage"]) == (case, arm, rep, "final")]
                marks = [sum(reviews[v][r["label"]]["marks"]) for v in READERS]
                items.append((f"{arm}   run {rep}   readers {marks[0]}/4, {marks[1]}/4", ROOT / arm / r["file"]))
        sheet(items, 2, (690, 460), compare / f"{case}.jpg")


if __name__ == "__main__":
    {"prepare": prepare, "aggregate": aggregate}[sys.argv[1]]()
