from structural import FBC2010
from structural.windcalc import WindCalc
import unittest

class TestWindCalcASCE7_10(unittest.TestCase):

    def setUp(self):
        self.calc = WindCalc(V=142.0, exposure="C", z=15.0, Kd=0.85, Kzt=1.0,
                code=FBC2010)

    def test_results(self):
        self.calc.recalc()
        self.assertAlmostEqual(self.calc.Kz, 0.85, places=2)
        self.assertAlmostEqual(self.calc.Kzt, 1.00, places=2)
        self.assertAlmostEqual(self.calc.Kd, 0.85, places=2)
        self.assertAlmostEqual(self.calc.qz, 37.295, places=2)

    def test_report(self):
        self.calc.recalc()
        r = self.calc.render("txt")
        self.assertTrue(len(r) > 0)
        self.assertTrue(type(r) == type("Joe"))


if __name__ == '__main__': # pragma: no cover
    unittest.main()

