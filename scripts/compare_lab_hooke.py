"""Summarize the Hooke lab extension and set it beside the Standard run's Hooke tables.

Run from the repo root, after scoring each lab log with scripts/score.py:
    python3 scripts/compare_lab_hooke.py

Writes results/lab_hooke_comparison.md: the locked outcome per model and framing,
the same near laws on tables (Standard) vs in the lab, how the models measured,
and which reference each near answer lands closest to (the data's law, a straight
line fitted to the model's own readings, or a quadratic fitted to them).
"""

import csv
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare_lab import model_text  # noqa: E402
from generate_pilot import quad_fit  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = [("Gemma 4 31B", "gemma", "gemma4-31b"), ("Claude Sonnet 4.6", "claude", "claude-sonnet-4.6")]
HOOKE = re.compile(r"hooke", re.I)


def load(p):
    with open(os.path.join(ROOT, p), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def r2(x):
    return round(x, 2) + 0.0


def near_stats(rows):
    rs = [r for r in rows if r["law_distance"] == "near"]
    sc = [float(r["norm_score"]) for r in rs if r["norm_score"] != ""]
    mean = f"{r2(statistics.mean(sc)):.2f} ({r2(statistics.median(sc)):.2f})" if sc else "n/a"
    counts = "/".join(str(sum(r["label"] == k for r in rs)) for k in ["tracked", "between", "leaked", "hedge"])
    return mean, counts


def closest(r):
    if r["answer_value"] == "":
        return "hedge"
    a = float(r["answer_value"])
    pts = json.loads(r["measurements"])
    X = float(r["test_x"])
    refs = {"data law": float(r["cf_answer"])}
    if pts:
        k = sum(d * t for t, d in pts) / sum(t * t for t, _ in pts)
        refs["straight line"] = k * X
    if len({t for t, _ in pts}) >= 3:
        refs["quadratic"] = quad_fit([t for t, _ in pts], [d for _, d in pts], X)
    dist = {k: abs(a - v) / abs(v) for k, v in refs.items() if v}
    best = min(dist.values())
    return " = ".join(k for k, d in dist.items() if d - best <= 0.01)


def main():
    out = ["# Lab extension: Hooke's law, both models\n",
           "Design: \"Lab extension\" in `PLAN.md`. Each model chooses its own weights (0–600 g, up to 8), "
           "then predicts the stretch at 700–1600 g. Normalized score: 0 = the data's law, 1 = the straight "
           "line fitted to the Standard's table points. 10 items per row.\n",
           "## Locked outcome\n",
           "| Model | Framing | Real-law control | Near: mean (median) | Near tracked / between / leaked / hedge | Far: mean | Far tracked | Called out |",
           "|---|---|---|---|---|---|---|---|"]
    tables = ["## The same near laws: given a table vs choosing the measurements\n",
              "| Model | Setting | Near: mean (median) | Near tracked / between / leaked / hedge |",
              "|---|---|---|---|"]
    beh = ["## How they measured, and where near answers land\n",
           "| Model | Framing | Mean measurements | Widest weight measured (median) | Replies naming Hooke's law | Near answers closest to: data law / straight line / quadratic / other |",
           "|---|---|---|---|---|---|"]
    cost = 0.0
    for mname, mkey, skey in MODELS:
        std = load(f"results/run_log_std_{skey}_hooke_scored.csv")
        m, c = near_stats(std)
        tables.append(f"| {mname} | Standard: table of 6 points | {m} | {c} |")
        for framing in ["physics", "neutral"]:
            rows = load(f"results/run_log_lab_hooke_{framing}_exact_{mkey}_scored.csv")
            cost += sum(float(r["cost_usd"] or 0) for r in rows)
            real = [r for r in rows if r["law_distance"] == "real"]
            far = [r for r in rows if r["law_distance"] == "far"]
            fsc = [float(r["norm_score"]) for r in far if r["norm_score"] != ""]
            nm, nc = near_stats(rows)
            yes = sum(r["called_out"] == "yes" for r in rows)
            label = "spring story" if framing == "physics" else "neutral dial"
            out.append(f"| {mname} | {label} | {sum(r['label'] == 'correct' for r in real)}/{len(real)} | {nm} | {nc} | "
                       f"{r2(statistics.mean(fsc)):.2f} | {sum(r['label'] == 'tracked' for r in far)}/{len(far)} | "
                       f"{yes if framing == 'physics' else 'n/a'} |")
            tables.append(f"| {mname} | Lab: {label} | {nm} | {nc} |")
            near = [r for r in rows if r["law_distance"] == "near"]
            cl = [closest(r) for r in near]
            other = sum(1 for x in cl if x not in ("data law", "straight line", "quadratic"))
            widest = statistics.median(max(t for t, _ in json.loads(r["measurements"])) for r in rows if json.loads(r["measurements"]))
            beh.append(f"| {mname} | {label} | {statistics.mean(int(r['n_measurements']) for r in rows):.1f} | {widest:g} g | "
                       f"{sum(bool(HOOKE.search(model_text(r['transcript']))) for r in rows)}/{len(rows)} | "
                       f"{cl.count('data law')} / {cl.count('straight line')} / {cl.count('quadratic')} / {other} |")
    text = "\n".join(out + ["", *tables, "", *beh, "", f"Lab extension cost ${cost:.4f}.\n"]) + "\n"
    dest = os.path.join(ROOT, "results", "lab_hooke_comparison.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    main()
