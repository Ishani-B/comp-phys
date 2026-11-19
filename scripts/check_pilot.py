"""Check the pilot data files independently of the generator.

Run from the repo root:
    python3 scripts/check_pilot.py

Checks both files have the Starter's 30 laws and test times, the noisy values sit
within +-10% of the law (plus rounding), the sparse values are exact, the answer
key comes from the noise-free law, and every law distance at the same test time
got the same noise. Exits non-zero on any failure.
"""

import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fail = []


def law_of(formula):
    m = re.fullmatch(r"d = ([\d.]+) \* t(?:\^(\d))?", formula)
    return float(m.group(1)), int(m.group(2) or 1)


starter = {(r["law_distance"], r["formula"], r["test_t"]): r
           for r in csv.DictReader(open(os.path.join(ROOT, "data", "freefall_starter.csv"), encoding="utf-8"))}

for level, times in [("noisy", [1, 2, 3, 4, 5, 6]), ("sparse", [1, 2, 3])]:
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data", f"freefall_pilot_{level}.csv"), encoding="utf-8")))
    if len(rows) != 30:
        fail.append(f"{level}: {len(rows)} items, expected 30")
    keys = {(r["law_distance"], r["formula"], r["test_t"]) for r in rows}
    if keys != set(starter):
        fail.append(f"{level}: laws/test times differ from the Starter")
    ratios_by_T = {}
    for r in rows:
        c, n = law_of(r["formula"])
        T = int(r["test_t"])
        shown = [(int(x.split("s: ")[0]), float(x.split(": ")[1])) for x in r["table"].split("; ")]
        if [t for t, _ in shown] != times:
            fail.append(f"{r['item_id']}: shows t={[t for t, _ in shown]}")
        for t, d in shown:
            true = c * t ** n
            if level == "sparse" and abs(d - true) > 1e-6:
                fail.append(f"{r['item_id']}: t={t} shows {d}, law gives {true}")
            if level == "noisy" and not (true * 0.9 - 0.05 <= d <= true * 1.1 + 0.05):
                fail.append(f"{r['item_id']}: t={t} shows {d}, outside +-10% of {true}")
        if abs(float(r["cf_answer"]) - c * T ** n) > 1e-6 or abs(float(r["real_answer"]) - 4.9 * T * T) > 1e-6:
            fail.append(f"{r['item_id']}: answer key wrong")
        if f"How far has it fallen at {T} seconds? End with 'Answer: X'." not in r["prompt"]:
            fail.append(f"{r['item_id']}: question line wrong")
        if level == "noisy":
            ratios_by_T.setdefault(T, []).append([d / (c * t ** n) for t, d in shown])
    if level == "noisy":
        # Same noise at the same test time across real/near/far (up to rounding to 0.1).
        for T, groups in ratios_by_T.items():
            for t_idx in range(6):
                vals = [g[t_idx] for g in groups]
                if t_idx >= 2 and max(vals) - min(vals) > 0.02:  # t=1,2 values are small, rounding dominates
                    fail.append(f"noisy T={T} t={t_idx + 1}: noise differs across law distances {vals}")

if fail:
    print(f"FAILED: {len(fail)} problem(s)")
    for f in fail:
        print(" -", f)
    sys.exit(1)
print("OK: both pilot files match the Starter laws, noise within +-10%, sparse exact, answer key correct.")
