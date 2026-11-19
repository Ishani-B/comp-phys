"""Summarize the virtual lab across its four cells (framing x readings).

Run from the repo root, after scoring each cell's run log with scripts/score.py:
    python3 scripts/compare_lab.py

Writes results/lab_comparison.md:
- the locked outcome per cell and law distance (mean normalized score, with
  median and counts; real-law items as number correct within 5%),
- how the model experimented (measurements, repeats, invalid and merged calls),
- how often its replies use physics words,
- for near and far episodes, which reference the answer is closest to: the
  data's law, Earth's law (4.9 T^2), the t^2 fit or the quadratic fit of the
  readings it actually got (the pre-registered second measure),
- the hand-coded "first hypothesis was t^2" share, if results/lab_coding.csv exists.
"""

import csv
import os
import re
import statistics
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELLS = [("physics", "exact"), ("physics", "noisy"), ("neutral", "exact"), ("neutral", "noisy")]
REFS = ["data law", "Earth's law", "t² fit", "quadratic fit"]
# Stricter than the run-time physics_words column: a bare "9.8" there also matched numbers like 19.8.
PHYSICS = re.compile(r"gravit|free.?fall|\\frac\{1\}\{2\}\s*g|physics|earth|(?<![\d.])9\.8(?![\d])\s*(m/s|\\text)", re.I)


def model_text(transcript):
    """The model's own words from a rendered transcript (multi-paragraph replies included)."""
    out, speaker = [], None
    for p in transcript.split("\n\n"):
        if p.startswith(("USER:", "TOOL:", "MODEL CALLS")):
            speaker = "other"
            continue
        if p.startswith("MODEL: "):
            speaker, p = "model", p[7:]
        if speaker == "model":
            out.append(p)
    return "\n\n".join(out)


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def closest(r):
    if r["answer_value"] == "":
        return "hedge"
    a = float(r["answer_value"])
    refs = {"data law": r["cf_answer"], "Earth's law": r["real_answer"],
            "t² fit": r["t2_fit_answer"], "quadratic fit": r["quad_fit_answer"]}
    dist = {k: abs(a - float(v)) / abs(float(v)) for k, v in refs.items() if v not in ("", None) and float(v) != 0}
    best = min(dist.values())
    winners = [k for k in REFS if k in dist and dist[k] - best <= 0.01]
    return " = ".join(winners)


def supplementary():
    """Pre-registered supplementary rerun of token-limited noisy episodes at a higher limit."""
    lines = []
    pairs = []
    for framing in ["physics", "neutral"]:
        orig_p = os.path.join(ROOT, "results", f"run_log_lab_{framing}_noisy_scored.csv")
        rer_p = os.path.join(ROOT, "results", f"run_log_lab_{framing}_noisy_cap16k_scored.csv")
        if os.path.exists(orig_p) and os.path.exists(rer_p):
            pairs.append((framing, load(orig_p), {r["item_id"]: r for r in load(rer_p)}))
    if not pairs:
        return lines
    lines += ["## Supplementary: token-limited episodes rerun at 16384 tokens\n",
              "Pre-registered in `PLAN.md`. The 4096-token results above stay primary. These are the same "
              "episodes rerun from the start with a higher per-turn limit.\n",
              "| Framing | Item | Law | Original | Rerun answer | Rerun label | Rerun score | Closest | Rerun measurements | Rerun output tokens | Finish |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    cell = ["", "### Noisy cells if rerun answers replace the hedges\n",
            "| Framing | Real-law control | Near: mean (median) | Near tracked | Far: mean (median) | Far tracked | Far leaked | Hedges left |",
            "|---|---|---|---|---|---|---|---|"]
    for framing, orig, rerun in pairs:
        merged = []
        for r in orig:
            rr = rerun.get(r["item_id"])
            if rr is not None:
                ans = f"{float(rr['answer_value']):g}" if rr["answer_value"] != "" else "none"
                lines.append(f"| {framing} | {r['item_id']} | {r['formula']} | {r['label']} | {ans} | {rr['label']} | "
                             f"{rr['norm_score'] or rr['pct_error']} | {closest(rr) if rr['law_distance'] != 'real' else ''} | "
                             f"{rr['n_measurements']} | {rr['output_tokens']} | {rr['done_reason']} |")
                merged.append(rr)
            else:
                merged.append(r)

        def by(d):
            return [x for x in merged if x["law_distance"] == d]

        def ms(rs):
            sc = [float(x["norm_score"]) for x in rs if x["norm_score"] != ""]
            return (f"{round(statistics.mean(sc), 2) + 0.0:.2f} ({round(statistics.median(sc), 2) + 0.0:.2f})"
                    if sc else "n/a")
        real, near, far = by("real"), by("near"), by("far")
        cell.append(f"| {framing} | {sum(x['label'] == 'correct' for x in real)}/{len(real)} | {ms(near)} | "
                    f"{sum(x['label'] == 'tracked' for x in near)}/{len(near)} | {ms(far)} | "
                    f"{sum(x['label'] == 'tracked' for x in far)}/{len(far)} | {sum(x['label'] == 'leaked' for x in far)} | "
                    f"{sum(x['label'] == 'hedge' for x in merged)} |")
    return lines + cell + [""]


