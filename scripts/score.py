"""Score a run log with the grading rule locked in PLAN.md, before any results.

Run from the repo root:
    python3 scripts/score.py results/run_log_gemma3-1b.csv

Writes <run log>_scored.csv (one row per call) and <run log>_summary.md.

The rule, as locked:
- Take the number after "Answer:". If "Answer:" appears more than once, the
  last one counts. No number there means a hedge.
- Real-law items: percent error against the real answer; within 5% is correct.
- Counterfactual items: normalized score
      (prediction - cf_answer) / (real_answer - cf_answer)
  0 means it followed the data, 1 means it gave the real-world answer.
  Tracked is 0.2 or less, leaked is 0.8 or more, anything between is recorded
  by its exact score.
- Called out (the model says the data doesn't match real physics) is a separate
  flag. It is read by hand and stored in results/called_out_coding.csv
  (columns: item_id, run_id, called_out, quote). The answer is still scored by
  its number.

Scores below 0 or above 1 are labelled by the rule as written (so -3 counts as
"tracked"), and also flagged in the outside_0_1 column so they can be seen.
"""

import csv
import os
import re
import statistics
import sys

NUMBER = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?|[-+]?\.\d+")
ANSWER = re.compile(r"answer\s*:", re.IGNORECASE)


def extract_answer(text):
    """Return (value or None, parse_status) from the number after the last 'Answer:'."""
    hits = list(ANSWER.finditer(text))
    if not hits:
        return None, "no_answer_line"
    # The rest of that line; if the line is empty (e.g. "**Answer:**\n313.6"), the next one.
    rest = text[hits[-1].end():].lstrip(" \t*\n").split("\n", 1)[0]
    m = NUMBER.search(rest)
    if not m:
        return None, "non_numeric"
    return float(m.group().replace(",", "")), "ok"


def plain(x):
    """240.1, 6144, -12.5: no trailing zeros, no scientific notation."""
    return f"{float(x):.4f}".rstrip("0").rstrip(".")


def score_row(row):
    value, status = extract_answer(row["response"])
    cf, real = float(row["cf_answer"]), float(row["real_answer"])
    out = {"answer_value": "" if value is None else value, "parse_status": status,
           "pct_error": "", "norm_score": "", "outside_0_1": ""}
    if value is None:
        out["label"] = "hedge"
    elif row["law_distance"] == "real":
        err = abs(value - real) / real
        out["pct_error"] = round(err * 100, 2)
        out["label"] = "correct" if err <= 0.05 else "incorrect"
    else:
        s = round((value - cf) / (real - cf), 4) + 0.0  # label from the recorded value (0.79999... is 0.8); + 0.0 turns -0.0 into 0.0
        out["norm_score"] = s
        out["outside_0_1"] = "yes" if (s < 0 or s > 1) else ""
        out["label"] = "tracked" if s <= 0.2 else "leaked" if s >= 0.8 else "between"
    return out


def load_coding(path):
    """Coding keyed by (run_id, item_id, model). Two runs started in the same second share a
    run_id, so rows that need it carry a `model` column; rows without one match any model."""
    coding = {}
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                coding[(r["run_id"], r["item_id"], r.get("model") or "")] = r
    return coding


def lookup_coding(coding, row):
    return (coding.get((row["run_id"], row["item_id"], row.get("model", "")))
            or coding.get((row["run_id"], row["item_id"], "")))


