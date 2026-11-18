"""Tests for the answer parser and the locked grading rule.

Run from the repo root:
    python3 -m unittest discover tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from score import extract_answer, score_row  # noqa: E402


def row(distance, response, cf, real):
    return {"law_distance": distance, "response": response, "cf_answer": str(cf), "real_answer": str(real)}


class ExtractAnswer(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(extract_answer("blah\nAnswer: 313.6"), (313.6, "ok"))

    def test_units_and_bold(self):
        self.assertEqual(extract_answer("**Answer: 160 meters**"), (160.0, "ok"))
        self.assertEqual(extract_answer("Answer: **1,024**"), (1024.0, "ok"))

    def test_number_on_next_line(self):
        self.assertEqual(extract_answer("**Answer:**\n800"), (800.0, "ok"))

    def test_last_answer_counts(self):
        self.assertEqual(extract_answer("I will end with Answer: X.\nWork...\nAnswer: 108"), (108.0, "ok"))

    def test_final_answer_and_case(self):
        self.assertEqual(extract_answer("Final answer: 396.9 m"), (396.9, "ok"))

    def test_no_answer_line(self):
        self.assertEqual(extract_answer("It has fallen 313.6 meters."), (None, "no_answer_line"))

    def test_non_numeric(self):
        self.assertEqual(extract_answer("Answer: X"), (None, "non_numeric"))
        self.assertEqual(extract_answer("Answer: I cannot determine this."), (None, "non_numeric"))


class ScoreRow(unittest.TestCase):
    def test_counterfactual_correct_is_zero(self):
        r = score_row(row("near", "Answer: 160", 160, 313.6))
        self.assertEqual((r["norm_score"], r["label"]), (0.0, "tracked"))

    def test_real_world_answer_is_one(self):
        r = score_row(row("far", "Answer: 313.6", 1024, 313.6))
        self.assertEqual((r["norm_score"], r["label"]), (1.0, "leaked"))

    def test_halfway_records_exact_score(self):
        r = score_row(row("near", "Answer: 645", 800, 490))  # (645-800)/(490-800) = 0.5
        self.assertEqual((r["norm_score"], r["label"]), (0.5, "between"))

    def test_boundaries(self):
        self.assertEqual(score_row(row("near", "Answer: 190.72", 160, 313.6))["label"], "tracked")   # 0.2
        self.assertEqual(score_row(row("near", "Answer: 282.88", 160, 313.6))["label"], "leaked")    # 0.8

    def test_outside_range_flagged(self):
        r = score_row(row("near", "Answer: 0", 160, 313.6))  # score -1.04
        self.assertEqual((r["label"], r["outside_0_1"]), ("tracked", "yes"))

    def test_hedge(self):
        self.assertEqual(score_row(row("far", "I can't tell.", 108, 396.9))["label"], "hedge")

    def test_real_within_5_percent(self):
        self.assertEqual(score_row(row("real", "Answer: 320", 313.6, 313.6))["label"], "correct")   # 2.0%
        self.assertEqual(score_row(row("real", "Answer: 340", 313.6, 313.6))["label"], "incorrect")  # 8.4%


if __name__ == "__main__":
    unittest.main()
