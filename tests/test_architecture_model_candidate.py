import random
import unittest
from itertools import combinations, product
from architecture_model_candidate import search_model


class ModelCandidateTests(unittest.TestCase):
    def run_model(self, **changes):
        args = dict(domains={'a': ('0', '1'), 'b': ('0', '1'), 'p': ('0', '1')},
                    writable=('a', 'b', 'p'), baselines={'c': {'a': '0', 'b': '0', 'p': '1'}},
                    obligations={'joint': ({'a': '1', 'b': '1'},)},
                    protected={'keep': ({'p': '1'},)}, admissible=({},), authority='fixture')
        args.update(changes)
        return search_model(**args)

    def test_new_joint_intervention(self):
        r = self.run_model()
        self.assertEqual(r['status'], 'OPEN')
        self.assertEqual(r['evaluated'], 26)
        self.assertIn(((('a', '1'), ('b', '1')), (('c', 'joint'),)), r['frontier'])
        self.assertTrue(all(('p', '0') not in edit for edit, _ in r['frontier']))
        self.assertGreater(r['rejected']['regression'], 0)

    def test_admission_distinct_from_preservation(self):
        r = self.run_model(admissible=({'a': '0'},))
        self.assertFalse(r['frontier'])
        self.assertGreater(r['rejected']['inadmissible'], 0)

    def test_budget_fails_closed(self):
        r = self.run_model(max_trials=25)
        self.assertEqual(r['evaluated'], 0)
        self.assertEqual(r['reason'], 'MODEL_SEARCH_BUDGET_EXCEEDED')

    def test_multicontext_regression(self):
        r = self.run_model(baselines={'c': {'a': '0', 'b': '0', 'p': '1'},
                                     'd': {'a': '1', 'b': '0', 'p': '1'}},
                           protected={'keep': ({'a': '0'},)})
        self.assertTrue(r['frontier'])
        self.assertTrue(all(gain == (('d', 'joint'),) and not any(k == 'a' for k, _ in edit)
                            for edit, gain in r['frontier']))

    def test_invalid_rule(self):
        with self.assertRaisesRegex(ValueError, 'MODEL_RULE_INVALID'):
            self.run_model(obligations={'q': ({'unknown': '0'},)})

    def test_random_truth_table_oracle(self):
        rng = random.Random(20261126)
        keys = ('a', 'b', 'p')
        states = list(product('01', repeat=3))
        def dnf(table):
            return tuple(dict(zip(keys, s)) for s in states if s in table)
        for _ in range(300):
            q_tables = {q: {s for s in states if rng.randrange(2)} for q in ('q1', 'q2', 'q3')}
            p_table = {s for s in states if rng.randrange(2)}
            allowed = {s for s in states if rng.randrange(2)}
            starts = rng.sample(states, 2)
            allowed.update(starts)
            contexts = dict(zip(('c', 'd'), starts))
            r = self.run_model(baselines={c: dict(zip(keys, s)) for c, s in contexts.items()},
                               obligations={q: dnf(t) for q, t in q_tables.items()},
                               protected={'p': dnf(p_table)}, admissible=dnf(allowed))
            expected = {}
            for width in range(1, 4):
                for subset in combinations(range(3), width):
                    for vals in product('01', repeat=width):
                        edit = dict(zip(subset, vals))
                        gains = set()
                        for c, old in contexts.items():
                            new = tuple(edit.get(i, v) for i, v in enumerate(old))
                            if new not in allowed or (new in p_table) != (old in p_table):
                                break
                            if any(old in t and new not in t for t in q_tables.values()):
                                break
                            gains.update((c, q) for q, t in q_tables.items() if new in t and old not in t)
                        else:
                            if gains:
                                expected[tuple(sorted((keys[i], v) for i, v in edit.items()))] = gains
            frontier = {e: tuple(sorted(g)) for e, g in expected.items()
                        if not any(g < other for other in expected.values())}
            self.assertEqual(dict(r['frontier']), frontier)
            self.assertEqual(r['accepted'], len(expected))
            self.assertEqual(sum(r['rejected'].values()) + r['accepted'], 26)


if __name__ == '__main__':
    unittest.main()
