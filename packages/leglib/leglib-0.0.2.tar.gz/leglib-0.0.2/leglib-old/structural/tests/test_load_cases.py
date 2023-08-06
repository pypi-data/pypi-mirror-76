from structural.load_cases import calc_combos
from structural.load_cases import case_abbrs
from structural.load_cases import case_names
from structural.load_cases import cases
from structural.load_cases import combos
import unittest


class TestLoadCases(unittest.TestCase):

    def test_name(self):
        pass

    def test_calc_combos(self):
        P = [4.5, 11.7]
        results = calc_combos("ASD", P)
        self.assertAlmostEqual(max(results), 16.2, places=1)
        self.assertAlmostEqual(min(results), 4.5, places=1)
        results = calc_combos("LRFD", P)
        self.assertAlmostEqual(max(results), 24.12, places=1)
        self.assertAlmostEqual(min(results), 6.30, places=1)
        self.assertAlmostEqual(max(results), 24.12, places=1)
        # D, L, Lr, S, W+, W-, E, H
        P = [4.5, 0, 0, 0, 20.0, -8.0]
        results = calc_combos("ASD", P)
        # D + W+ = 4.5 + 20 = 24.5
        self.assertAlmostEqual(max(results), 24.5, places=1)
        # 0.6D + W- = 0.6(4.5) - 8.0 = -5.30
        self.assertAlmostEqual(min(results), -5.30, places=1)
        # D, L, Lr, S, W+, W-, E, H
        P = [4.5, 7.0, 0, 0, 20.0, -8.0]
        results = calc_combos("ASD", P)
        # D + 0.75L + 0.75W+ = 4.5 + 0.75(7) + 0.75(20) = 24.75
        self.assertAlmostEqual(max(results), 24.75, places=2)



if __name__ == '__main__': # pragma: no cover
    unittest.main()