def summarize(rows):
    lines = []
    by = {}
    for r in rows:
        by.setdefault(r["law_distance"], []).append(r)
    model = rows[0]["model"]
    lines.append(f"# Summary: {model}\n")
    r0 = rows[0]
    if "provider" in r0:  # OpenRouter run log
        providers = sorted({r["provider"] for r in rows})
        served = sorted({r["model_served"] for r in rows})
        lines.append(f"OpenRouter, provider {', '.join(providers)} ({r0['quantization']}), served as "
                     f"`{', '.join(served)}`, temperature {r0['temperature']}, seed {r0['seed']}, "
                     f"reasoning {r0['reasoning_setting']}, {len(rows)} calls.\n")
        costs = [float(r["cost_usd"]) for r in rows if r.get("cost_usd") not in ("", None)]
        if costs:
            lines.append(f"Total cost ${sum(costs):.4f}.\n")
    else:  # Ollama run log
        lines.append(f"Model digest `{r0['model_digest']}`, {r0['parameter_size']}, "
                     f"{r0['quantization']}, Ollama {r0['ollama_version']}, "
                     f"temperature {r0['temperature']}, {len(rows)} calls.\n")

    real = by.get("real", [])
    if real:
        errs = [float(r["pct_error"]) for r in real if r["pct_error"] != ""]
        lines.append("## Real-law control (can the model do the task at all?)\n")
        lines.append("| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |")
        lines.append("|---|---|---|---|---|---|")
        lines.append(f"| {len(real)} | {sum(r['label'] == 'correct' for r in real)} | "
                     f"{sum(r['label'] == 'incorrect' for r in real)} | "
                     f"{sum(r['label'] == 'hedge' for r in real)} | "
                     f"{sum(r['called_out'] == 'yes' for r in real)} | "
                     f"{statistics.median(errs):.1f} |\n" if errs else "| | | | | | |\n")

    lines.append("## Counterfactual conditions\n")
    lines.append("Normalized score: 0 = followed the data, 1 = gave the real-world answer.\n")
    lines.append("| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | "
                 "Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for cond in ["near", "far"]:
        rs = by.get(cond, [])
        if not rs:
            continue
        scores = [float(r["norm_score"]) for r in rs if r["norm_score"] != ""]
        mean = f"{statistics.mean(scores):.2f}" if scores else "n/a"
        med = f"{statistics.median(scores):.2f}" if scores else "n/a"
        lines.append(f"| {cond} | {len(rs)} | {mean} | {med} | "
                     f"{sum(r['label'] == 'tracked' for r in rs)} | "
                     f"{sum(r['label'] == 'between' for r in rs)} | "
                     f"{sum(r['label'] == 'leaked' for r in rs)} | "
                     f"{sum(r['outside_0_1'] == 'yes' for r in rs)} | "
                     f"{sum(r['label'] == 'hedge' for r in rs)} | "
                     f"{sum(r['called_out'] == 'yes' for r in rs)} |")
    lines.append("")
    borderline = [r["item_id"] for r in rows if r["called_out"] == "borderline"]
    if borderline:
        lines.append(f"Borderline called out (not counted above; see `called_out_coding.csv`): "
                     f"{', '.join(borderline)}.\n")
    lines.append("The mean is the locked outcome. The median is shown as well because a single "
                 "wild answer can move the mean a long way with 10 items.\n")

    lines.append("## Every call\n")
    lines.append("| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        sc = r["norm_score"] if r["norm_score"] != "" else (f"{r['pct_error']}%" if r["pct_error"] != "" else "")
        ans = plain(r["answer_value"]) if r["answer_value"] != "" else f"({r['parse_status']})"
        lines.append(f"| {r['item_id']} | {r['law_variant']} | {r['test_t']} | {r['cf_answer']} | "
                     f"{r['real_answer']} | {ans} | {sc} | {r['label']} | {r['called_out']} |")
    return "\n".join(lines) + "\n"


def main():
    path = sys.argv[1]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    coding = load_coding(os.path.join(root, "results", "called_out_coding.csv"))
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    scored = []
    for r in rows:
        r = {**r, **score_row(r)}
        c = lookup_coding(coding, r)
        r["called_out"] = c["called_out"] if c else "not coded"
        scored.append(r)
    base = os.path.splitext(path)[0]
    cols = list(rows[0].keys()) + ["answer_value", "parse_status", "pct_error", "norm_score",
                                   "outside_0_1", "label", "called_out"]
    with open(base + "_scored.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(scored)
    with open(base + "_summary.md", "w", encoding="utf-8") as f:
        f.write(summarize(scored))
    print(f"Wrote {base}_scored.csv and {base}_summary.md")


if __name__ == "__main__":
    main()
