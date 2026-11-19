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
# The pilot rows alone, with no header row, for File > Import > "Append to current sheet".
PILOT_APPEND = os.path.join(RESULTS, "drive_run_log_pilot_append.csv")

# Oldest run first: (scored log, evidence level shown in notes).
SCORED = [
    ("run_log_gemma3-1b_cap1024_real_scored.csv", "exact-6"),
    ("run_log_gemma3-1b_scored.csv", "exact-6"),
    ("run_log_gemma-4-31b-it_scored.csv", "exact-6"),
    ("run_log_gemma-4-31b-it_pilot_noisy_scored.csv", "noisy-6"),
    ("run_log_gemma-4-31b-it_pilot_sparse_scored.csv", "exact-3"),
    ("run_log_lab_physics_exact_scored.csv", "lab"),
    ("run_log_lab_physics_noisy_scored.csv", "lab"),
    ("run_log_lab_neutral_exact_scored.csv", "lab"),
    ("run_log_lab_neutral_noisy_scored.csv", "lab"),
    ("run_log_lab_physics_noisy_cap16k_scored.csv", "lab-rerun"),
    ("run_log_lab_neutral_noisy_cap16k_scored.csv", "lab-rerun"),
    ("run_log_gemma-4-31b-it_consistency_scored.csv", "consistency"),
    ("run_log_std_gemma4-31b_hooke_scored.csv", "standard"),
    ("run_log_std_gemma4-31b_kepler_scored.csv", "standard"),
    ("run_log_std_claude-sonnet-4.6_freefall_scored.csv", "standard"),
    ("run_log_std_claude-sonnet-4.6_hooke_scored.csv", "standard"),
    ("run_log_std_claude-sonnet-4.6_kepler_scored.csv", "standard"),
]
# Consistency check and Standard rows, no header, for appending.
STD_APPEND = os.path.join(RESULTS, "drive_run_log_standard_append.csv")
RERUN_APPEND = os.path.join(RESULTS, "drive_run_log_lab_rerun_append.csv")
PILOT = {"noisy-6", "exact-3"}
# Lab rows alone, no header, for appending. One row per episode; an episode holds several model calls.
LAB_APPEND = os.path.join(RESULTS, "drive_run_log_lab_append.csv")

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
    rows, pilot_rows, lab_rows, rerun_rows, std_rows = [], [], [], [], []
    for name, evidence in SCORED:
        path = os.path.join(RESULTS, name)
        if not os.path.exists(path):
            continue
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                score, label = score_and_label(r)
                answer = r["answer_value"] if r["answer_value"] != "" else "none"
                is_lab = evidence in ("lab", "lab-rerun")
                where = (f"evidence={evidence} ({r['framing']} framing, {r['readings']} readings, "
                         f"max {r['max_tokens']} tokens per turn, "
                         f"{r['n_measurements']} measurements, {r['n_turns']} model calls in this episode)"
                         if is_lab else f"evidence={evidence}")
                notes = "; ".join([
                    label,
                    where,
                    f"answer={answer}",
                    f"correct (data)={r['cf_answer']}",
                    f"real-world={r['real_answer']}",
                    f"variant={r['law_variant']}",
                    f"T={r['test_t']}",
                    f"called_out={r['called_out']}",
                    settings_text(r),
                    f"finish={r['done_reason']}",
                ])
                row = {
                    "run_id": r["run_id"],
                    "date": r["timestamp_utc"][:10],
                    "condition": r["law_distance"],
                    "item_id": r["item_id"],
                    "model": model_text(r),
                    "temperature": r["temperature"],
                    "repeat": 1,
                    "prompt_id": r["prompt_id"],
                    "output": r["transcript"] if is_lab else r["response"],
                    "score": score,
                    "notes": notes,
                }
                rows.append(row)
                if evidence in PILOT:
                    pilot_rows.append(row)
                if evidence == "lab":
                    lab_rows.append(row)
                if evidence == "lab-rerun":
                    rerun_rows.append(row)
                if evidence in ("standard", "consistency"):
                    std_rows.append(row)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    with open(PILOT_APPEND, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=COLUMNS).writerows(pilot_rows)  # no header: for appending
    with open(LAB_APPEND, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=COLUMNS).writerows(lab_rows)  # no header: for appending
    with open(RERUN_APPEND, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=COLUMNS).writerows(rerun_rows)  # no header: for appending
    print(f"{len(rerun_rows)} lab rerun rows to {os.path.relpath(RERUN_APPEND, ROOT)}")
    with open(STD_APPEND, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=COLUMNS).writerows(std_rows)  # no header: for appending
    print(f"{len(std_rows)} consistency + Standard rows to {os.path.relpath(STD_APPEND, ROOT)}")
    print(f"Wrote {len(rows)} rows to {os.path.relpath(OUT, ROOT)}, {len(pilot_rows)} pilot rows to "
          f"{os.path.relpath(PILOT_APPEND, ROOT)} and {len(lab_rows)} lab rows to {os.path.relpath(LAB_APPEND, ROOT)} "
          f"(append files have no header)")


if __name__ == "__main__":
    main()
