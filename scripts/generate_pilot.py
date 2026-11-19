"""Generate the harder-evidence pilot items (see "Pilot: harder evidence" in PLAN.md).

Run from the repo root:
    python3 scripts/generate_pilot.py

Writes data/freefall_pilot_noisy.csv and data/freefall_pilot_sparse.csv.
Both reuse the Starter's 30 laws and test times from generate_items.py; only the
points shown change.

- Noisy: t = 1..6, each value times a factor drawn uniformly from [0.9, 1.1]
  (fixed seed), rounded to one decimal. The six factors depend only on the test
  time, so real, near and far items at the same T get the same noise.
- Sparse: t = 1..3, exact values.

Each item also records two reference answers computed from the points shown,
which are descriptive only and not part of the grading rule:
- t2_fit_answer: d = k t^2, k fitted by least squares
- quad_fit_answer: d = a t^2 + b t + c, least squares
"""

import csv
import os
import random

from generate_items import (CONDITIONS, PROMPT_TEMPLATE, REAL_K, fmt, formula_text, law)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = 20261118
NOISE = 0.10

COLUMNS = [
    "item_id", "domain", "evidence_level", "law_distance", "law_variant", "formula",
    "coefficient", "exponent", "table", "test_t", "cf_answer", "real_answer",
    "t2_fit_answer", "quad_fit_answer", "prompt_id", "prompt",
]


def solve3(m, v):
    """Solve a 3x3 linear system by Cramer's rule."""
    def det(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    d = det(m)
    out = []
    for col in range(3):
        mc = [row[:] for row in m]
        for r in range(3):
            mc[r][col] = v[r]
        out.append(det(mc) / d)
    return out


def t2_fit(ts, ds, T):
    k = sum(d * t * t for t, d in zip(ts, ds)) / sum(t ** 4 for t in ts)
    return k * T * T


def quad_fit(ts, ds, T):
    # Normal equations for d = a t^2 + b t + c.
    basis = [[t * t, t, 1.0] for t in ts]
    m = [[sum(row[i] * row[j] for row in basis) for j in range(3)] for i in range(3)]
    v = [sum(row[i] * d for row, d in zip(basis, ds)) for i in range(3)]
    a, b, c = solve3(m, v)
    return a * T * T + b * T + c


def noise_factors():
    rng = random.Random(SEED)
    return {T: [rng.uniform(1 - NOISE, 1 + NOISE) for _ in range(6)] for T in range(7, 17)}


def build(level):
    factors = noise_factors()
    times = [1, 2, 3, 4, 5, 6] if level == "noisy" else [1, 2, 3]
    tag = "NZ" if level == "noisy" else "SP"
    items = []
    for distance, code, specs in CONDITIONS:
        for i, (T, variant, coefficient, exponent) in enumerate(sorted(specs), start=1):
            if level == "noisy":
                shown = [round(law(coefficient, exponent, t) * f, 1) for t, f in zip(times, factors[T])]
            else:
                shown = [law(coefficient, exponent, t) for t in times]
            table = "\n".join(["Seconds | Meters"] + [f"{t} | {fmt(d)}" for t, d in zip(times, shown)])
            items.append({
                "item_id": f"FF{tag}-{code}-{i:02d}",
                "domain": "free_fall",
                "evidence_level": level,
                "law_distance": distance,
                "law_variant": variant,
                "formula": formula_text(coefficient, exponent),
                "coefficient": fmt(coefficient),
                "exponent": exponent,
                "table": "; ".join(f"{t}s: {fmt(d)}" for t, d in zip(times, shown)),
                "test_t": T,
                "cf_answer": fmt(law(coefficient, exponent, T)),
                "real_answer": fmt(law(REAL_K, 2, T)),
                "t2_fit_answer": fmt(t2_fit(times, shown, T)),
                "quad_fit_answer": fmt(quad_fit(times, shown, T)),
                "prompt_id": "P1",
                "prompt": PROMPT_TEMPLATE.replace("[TABLE]", table).replace("[T]", str(T)),
            })
    return items


def main():
    for level in ["noisy", "sparse"]:
        path = os.path.join(ROOT, "data", f"freefall_pilot_{level}.csv")
        items = build(level)
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(items)
        print(f"Wrote {len(items)} items to {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
