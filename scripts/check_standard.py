"""Check the Standard run's Hooke and Kepler data independently of the generator.

Run from the repo root:
    python3 scripts/check_standard.py

Recomputes every table value, the data's answer, and the familiar-form answer
(least-squares fit of the real law's form to the shown points); checks the
design (10 items per distance, test points 7..16 x scale, sub-variant split),
that the two reference answers differ by at least 10% on every near/far item,
and that no prompt uses physics vocabulary. Exits non-zero on any failure.
"""

import csv
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAINS = {"hooke": (100, 1.0, "P4"), "kepler": (10, 1.5, "P5")}
BANNED = ["hooke", "kepler", "orbit", "gravity", "gravitational", "elastic", "force", "period",
          "physics", "newton", "constant", "law"]
fail = []

for name, (scale, real_p, pid) in DOMAINS.items():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data", f"{name}_standard.csv"), encoding="utf-8")))
    if len(rows) != 30 or Counter(r["law_distance"] for r in rows) != {"real": 10, "near": 10, "far": 10}:
        fail.append(f"{name}: wrong item counts")
    for d in ["real", "near", "far"]:
        xs = sorted(int(r["test_x"]) for r in rows if r["law_distance"] == d)
        if xs != [x * scale for x in range(7, 17)]:
            fail.append(f"{name} {d}: test points {xs}")
    for r in rows:
        m = re.fullmatch(r"y = ([\d.]+) \* \(x/(\d+)\)\^([\d.]+)", r["formula"])
        c, sc, p = float(m.group(1)), int(m.group(2)), float(m.group(3))
        if sc != scale:
            fail.append(f"{r['item_id']}: scale {sc}")
        pts = [(int(a.split(": ")[0]), float(a.split(": ")[1])) for a in r["table"].split("; ")]
        if [x for x, _ in pts] != [k * scale for k in range(1, 7)]:
            fail.append(f"{r['item_id']}: table x values")
        for x, y in pts:
            if abs(y - round(c * (x / scale) ** p, 2)) > 1e-9:
                fail.append(f"{r['item_id']}: table value at {x}")
        xt = int(r["test_x"]) / scale
        if abs(float(r["cf_answer"]) - c * xt ** p) > 1e-3:
            fail.append(f"{r['item_id']}: cf_answer")
        u = [x / scale for x, _ in pts]
        k = sum(y * ui ** real_p for ui, (_, y) in zip(u, pts)) / sum(ui ** (2 * real_p) for ui in u)
        if abs(float(r["real_answer"]) - k * xt ** real_p) > 1e-3:
            fail.append(f"{r['item_id']}: real_answer")
        if r["law_distance"] == "real" and abs(p - real_p) > 1e-9:
            fail.append(f"{r['item_id']}: real item exponent {p}")
        if r["law_distance"] != "real":
            gap = abs(float(r["real_answer"]) - float(r["cf_answer"])) / float(r["cf_answer"])
            if gap < 0.10:
                fail.append(f"{r['item_id']}: reference answers only {gap:.0%} apart")
        if r["prompt_id"] != pid or "End with 'Answer: X'." not in r["prompt"] or str(r["test_x"]) not in r["prompt"]:
            fail.append(f"{r['item_id']}: prompt")
        for word in BANNED:
            if re.search(rf"\b{word}\b", r["prompt"], re.I):
                fail.append(f"{r['item_id']}: prompt contains '{word}'")

if fail:
    print(f"FAILED: {len(fail)} problem(s)")
    for f in fail:
        print(" -", f)
    sys.exit(1)
print("OK: Hooke and Kepler items match their laws, fits recomputed, every near/far gap >= 10%, no physics vocabulary.")
