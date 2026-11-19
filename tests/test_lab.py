"""Tests for the virtual lab's measurement rules (no API calls).

Run from the repo root:
    python3 -m unittest discover tests
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from lab import BUDGET, World, noise_factor, split_tool_calls  # noqa: E402


def tc(args, id_="c1", name="drop_ball"):
    return {"id": id_, "function": {"name": name, "arguments": args}}


class SplitToolCalls(unittest.TestCase):
    def test_merged_calls_are_split(self):
        calls, merged = split_tool_calls([tc('{"seconds": 1}{"seconds": 2}')])
        self.assertEqual(merged, 1)
        self.assertEqual([c["id"] for c in calls], ["c1_1", "c1_2"])
        self.assertEqual([json.loads(c["arguments"]) for c in calls], [{"seconds": 1}, {"seconds": 2}])

    def test_single_call_unchanged(self):
        calls, merged = split_tool_calls([tc('{"seconds": 3.5}')])
        self.assertEqual((merged, len(calls), calls[0]["id"]), (0, 1, "c1"))

    def test_bad_json_echoed_as_empty_object(self):
        calls, _ = split_tool_calls([tc('{"seconds": 3')])
        self.assertEqual(calls[0]["arguments"], "{}")      # valid JSON to echo back
        self.assertEqual(calls[0]["raw"], '{"seconds": 3')  # original kept so the lab rejects it

    def test_empty_arguments(self):
        calls, _ = split_tool_calls([tc("")])
        self.assertEqual(calls[0]["arguments"], "{}")


class LabRules(unittest.TestCase):
    def test_exact_reading(self):
        w = World(2.5, 2, 8, "physics", noisy=False)
        self.assertEqual(w.measure('{"seconds": 2}'), {"seconds": 2.0, "meters": 10.0, "measurements_left": 7})

    def test_neutral_names(self):
        w = World(2.5, 2, 8, "neutral", noisy=False)
        self.assertEqual(w.measure({"tocks": 2}), {"tocks": 2.0, "glims": 10.0, "readings_left": 7})

    def test_window_rejected_and_free(self):
        w = World(1, 3, 9, "physics", noisy=False)
        for bad in ['{"seconds": 0}', '{"seconds": 6.5}', '{"seconds": -1}', '{"seconds": "abc"}', "not json"]:
            self.assertIn("error", w.measure(bad))
        self.assertEqual(len(w.readings), 0)          # rejected calls use no budget
        self.assertEqual(w.invalid, 5)
        self.assertIn("meters", w.measure('{"seconds": 6}'))  # 6 itself is allowed

    def test_budget(self):
        w = World(1, 2, 9, "physics", noisy=False)
        for i in range(BUDGET):
            self.assertIn("meters", w.measure({"seconds": 1 + i * 0.5}))
        self.assertEqual(w.measure({"seconds": 1}), {"error": "No measurements left. Give your answer."})
        self.assertEqual(len(w.readings), BUDGET)

    def test_misnamed_argument_accepted(self):
        w = World(4.9, 2, 9, "physics", noisy=False)
        self.assertEqual(w.measure('{"time": 2}')["meters"], 19.6)

    def test_rounding(self):
        w = World(4.9, 2, 9, "physics", noisy=False)
        r = w.measure({"seconds": 1.23456})
        self.assertEqual(r["seconds"], 1.23)
        self.assertEqual(r["meters"], round(4.9 * 1.23 ** 2, 3))

    def test_noise_within_10_percent_and_fresh_per_reading(self):
        w = World(2, 3, 12, "physics", noisy=True)
        a, b = w.measure({"seconds": 3})["meters"], w.measure({"seconds": 3})["meters"]
        for v in (a, b):
            self.assertTrue(54 * 0.9 - 0.001 <= v <= 54 * 1.1 + 0.001)
        self.assertNotEqual(a, b)                      # a repeat gets a new draw

    def test_noise_matched_across_framings_and_laws(self):
        # Same T, same reading number -> same factor, whatever the framing or law.
        phys = World(2.5, 2, 8, "physics", noisy=True)
        neut = World(2.5, 2, 8, "neutral", noisy=True)
        far = World(2, 3, 8, "physics", noisy=True)
        p = phys.measure({"seconds": 2})["meters"] / 10.0
        n = neut.measure({"tocks": 2})["glims"] / 10.0
        f = far.measure({"seconds": 2})["meters"] / 16.0
        self.assertAlmostEqual(p, n, places=3)
        self.assertAlmostEqual(p, f, places=3)
        self.assertAlmostEqual(p, noise_factor(8, 1), places=3)

    def test_noise_differs_by_test_time(self):
        self.assertNotEqual(noise_factor(8, 1), noise_factor(9, 1))


if __name__ == "__main__":
    unittest.main()
