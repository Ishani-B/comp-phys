"""Summarize the Standard run: 3 domains x 2 models x 3 law distances.

Run from the repo root, after scoring each run log with scripts/score.py:
    python3 scripts/compare_standard.py

Gemma 4 31B on free fall is the Starter run (results/run_log_gemma-4-31b-it_scored.csv),
reused as the design says. Writes results/standard_comparison.md with the locked
outcome per cell: real-law control (correct within 5%), and for near and far the
mean normalized score (median), tracked / between / leaked counts, hedges and
called out.
"""

import csv
import os
import statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = [("Gemma 4 31B", "gemma4-31b"), ("Claude Sonnet 4.6", "claude-sonnet-4.6")]
DOMAINS = [("Free fall", "freefall"), ("Hooke", "hooke"), ("Kepler", "kepler")]


def path_for(model_key, domain_key):
    if model_key == "gemma4-31b" and domain_key == "freefall":
        return os.path.join(ROOT, "results", "run_log_gemma-4-31b-it_scored.csv")
    return os.path.join(ROOT, "results", f"run_log_std_{model_key}_{domain_key}_scored.csv")


def r2(x):
    return round(x, 2) + 0.0


def main():
    out = ["# Standard run: three domains, two models\n",
           "Design: \"Standard run\" in `PLAN.md`. Normalized score: 0 = followed the data's law, "
           "1 = gave the real-world answer (Earth's law for free fall; the familiar form fitted to the "
           "data for Hooke and Kepler). 10 items per cell.\n",
           "| Domain | Model | Real-law control | Near: mean (median) | Near tracked / between / leaked | "
           "Far: mean (median) | Far tracked / between / leaked | Hedges | Called out |",
           "|---|---|---|---|---|---|---|---|---|"]
    cost = 0.0
    for dname, dkey in DOMAINS:
        for mname, mkey in MODELS:
            p = path_for(mkey, dkey)
            if not os.path.exists(p):
                out.append(f"| {dname} | {mname} | not run | | | | | | |")
                continue
            with open(p, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            if not (mkey == "gemma4-31b" and dkey == "freefall"):
                cost += sum(float(r.get("cost_usd") or 0) for r in rows)

            def cell(d):
                rs = [r for r in rows if r["law_distance"] == d]
                if not rs:
                    return "not run", ""
                sc = [float(r["norm_score"]) for r in rs if r["norm_score"] != ""]
                m = f"{r2(statistics.mean(sc)):.2f} ({r2(statistics.median(sc)):.2f})" if sc else "n/a"
                counts = "/".join(str(sum(r["label"] == k for r in rs)) for k in ["tracked", "between", "leaked"])
                return m, counts
            real = [r for r in rows if r["law_distance"] == "real"]
            nm, nc = cell("near")
            fm, fc = cell("far")
            borderline = sum(r["called_out"] == "borderline" for r in rows)
            out.append(f"| {dname} | {mname} | {sum(r['label'] == 'correct' for r in real)}/{len(real)} | {nm} | {nc} | "
                       f"{fm} | {fc} | {sum(r['label'] == 'hedge' for r in rows)} | "
                       f"{sum(r['called_out'] == 'yes' for r in rows)}{f' (+{borderline} borderline)' if borderline else ''} |")
    out += ["", f"New Standard calls cost ${cost:.4f} (Gemma free fall reused from the Starter).\n"]
    dest = os.path.join(ROOT, "results", "standard_comparison.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"Wrote {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    main()
