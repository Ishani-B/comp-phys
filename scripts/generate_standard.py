"""Generate the Standard run's Hooke's-law and Kepler items (see "Standard run" in PLAN.md).

Run from the repo root:
    python3 scripts/generate_standard.py

Writes data/hooke_standard.csv and data/kepler_standard.csv. No randomness.
Free fall reuses data/freefall_starter.csv unchanged.

Both domains copy the Starter's structure: 6 table points at x = 1..6 (scaled),
10 test points at x = 7..16, 10 items per law distance, and sub-variants split
across test points the same way. The law is y = c * (x / scale) ** p.

Hooke: weights 100..600 g in the table, 700..1600 g asked; stretch in cm.
  real p = 1, near p = 0.7 or 1.4, far p = 0.5 or 2.
Kepler: distances 10..60 thousand km in the table, 70..160 asked; days per circle.
  real p = 1.5, near p = 1.2 or 1.8, far p = 1 or 3.
Near exponents were chosen so the two reference answers differ by at least 10%
on every item (1.25/1.75 left one Kepler item at 9%).

There is no single real-world constant for either law, so the "real-world
answer" is the real law's form with its constant fitted (least squares) to the
points shown: a straight line through zero for Hooke, c * r^1.5 for Kepler.
Shown values are rounded to 2 decimals; answers come from the exact law.
"""

import csv
import os

from generate_items import fmt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE_X = [1, 2, 3, 4, 5, 6]
SMALL_GROUP = [7, 8, 11, 15, 16]   # same split as the Starter (sums 57 / 58)
LARGE_GROUP = [9, 10, 12, 13, 14]
CONSTANTS = [1.2, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]  # value at x = 1, one per item

DOMAINS = {
    "hooke": {
        "code": "HK", "scale": 100, "unit_x": "grams", "real_p": 1.0,
        "near": {"smaller": 0.7, "larger": 1.4}, "far": {"small_group": 2.0, "large_group": 0.5},
        "far_names": {"small_group": "far_quadratic", "large_group": "far_square_root"},
        "prompt_id": "P4",
        "prompt": ("Weights are hung from a spring. The table shows how far the spring stretches "
                   "(centimeters) for each weight (grams).\n\n[TABLE]\n\n"
                   "How far will it stretch with [X] grams? End with 'Answer: X'."),
        "header": "Grams | Centimeters",
    },
    "kepler": {
        "code": "KP", "scale": 10, "unit_x": "thousand km", "real_p": 1.5,
        "near": {"smaller": 1.2, "larger": 1.8}, "far": {"small_group": 3.0, "large_group": 1.0},
        "far_names": {"small_group": "far_cubic", "large_group": "far_linear"},
        "prompt_id": "P5",
        "prompt": ("Moons travel in circles around a planet. The table shows how many days one full "
                   "circle takes for a moon at each distance from the planet (thousands of kilometers)."
                   "\n\n[TABLE]\n\n"
                   "How many days does one full circle take at [X] thousand kilometers? End with 'Answer: X'."),
        "header": "Thousand km | Days",
    },
}

COLUMNS = ["item_id", "domain", "law_distance", "law_variant", "formula", "coefficient", "exponent",
           "table", "test_x", "test_t", "cf_answer", "real_answer", "prompt_id", "prompt"]


def law(c, p, x):
    return c * x ** p  # x in units of `scale` (1..16)


def familiar_fit(xs, ys, real_p, x_test):
    """Least-squares constant for y = k * x^real_p through the shown points, evaluated at x_test."""
    k = sum(y * x ** real_p for x, y in zip(xs, ys)) / sum(x ** (2 * real_p) for x in xs)
    return k * x_test ** real_p


def specs(d):
    """(test x, law_distance, variant, exponent) for the 30 items of a domain."""
    out = [(x, "real", "real", d["real_p"]) for x in range(7, 17)]
    out += [(x, "near", "near_smaller_exponent", d["near"]["smaller"]) for x in SMALL_GROUP]
    out += [(x, "near", "near_larger_exponent", d["near"]["larger"]) for x in LARGE_GROUP]
    out += [(x, "far", d["far_names"]["small_group"], d["far"]["small_group"]) for x in SMALL_GROUP]
    out += [(x, "far", d["far_names"]["large_group"], d["far"]["large_group"]) for x in LARGE_GROUP]
    return out


def build(name):
    d = DOMAINS[name]
    items = []
    for distance in ["real", "near", "far"]:
        rows = sorted(s for s in specs(d) if s[1] == distance)
        for i, (x, _, variant, p) in enumerate(rows, start=1):
            c = CONSTANTS[i - 1]
            shown = [round(law(c, p, t), 2) for t in TABLE_X]
            scale = d["scale"]
            table_txt = "\n".join([d["header"]] + [f"{t * scale} | {fmt(v)}" for t, v in zip(TABLE_X, shown)])
            cf = law(c, p, x)
            real = familiar_fit(TABLE_X, shown, d["real_p"], x)
            items.append({
                "item_id": f"{d['code']}-{distance[0].upper()}-{i:02d}",
                "domain": name,
                "law_distance": distance,
                "law_variant": variant,
                "formula": f"y = {fmt(c)} * (x/{scale})^{fmt(p)}",
                "coefficient": fmt(c),
                "exponent": fmt(p),
                "table": "; ".join(f"{t * scale}: {fmt(v)}" for t, v in zip(TABLE_X, shown)),
                "test_x": x * scale,
                "test_t": x,  # the scaled test point (7..16), same role as the Starter's T
                "cf_answer": fmt(cf),
                "real_answer": fmt(real),
                "prompt_id": d["prompt_id"],
                "prompt": d["prompt"].replace("[TABLE]", table_txt).replace("[X]", str(x * scale)),
            })
    return items


def main():
    for name in DOMAINS:
        items = build(name)
        path = os.path.join(ROOT, "data", f"{name}_standard.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(items)
        gaps = [abs(float(i["real_answer"]) - float(i["cf_answer"])) / float(i["cf_answer"])
                for i in items if i["law_distance"] != "real"]
        print(f"Wrote {len(items)} items to {os.path.relpath(path, ROOT)}; "
              f"smallest gap between the two reference answers: {min(gaps):.0%}")


if __name__ == "__main__":
    main()
