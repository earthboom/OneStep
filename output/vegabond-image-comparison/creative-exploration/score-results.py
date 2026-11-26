"""Join the blinded judgments to their routes and count eligible concept families."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ROUTES = ("repeat", "style", "concept")


def read_json(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def inspect_image(job):
    path = ROOT / "raw" / f"{job['id']}.png"
    with Image.open(path) as image:
        if image.format != "PNG":
            raise ValueError(f"Expected PNG: {path}")
        image.load()
        facts = {"size": image.size, "sha256": sha256(path.read_bytes()).hexdigest()}
        if job["case"] == "mascot":
            alpha = image.convert("RGBA").getchannel("A")
            corners = [(0, 0), (0, image.height - 1), (image.width - 1, 0),
                       (image.width - 1, image.height - 1)]
            facts["alpha_extrema"] = alpha.getextrema()
            facts["corner_alpha"] = [alpha.getpixel(point) for point in corners]
            facts["transparent"] = (facts["corner_alpha"] == [0, 0, 0, 0]
                                    and facts["alpha_extrema"][1] >= 240)
    return facts


def score_route(rows):
    eligible = [row for row in rows if all(row["checks"])]
    return {
        "first_pass": len(eligible),
        "images": len(rows),
        "all_families": sorted({row["family"] for row in rows}),
        "eligible_families": sorted({row["family"] for row in eligible}),
        "best_eligible_novelty": max((row["novelty"] for row in eligible), default=None),
        "failed_checks": [sum(not row["checks"][i] for row in rows) for i in range(4)],
    }


def prepare_reader(judgments, label_map, jobs, image_facts):
    if {row["id"] for row in judgments} != set(label_map) or len(judgments) != 9:
        raise ValueError("A blind sheet requires one judgment for each label.")

    rows = {route: [] for route in ROUTES}
    for judgment in judgments:
        job = jobs[label_map[judgment["id"]]]
        checks = judgment["checks"].copy()
        if (len(checks) != 4 or any(type(value) is not bool for value in checks)
                or not judgment["family"] or judgment["novelty"] not in (0, 1, 2)):
            raise ValueError(f"Invalid judgment: {judgment}")
        if job["case"] == "mascot":
            checks[3] = checks[3] and image_facts[job["id"]]["transparent"]
        rows[job["route"]].append({**judgment, "checks": checks})

    if any(len(route_rows) != 3 for route_rows in rows.values()):
        raise ValueError("Each route must contain three candidates.")
    return {route: score_route(route_rows) for route, route_rows in rows.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-all", action="store_true")
    args = parser.parse_args()
    jobs = {job["id"]: job for job in read_json("experiment.json")["plan"]}
    key = read_json("review-key.json")
    readers = {name: read_json(f"reader-{name}.json") for name in ("a", "b")}
    complete = set(key).intersection(*(set(scores) for scores in readers.values()))
    present = {item for sheet in complete for item in key[sheet].values()}
    if args.require_all and (len(complete) != 6 or present != set(jobs)):
        raise ValueError(f"Expected all 54 judgments per reader. Shared sheets: {sorted(complete)}")
    if not complete:
        raise ValueError("No complete shared blind review.")

    facts = {name: inspect_image(jobs[name]) for name in sorted(present)}
    scores = {
        sheet: {name: prepare_reader(reader[sheet], key[sheet], jobs, facts)
                for name, reader in readers.items()}
        for sheet in sorted(complete)
    }
    totals = {}
    for route in ROUTES:
        summaries = [reader[route] for sheet in scores.values() for reader in sheet.values()]
        totals[route] = {"eligible_family_sum": sum(len(s["eligible_families"]) for s in summaries),
                         "families_before_checks_sum": sum(len(s["all_families"]) for s in summaries),
                         "first_pass": sum(s["first_pass"] for s in summaries),
                         "image_reviews": sum(s["images"] for s in summaries)}
    report = {"totals": totals, "groups": scores, "images": facts}
    (ROOT / "metrics.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
