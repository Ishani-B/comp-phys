"""Check data/freefall_starter.csv independently of the generator.

Run from the repo root:
    python3 scripts/check_items.py

Recomputes every answer from the stated formula, checks the table and prompt,
checks the design is balanced, and checks the 5 sample items from the data plan
appear with exactly the answers written there. Exits non-zero on any failure.
"""

import csv
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "freefall_starter.csv")

# The 5 sample items exactly as written in the data plan:
# (law_distance, formula, T, table values, correct answer, real-world answer)
SAMPLES = [
    ("real", "d = 4.9 * t^2", 8, [4.9, 19.6, 44.1, 78.4, 122.5, 176.4], 313.6, 313.6),
    ("near", "d = 2.5 * t^2", 8, [2.5, 10, 22.5, 40, 62.5, 90], 160, 313.6),
    ("near", "d = 8 * t^2", 10, [8, 32, 72, 128, 200, 288], 800, 490),
    ("far", "d = 2 * t^3", 8, [2, 16, 54, 128, 250, 432], 1024, 313.6),
    ("far", "d = 12 * t", 9, [12, 24, 36, 48, 60, 72], 108, 396.9),
]

failures = []


def check(ok, msg):
    if not ok:
        failures.append(msg)


def close(a, b):
    return abs(a - b) < 1e-6


def parse_formula(s):
    m = re.fullmatch(r"d = ([\d.]+) \* t(?:\^(\d))?", s)
    return float(m.group(1)), int(m.group(2) or 1)


with open(PATH, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

check(len(rows) == 30, f"expected 30 items, found {len(rows)}")
check(len({r["item_id"] for r in rows}) == len(rows), "item_id values are not unique")
check(Counter(r["law_distance"] for r in rows) == {"real": 10, "near": 10, "far": 10},
      "expected 10 items per law distance")

for r in rows:
    iid = r["item_id"]
    c, n = parse_formula(r["formula"])
    T = int(r["test_t"])
    table = [float(x.split(": ")[1]) for x in r["table"].split("; ")]
    check(len(table) == 6, f"{iid}: table does not have 6 points")
    for t, d in zip(range(1, 7), table):
        check(close(d, c * t ** n), f"{iid}: table value at t={t} is {d}, formula gives {c * t ** n}")
    check(T not in range(1, 7), f"{iid}: test time {T} is already in the table")
    check(close(float(r["cf_answer"]), c * T ** n), f"{iid}: cf_answer wrong")
    check(close(float(r["real_answer"]), 4.9 * T ** 2), f"{iid}: real_answer wrong")
    if r["law_distance"] == "real":
        check((c, n) == (4.9, 2), f"{iid}: real item does not use d = 4.9 t^2")
    elif r["law_distance"] == "near":
        check(n == 2 and c != 4.9, f"{iid}: near item must change only the constant")
        ratio = c / 4.9
        check(ratio <= 0.65 or ratio >= 1.4, f"{iid}: near constant too close to real (ratio {ratio:.2f})")
    else:
        check(n != 2, f"{iid}: far item must change the exponent or form")
    p = r["prompt"]
    check(p.startswith("A ball is dropped on a planet."), f"{iid}: prompt opening changed")
    check(f"How far has it fallen at {T} seconds? End with 'Answer: X'." in p, f"{iid}: question line wrong")
    check(len(p.split("\n")) == 11, f"{iid}: prompt layout changed (expected 11 lines)")
    for word in ["gravity", "free fall", "free-fall", "acceleration", "physics", "Earth"]:
        check(word.lower() not in p.lower(), f"{iid}: prompt contains physics term '{word}'")

# Every condition uses the same test times.
for distance in ["real", "near", "far"]:
    ts = sorted(int(r["test_t"]) for r in rows if r["law_distance"] == distance)
    check(ts == list(range(7, 17)), f"{distance}: test times are {ts}, expected 7..16")

# Sample items from the data plan.
for distance, formula, T, table, cf, real in SAMPLES:
    match = [r for r in rows if r["law_distance"] == distance and r["formula"] == formula
             and int(r["test_t"]) == T]
    if not match:
        failures.append(f"sample item missing: {distance} {formula} T={T}")
        continue
    r = match[0]
    got_table = [float(x.split(": ")[1]) for x in r["table"].split("; ")]
    check(all(close(a, b) for a, b in zip(got_table, table)), f"sample {formula}: table differs from plan")
    check(close(float(r["cf_answer"]), cf), f"sample {formula}: correct answer {r['cf_answer']} != plan {cf}")
    check(close(float(r["real_answer"]), real), f"sample {formula}: real answer {r['real_answer']} != plan {real}")

if failures:
    print(f"FAILED: {len(failures)} problem(s)")
    for msg in failures:
        print(" -", msg)
    sys.exit(1)
print(f"OK: {len(rows)} items checked, all 5 sample items match the plan.")
