from structural.snowcalc import SnowCalc
import unittest

class TestSnowCalc(unittest.TestCase):

    def setUp(self):
        self.calc = SnowCalc(pg=70.0, W=50.0, Ce=1.1, Ct=1.0, I=1.1,
                is_leeward=False)

    def test_calc(self):
        self.assertAlmostEqual(self.calc.pf, 59.0, places=0)
        self.assertAlmostEqual(self.calc.ps, 59.0, places=0)
        self.assertAlmostEqual(self.calc.hb, 59.0/23.1, places=0)

    def test_report(self):
        r = self.calc.render("txt")
        self.assertTrue(len(r) > 0)
        self.assertTrue(type(r) == type("Joe"))


if __name__ == '__main__': # pragma: no cover
    unittest.main()
