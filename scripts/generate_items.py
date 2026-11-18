"""Generate the Starter items for the counterfactual free-fall study.

Run from the repo root:
    python3 scripts/generate_items.py

Writes data/freefall_starter.csv. There is no randomness: every item is listed
below, so the same file comes out every time. The answer key is computed from
the formula that generated each table.

Design (Starter): 1 domain (free-fall) x 3 law distances x 10 test predictions.
- The table always shows t = 1..6 seconds.
- Every condition asks about the same 10 test times, T = 7..16, one item per
  time, so the only thing that changes between conditions is the law.
- Near (changed constant): 5 items with a smaller constant, 5 with a larger one.
- Far (changed exponent or form): 5 items with d = c*t^3, 5 with d = c*t.
- Sub-variants are split across test times so their mean T is as close as
  possible (57 vs 58), and the 5 sample items in the data plan are included
  exactly as written.
"""

import csv
import os

REAL_K = 4.9  # real free-fall: d = 1/2 * 9.8 * t^2 = 4.9 t^2
TABLE_TIMES = [1, 2, 3, 4, 5, 6]
TEST_TIMES = list(range(7, 17))  # 7..16, shared by all three conditions
PROMPT_ID = "P1"

PROMPT_TEMPLATE = (
    "A ball is dropped on a planet. The table shows how far it has fallen "
    "(meters) after each number of seconds.\n"
    "\n"
    "[TABLE]\n"
    "\n"
    "How far has it fallen at [T] seconds? End with 'Answer: X'."
)

# (test time, variant, coefficient, exponent). d = coefficient * t ** exponent
REAL_ITEMS = [(t, "real", REAL_K, 2) for t in TEST_TIMES]

NEAR_ITEMS = [
    (7, "near_smaller_constant", 2.0, 2),
    (8, "near_smaller_constant", 2.5, 2),   # sample item 2
    (9, "near_larger_constant", 7.0, 2),
    (10, "near_larger_constant", 8.0, 2),  # sample item 3
    (11, "near_smaller_constant", 1.5, 2),
    (12, "near_larger_constant", 9.0, 2),
    (13, "near_larger_constant", 10.0, 2),
    (14, "near_larger_constant", 12.0, 2),
    (15, "near_smaller_constant", 3.0, 2),
    (16, "near_smaller_constant", 1.2, 2),
]

FAR_ITEMS = [
    (7, "far_changed_exponent", 3.0, 3),
    (8, "far_changed_exponent", 2.0, 3),   # sample item 4
    (9, "far_changed_form", 12.0, 1),      # sample item 5
    (10, "far_changed_form", 15.0, 1),
    (11, "far_changed_exponent", 1.0, 3),
    (12, "far_changed_form", 10.0, 1),
    (13, "far_changed_form", 20.0, 1),
    (14, "far_changed_form", 8.0, 1),
    (15, "far_changed_exponent", 0.5, 3),
    (16, "far_changed_exponent", 1.5, 3),
]

CONDITIONS = [("real", "R", REAL_ITEMS), ("near", "N", NEAR_ITEMS), ("far", "F", FAR_ITEMS)]

COLUMNS = [
    "item_id", "domain", "law_distance", "law_variant", "formula",
    "coefficient", "exponent", "table", "test_t",
    "cf_answer", "real_answer", "prompt_id", "prompt",
]


def law(coefficient, exponent, t):
    return round(coefficient * t ** exponent, 4)


def fmt(x):
    """Plain decimal, no trailing zeros, no scientific notation: 240.1, 72, 0.5."""
    s = f"{round(x, 4):.4f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def formula_text(coefficient, exponent):
    return f"d = {fmt(coefficient)} * t^{exponent}" if exponent != 1 else f"d = {fmt(coefficient)} * t"


def render_table(coefficient, exponent):
    rows = ["Seconds | Meters"]
    rows += [f"{t} | {fmt(law(coefficient, exponent, t))}" for t in TABLE_TIMES]
    return "\n".join(rows)


def render_prompt(coefficient, exponent, test_t):
    return (PROMPT_TEMPLATE
            .replace("[TABLE]", render_table(coefficient, exponent))
            .replace("[T]", str(test_t)))


def build_items():
    items = []
    for distance, code, specs in CONDITIONS:
        for i, (test_t, variant, coefficient, exponent) in enumerate(sorted(specs), start=1):
            items.append({
                "item_id": f"FF-{code}-{i:02d}",
                "domain": "free_fall",
                "law_distance": distance,
                "law_variant": variant,
                "formula": formula_text(coefficient, exponent),
                "coefficient": fmt(coefficient),
                "exponent": exponent,
                "table": "; ".join(f"{t}s: {fmt(law(coefficient, exponent, t))}" for t in TABLE_TIMES),
                "test_t": test_t,
                "cf_answer": fmt(law(coefficient, exponent, test_t)),
                "real_answer": fmt(law(REAL_K, 2, test_t)),
                "prompt_id": PROMPT_ID,
                "prompt": render_prompt(coefficient, exponent, test_t),
            })
    return items


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(root, "data", "freefall_starter.csv")
    items = build_items()
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(items)
    print(f"Wrote {len(items)} items to {os.path.relpath(out_path, root)}")


if __name__ == "__main__":
    main()
