"""Prepare randomized individual previews, then score locked first impressions and detailed reads."""

import hashlib
import json
import sys
from pathlib import Path
from random import SystemRandom

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ARMS = ("before", "after")
READERS = ("J", "K")
CASES = ("01", "02", "03")


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8-sig"))


def write(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    if (ROOT / "key.json").exists():
        raise ValueError("Blind key already saved")
    key = []
    for arm in ARMS:
        rows = read(f"{arm}/run.json")
        assert len(rows) == 9 and {(r["id"], r["repeat"]) for r in rows} == {
            (case, rep) for case in CASES for rep in (1, 2, 3)}
        for row in rows:
            assert row["final"] in (row["initial"], row["repair"])
            for stage in ("initial", "final"):
                key.append(dict(arm=arm, case=row["id"], rep=row["repeat"],
                                stage=stage, file=row[stage], labels={}))
    candidates = sorted({(k["arm"], k["file"]) for k in key})
    rng = SystemRandom()
    for reader in READERS:
        directory = ROOT / reader
        directory.mkdir(exist_ok=True)
        order = rng.sample(candidates, len(candidates))
        for i, (arm, name) in enumerate(order, 1):
            label = f"{i:02}"
            with Image.open(ROOT / arm / name) as img:
                rgb = img.convert("RGB")
                rgb.info.clear()
                rgb.save(directory / f"{label}-full.png")
                rgb.thumbnail((384, 384), Image.Resampling.LANCZOS)
                rgb.save(directory / f"{label}.png")
            for k in key:
                if (k["arm"], k["file"]) == (arm, name):
                    k["labels"][reader] = label
    write("key.json", key)


def unlock():
    key = read("key.json")
    for reader in READERS:
        labels = {k["labels"][reader]: k["case"] for k in key}
        path = ROOT / reader / "first.json"
        first = read(path)
        assert {r["label"] for r in first} == set(labels) and len(first) == len(labels)
        assert all(isinstance(r["tie"], bool) and r["object"].strip() for r in first)
        write(f"{reader}/case-map.json", labels)
    write("first-hashes.json", {r: digest(ROOT / r / "first.json") for r in READERS})


def aggregate():
    key = read("key.json")
    marks = {}
    for reader in READERS:
        assert digest(ROOT / reader / "first.json") == read("first-hashes.json")[reader]
        first = {x["label"]: x for x in read(f"{reader}/first.json")}
        scores = read(f"{reader}/scores.json")
        assert len(scores) == len(first) and {x["label"] for x in scores} == set(first)
        marks[reader] = {}
        for row in scores:
            m = row["marks"]
            assert len(m) == 4 and set(m) <= {0, 1} and row["note"].strip()
            assert not first[row["label"]]["tie"] or m[1] == 0
            marks[reader][row["label"]] = m
    def count(rows, readers=READERS):
        m = [marks[r][k["labels"][r]] for k in rows for r in readers]
        return dict(n=len(m), identity=sum(v[0] for v in m), focus=sum(v[1] for v in m),
                    joint=sum(v[0] and v[1] for v in m), light=sum(v[2] for v in m),
                    scene=sum(v[3] for v in m), full=sum(all(v) for v in m))
    result = {}
    for stage in ("initial", "final"):
        result[stage] = {}
        for arm in ARMS:
            chosen = [k for k in key if k["arm"] == arm and k["stage"] == stage]
            result[stage][arm] = dict(overall=count(chosen),
                cases={c:count([k for k in chosen if k["case"]==c]) for c in CASES},
                readers={r:count(chosen,[r]) for r in READERS},
                both_readers=sum(count([k])["joint"]==2 for k in chosen))
    result["repair_calls"] = {a:sum(bool(r["repair"]) for r in read(f"{a}/run.json")) for a in ARMS}
    unique = {(k["arm"],k["file"]):k for k in key}.values()
    result["n_unique"] = len(unique)
    result["agreement"] = [sum(marks["J"][k["labels"]["J"]][i] == marks["K"][k["labels"]["K"]][i]
                               for k in unique) for i in range(4)]
    write("metrics.json",result)
    for case in CASES:
        canvas=Image.new("RGB",(1000,975),"#fafafa")
        draw=ImageDraw.Draw(canvas)
        for k in key:
            if k["stage"]!="final" or k["case"]!=case:
                continue
            x,y=500*ARMS.index(k["arm"]),325*(k["rep"]-1)
            with Image.open(ROOT/k["arm"]/k["file"]) as src:
                im=src.convert("RGB")
                im.thumbnail((492,298), Image.Resampling.LANCZOS)
                canvas.paste(im,(x+(500-im.width)//2,y+22))
            draw.text((x+6,y+4),f"{k['arm']}   run {k['rep']}   both conditions {count([k])['joint']}/2",fill="#202020")
        canvas.save(ROOT/f"comparison-{case}.jpg",quality=93)


if __name__=="__main__":
    {"prepare":prepare,"unlock":unlock,"aggregate":aggregate}[sys.argv[1]]()
