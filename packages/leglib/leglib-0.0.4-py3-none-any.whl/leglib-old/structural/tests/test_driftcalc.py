from structural.driftcalc import DriftCalc
import unittest

class TestDriftCalc(unittest.TestCase):

    def setUp(self):
        self.calc = DriftCalc(pg=70.0, lu=230, hc=10.0, Ce=1.1, Ct=1.0, I=1.1,
                is_leeward=False)

    def test_calc(self):
        self.assertAlmostEqual(self.calc.drift.pf, 59.3, places=1)
        self.assertAlmostEqual(self.calc.drift.hd, 4.7844, places=3)
        self.assertAlmostEqual(self.calc.drift.w, 19.0, places=1)
        self.assertAlmostEqual(self.calc.drift.gamma(), 23.1, places=1)
        self.assertAlmostEqual(self.calc.drift.pm, 169.81, places=0)
        self.assertAlmostEqual(self.calc.drift.hb, 2.567, places=2)
        self.calc = DriftCalc(pg=70.0, lu=230, hc=6.0, Ce=1.1, Ct=1.0, I=1.1,
                is_leeward=False)
        self.assertTrue(self.calc.drift.is_truncated)
        # Truncated drift = 6 - 2.567 = 3.433
        self.assertAlmostEqual(self.calc.drift.hd, 3.433 , places=2)
        # Width now becomes 4*4.78^2/6 = 15.260, round to 15.5
        self.assertAlmostEqual(self.calc.drift.w, 15.5, places=2)


if __name__ == '__main__': # pragma: no cover
    unittest.main()