def main():
    coding = {}
    cpath = os.path.join(ROOT, "results", "lab_coding.csv")
    if os.path.exists(cpath):
        coding = {(r["framing"], r["readings"], r["item_id"]): r for r in load(cpath)}

    out = ["# Virtual lab: Gemma 4 31B runs its own experiments\n",
           "Normalized score: 0 = followed the world's law, 1 = gave Earth's answer. "
           "Real-law items: number correct within 5%. 10 episodes per row; exploratory, no significance claims.\n",
           "## Locked outcome\n",
           "| Framing | Readings | Real-law control | Near: mean (median) | Near tracked | Far: mean (median) | Far tracked | Far leaked | Hedges | Called out |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    behaviour = ["## How it experimented\n",
                 "| Framing | Readings | Mean measurements | Episodes with repeats | Invalid calls | Merged calls | Mean turns | Replies mentioning real physics | Far: first hypothesis t² (read by hand) |",
                 "|---|---|---|---|---|---|---|---|---|"]
    refs_tbl = ["## Which reference near and far answers land closest to\n",
                "Ties within 1% are joined with \"=\". For near laws the data's law, the t² fit and often the quadratic fit coincide, "
                "so the informative rows are far.\n",
                "| Framing | Readings | Distance | " + " | ".join(REFS) + " | Ties / other | Hedge |",
                "|---|---|---|" + "---|" * (len(REFS) + 2)]
    detail = ["## Every far episode\n",
              "| Framing | Readings | Item | Law | T | Measured at | Answer | Data law | Earth | t² fit | Quad fit | Closest | Score |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for framing, readings in CELLS:
        path = os.path.join(ROOT, "results", f"run_log_lab_{framing}_{readings}_scored.csv")
        if not os.path.exists(path):
            out.append(f"| {framing} | {readings} | not run | | | | | | | |")
            continue
        rows = load(path)

        def by(d):
            return [r for r in rows if r["law_distance"] == d]

        def ms(rs):
            sc = [float(r["norm_score"]) for r in rs if r["norm_score"] != ""]
            def r2(x):
                return round(x, 2) + 0.0  # avoid printing -0.00
            return f"{r2(statistics.mean(sc)):.2f} ({r2(statistics.median(sc)):.2f})" if sc else "n/a"

        real, near, far = by("real"), by("near"), by("far")
        out.append(f"| {framing} | {readings} | {sum(r['label'] == 'correct' for r in real)}/{len(real)} | {ms(near)} | "
                   f"{sum(r['label'] == 'tracked' for r in near)}/{len(near)} | {ms(far)} | "
                   f"{sum(r['label'] == 'tracked' for r in far)}/{len(far)} | {sum(r['label'] == 'leaked' for r in far)} | "
                   f"{sum(r['label'] == 'hedge' for r in rows)} | {sum(r['called_out'] == 'yes' for r in rows)}"
                   f"{' (+' + str(sum(r['called_out'] == 'borderline' for r in rows)) + ' borderline)' if any(r['called_out'] == 'borderline' for r in rows) else ''} |")

        first = [coding.get((framing, readings, r["item_id"]), {}).get("first_hypothesis_t2", "") for r in far]
        first_txt = f"{sum(x == 'yes' for x in first)}/{sum(x in ('yes', 'no') for x in first)}" if any(first) else "not coded"
        physics_n = sum(bool(PHYSICS.search(model_text(r["transcript"]))) for r in rows)
        behaviour.append(
            f"| {framing} | {readings} | {statistics.mean(int(r['n_measurements']) for r in rows):.1f} | "
            f"{sum(int(r['n_repeats']) > 0 for r in rows)}/{len(rows)} | {sum(int(r['n_invalid']) for r in rows)} | "
            f"{sum(int(r['n_merged_calls']) for r in rows)} | {statistics.mean(int(r['n_turns']) for r in rows):.1f} | "
            f"{physics_n}/{len(rows)} | {first_txt} |")

        for d, rs in [("near", near), ("far", far)]:
            c = Counter(closest(r) for r in rs)
            other = sum(v for k, v in c.items() if k not in REFS and k != "hedge")
            refs_tbl.append(f"| {framing} | {readings} | {d} | " + " | ".join(str(c.get(k, 0)) for k in REFS)
                            + f" | {other} | {c.get('hedge', 0)} |")
        for r in far:
            times = ", ".join(f"{t:g}" for t, _ in __import__("json").loads(r["measurements"]))
            ans = f"{float(r['answer_value']):g}" if r["answer_value"] != "" else "hedge"
            detail.append(f"| {framing} | {readings} | {r['item_id']} | {r['formula']} | {r['test_t']} | {times} | {ans} | "
                          f"{r['cf_answer']} | {r['real_answer']} | {r['t2_fit_answer']} | {r['quad_fit_answer']} | "
                          f"{closest(r)} | {r['norm_score']} |")

    supp = supplementary()
    text = "\n".join(out + [""] + behaviour + [""] + refs_tbl + [""] + supp + detail) + "\n"
    dest = os.path.join(ROOT, "results", "lab_comparison.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    main()
