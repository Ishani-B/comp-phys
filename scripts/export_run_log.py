"""Combine scored run logs into one CSV for the Drive run-log spreadsheet.

Run from the repo root, after scripts/score.py:
    python3 scripts/export_run_log.py

Writes results/drive_run_log_import.csv with the lab's standard run-log columns,
in order: run_id, date, condition, item_id, model, temperature, repeat,
prompt_id, output, score, notes (see the kits-catalog glossary).

- condition is the law distance: real, near or far.
- score follows the locked rule: the normalized score for near and far items,
  and the percent error for real-law items. Hedges have no score.
- notes holds everything else needed to read or rerun the row: the label,
  the parsed answer, both correct answers, the law variant, called out, and
  the generation settings.
Every model call is one row, including the Gemma 3 1B runs.
"""

import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
OUT = os.path.join(RESULTS, "drive_run_log_import.csv")

# Oldest run first.
SCORED = [
    "run_log_gemma3-1b_cap1024_real_scored.csv",
    "run_log_gemma3-1b_scored.csv",
    "run_log_gemma-4-31b-it_scored.csv",
]

COLUMNS = ["run_id", "date", "condition", "item_id", "model", "temperature", "repeat",
           "prompt_id", "output", "score", "notes"]


def model_text(r):
    if "provider" in r:  # OpenRouter
        return f"{r['model']} (OpenRouter, provider {r['provider']}, {r['quantization']})"
    return (f"{r['model']} (Ollama {r['ollama_version']}, digest {r['model_digest'][:12]}, "
            f"{r['parameter_size']}, {r['quantization']})")


def settings_text(r):
    if "provider" in r:
        return f"seed={r['seed']}; max_tokens={r['max_tokens']}; reasoning={r['reasoning_setting']}"
    return f"seed={r['seed']}; max_tokens={r['num_predict']}"


def score_and_label(r):
    if r["label"] == "hedge":
        return "", f"label=hedge ({r['parse_status']})"
    if r["law_distance"] == "real":
        return r["pct_error"], f"label={r['label']}; score is % error (within 5% counts as correct)"
    extra = "; outside 0-1" if r.get("outside_0_1") == "yes" else ""
    return r["norm_score"], f"label={r['label']}{extra}"


def main():
    rows = []
    for name in SCORED:
        with open(os.path.join(RESULTS, name), newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                score, label = score_and_label(r)
                answer = r["answer_value"] if r["answer_value"] != "" else "none"
                notes = "; ".join([
                    label,
                    f"answer={answer}",
                    f"correct (data)={r['cf_answer']}",
                    f"real-world={r['real_answer']}",
                    f"variant={r['law_variant']}",
                    f"T={r['test_t']}",
                    f"called_out={r['called_out']}",
                    settings_text(r),
                    f"finish={r['done_reason']}",
                ])
                rows.append({
                    "run_id": r["run_id"],
                    "date": r["timestamp_utc"][:10],
                    "condition": r["law_distance"],
                    "item_id": r["item_id"],
                    "model": model_text(r),
                    "temperature": r["temperature"],
                    "repeat": 1,
                    "prompt_id": r["prompt_id"],
                    "output": r["response"],
                    "score": score,
                    "notes": notes,
                })
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
