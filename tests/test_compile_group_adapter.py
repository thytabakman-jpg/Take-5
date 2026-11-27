"""Integration regressions for the real Compile/ICC component binding.

Run: python tests/test_compile_group_adapter.py
Requires Python 3.10+, Node 18+, and the canonical runtime source files.
No network access or Git writes occur.
"""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from compile_group_adapter import frontier, prepare_group, verify_group


class CompileBindingTests(unittest.TestCase):
    def setUp(self):
        self.a = "o/r:old.md"
        self.b = "o/r:keep.md"
        self.c = "o/r:index.md"
        self.before = {self.a: "Historical research.\n",
                       self.b: "# Owner\n\nCurrent research.\n",
                       self.c: "[Research](old.md)\n"}
        self.packet = {"authority": "fixture", "revision": "a" * 40,
                       "before": self.before, "survivor": self.b,
                       "moves": {self.a: self.b}}

    def test_independent_work_and_prerequisites(self):
        groups = [{"id": "A", "authority": "fixture"},
                  {"id": "B", "authority": "fixture"}]
        self.assertEqual(frontier(groups, ["A:discovered"])["ready"],
                         ["A:prepare"])
        self.assertEqual(frontier(groups, ["A:discovered", "A:prepare",
                                          "A:reconstructed", "B:discovered"])["ready"],
                         ["A:verify", "B:prepare"])
        self.assertEqual(frontier([{"id": "C"}], ["C:discovered"])["ready"], [])

    def test_actual_working_map_and_preservation(self):
        p = prepare_group(self.packet)
        self.assertEqual(p["step2"][self.b],
                         self.before[self.b] + "\n\n" + self.before[self.a])
        self.assertEqual(p["step2"][self.a], self.before[self.a])
        self.assertNotIn(self.a, p["after"])
        self.assertEqual(p["after"][self.c], "[Research](keep.md)\n")
        self.assertEqual(p["working_closure"]["status"], "CLOSED")
        self.assertEqual(p["working_closure"]["settled_count"],
                         p["working_closure"]["harvest_count"])
        self.assertEqual(len(p["source_boundaries"]), 2)
        v = verify_group({**self.packet, "after": p["after"],
                          "decomposition": p["decomposition"],
                          "retire": [self.a], "allowedChanges": [self.b, self.c],
                          "sourceRevisions": {"o/r": "a" * 40},
                          "requireProvenance": True,
                          "scopeReview": {"complete": True,
                                          "evidence": "All three fixture paths checked."}})
        self.assertEqual(v["dependency"]["status"], "SUPPORTED_REFERENCES_VERIFIED")
        self.assertEqual(v["verification"]["status"], "READY_FOR_PUBLICATION",
                         v["verification"]["issues"])

    def test_missing_review_and_broken_reference_block_publication(self):
        p = prepare_group(self.packet)
        candidate = dict(p["after"])
        candidate[self.c] = self.before[self.c]
        v = verify_group({**self.packet, "after": candidate,
                          "decomposition": p["decomposition"],
                          "retire": [self.a], "allowedChanges": [self.b, self.c],
                          "sourceRevisions": {"o/r": "a" * 40},
                          "requireProvenance": True})
        self.assertEqual(v["verification"]["status"], "OPEN")

    def test_missing_authority_and_invalid_survivor(self):
        with self.assertRaises(ValueError):
            prepare_group({**self.packet, "authority": ""})
        with self.assertRaises(ValueError):
            prepare_group({**self.packet, "survivor": self.a})


if __name__ == "__main__":
    unittest.main()
