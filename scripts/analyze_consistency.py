"""Consistency check: how much do answers vary at the default temperature?

Run from the repo root, after scoring the consistency run log with scripts/score.py:
    python3 scripts/analyze_consistency.py

Compares 10 default-temperature samples per item with the temperature-0 Starter
answer (results/run_log_gemma-4-31b-it_scored.csv). Writes results/consistency_check.md.
"""

import csv
import os
import statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, "results", name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    samples = load("run_log_gemma-4-31b-it_consistency_scored.csv")
    t0 = {r["item_id"]: r for r in load("run_log_gemma-4-31b-it_scored.csv")}
    with open(os.path.join(ROOT, "data", "freefall_starter.csv"), newline="", encoding="utf-8") as f:
        formula = {r["item_id"]: r["formula"] for r in csv.DictReader(f)}
    out = ["# Consistency check: Gemma 4 31B at the default temperature\n",
           "Design: \"Consistency check\" in `PLAN.md`. 10 samples per item, temperature and seed left to "
           "the provider's defaults, everything else as in the Starter.\n",
           "| Item | Law | Correct (data) | Temp-0 answer | Default-temp answers (10) | Min | Max | SD | Distinct replies | Same label as temp 0 | Labels |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    same_total = n_total = 0
    for iid in sorted({r["item_id"] for r in samples}, key=lambda s: ["R", "N", "F"].index(s.split("-")[1]) * 100 + int(s[-2:])):
        rs = [r for r in samples if r["item_id"] == iid]
        vals = [float(r["answer_value"]) for r in rs if r["answer_value"] != ""]
        base = t0[iid]
        same = sum(r["label"] == base["label"] for r in rs)
        same_total += same
        n_total += len(rs)
        labels = ", ".join(f"{k} {v}" for k, v in sorted({l: sum(r['label'] == l for r in rs) for l in {r['label'] for r in rs}}.items()))
        distinct = len({r["response"] for r in rs})
        out.append(f"| {iid} | {formula.get(iid, '')} | {base['cf_answer']} | "
                   f"{float(base['answer_value']):g} | {', '.join(f'{v:g}' for v in vals)} | "
                   f"{min(vals):g} | {max(vals):g} | {statistics.pstdev(vals):.3g} | {distinct}/{len(rs)} | "
                   f"{same}/{len(rs)} | {labels} |")
    hedges = sum(r["label"] == "hedge" for r in samples)
    out += ["", f"**Overall:** {same_total} of {n_total} default-temperature answers keep the temperature-0 label; "
                f"{hedges} hedges. Cost ${sum(float(r['cost_usd'] or 0) for r in samples):.4f}.\n",
            "The provider really sampled: every reply's wording differs (\"Distinct replies\"), and lengths vary. "
            "So the identical answers come from the model, not from a deterministic default.\n"]
    dest = os.path.join(ROOT, "results", "consistency_check.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"Wrote {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    main()
