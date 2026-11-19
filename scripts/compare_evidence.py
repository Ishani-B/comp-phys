"""Compare Gemma 4 31B across evidence levels: Starter (six exact points), noisy, sparse.

Run from the repo root, after scoring the pilot run logs with scripts/score.py:
    python3 scripts/compare_evidence.py

Writes results/pilot_evidence_comparison.md. For each evidence level and law
distance it reports the locked outcome (mean normalized score) plus counts. For
far items it also reports which reference answer each prediction lands closest
to: the data's law, the real law, a t^2 fit or a quadratic fit to the points
shown (descriptive, not part of the grading rule).
"""

import csv
import os
import statistics

from generate_pilot import quad_fit, t2_fit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = [
    ("exact, 6 points (Starter)", "data/freefall_starter.csv", "results/run_log_gemma-4-31b-it_scored.csv"),
    ("noisy, 6 points", "data/freefall_pilot_noisy.csv", "results/run_log_gemma-4-31b-it_pilot_noisy_scored.csv"),
    ("exact, 3 points", "data/freefall_pilot_sparse.csv", "results/run_log_gemma-4-31b-it_pilot_sparse_scored.csv"),
]


def load(path):
    with open(os.path.join(ROOT, path), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def references(item):
    pts = [(float(x.split("s: ")[0]), float(x.split(": ")[1])) for x in item["table"].split("; ")]
    ts, ds = [p[0] for p in pts], [p[1] for p in pts]
    T = float(item["test_t"])
    return {
        "data law": float(item["cf_answer"]),
        "real law": float(item["real_answer"]),
        "t² fit": t2_fit(ts, ds, T),
        "quadratic fit": quad_fit(ts, ds, T),
    }


def closest(answer, refs):
    """Nearest reference by relative distance; references within 1% of the winner tie."""
    dist = {k: abs(answer - v) / abs(v) for k, v in refs.items()}
    best = min(dist.values())
    return " = ".join(k for k, d in dist.items() if d - best <= 0.01)


def main():
    lines = ["# Gemma 4 31B across evidence levels\n",
             "Normalized score: 0 = followed the data's law, 1 = gave the real-world answer. "
             "Real-law items show the number correct within 5%.\n",
             "| Evidence | Real-law control | Near: mean (median) | Near tracked | Far: mean (median) | Far tracked | Hedges | Called out |",
             "|---|---|---|---|---|---|---|---|"]
    detail = []
    for name, data_path, log_path in LEVELS:
        if not os.path.exists(os.path.join(ROOT, log_path)):
            lines.append(f"| {name} | not run | | | | | | |")
            continue
        items = {r["item_id"]: r for r in load(data_path)}
        rows = load(log_path)

        def stats(cond):
            rs = [r for r in rows if r["law_distance"] == cond]
            sc = [float(r["norm_score"]) for r in rs if r["norm_score"] != ""]
            mean = f"{statistics.mean(sc):.2f} ({statistics.median(sc):.2f})" if sc else "n/a"
            return mean, f"{sum(r['label'] == 'tracked' for r in rs)}/{len(rs)}"

        real = [r for r in rows if r["law_distance"] == "real"]
        near_m, near_t = stats("near")
        far_m, far_t = stats("far")
        lines.append(f"| {name} | {sum(r['label'] == 'correct' for r in real)}/{len(real)} | {near_m} | {near_t} | "
                     f"{far_m} | {far_t} | {sum(r['label'] == 'hedge' for r in rows)} | "
                     f"{sum(r['called_out'] == 'yes' for r in rows)} |")
        for r in rows:
            if r["law_distance"] != "far" or r["answer_value"] == "":
                continue
            refs = references(items[r["item_id"]])
            detail.append(f"| {name} | {r['item_id']} | {items[r['item_id']]['formula']} | {r['test_t']} | "
                          f"{float(r['answer_value']):g} | {refs['data law']:g} | {refs['real law']:g} | "
                          f"{refs['t² fit']:.1f} | {refs['quadratic fit']:.1f} | {closest(float(r['answer_value']), refs)} |")
    lines += ["", "## Far items: which reference each answer is closest to\n",
              "| Evidence | Item | Law in data | T | Answer | Data law | Real law | t² fit | Quadratic fit | Closest |",
              "|---|---|---|---|---|---|---|---|---|---|"] + detail
    out = os.path.join(ROOT, "results", "pilot_evidence_comparison.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
