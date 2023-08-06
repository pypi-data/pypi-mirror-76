from structural import IBC2009
from structural import set_code
from structural.roof import Roof
import unittest

# ======================
# ASCE 7-05
# ======================
class TestSnowASCE705(unittest.TestCase):

    def setUp(self):
        code = set_code(IBC2009)
        self.asce = code.asce7

    def test_flat_roof_snow(self):
        # Default when pg <= 20, I(pg) = (1.0)(15) = 15 psf
        self.assertAlmostEqual(self.asce.pf(pg=15.0, I=1.0, Ce=1.0, Ct=1.0),
                15.0, places=2)
        self.assertAlmostEqual(self.asce.pf(pg=20.0, I=1.0, Ce=1.0, Ct=1.0),
                20.0, places=2)
        self.assertAlmostEqual(self.asce.pf(pg=25.0, I=1.0, Ce=1.0, Ct=1.0),
                20.0, places=2)
        self.assertAlmostEqual(self.asce.pf(pg=30.0, I=1.0, Ce=1.0, Ct=1.0),
                21.0, places=2)
        self.assertAlmostEqual(self.asce.pf(pg=30.0, I=1.15, Ce=1.0, Ct=1.0),
                24.15, places=2)

    def test_Cs(self):
        roof = Roof(W=30.0, rise=8, slippery=False)
        self.assertAlmostEqual(self.asce.Cs(roof, Ct=1.0), 0.91, places=2)

    def test_snow_density(self):
        self.assertAlmostEqual(self.asce.snow_density(pg=30.0), 17.9, places=1)
        # Test upper limit of 30 pcf
        self.assertAlmostEqual(self.asce.snow_density(pg=1000.0), 30.0, places=1)

    def test_asce705_example_1(self):
        "Replicate Example 1 on p. 329 of ASCE 7-05 in Commentary Chapter 6"
        roof = Roof(W=30.0, rise=8, slippery=False)
        self.assertTrue(self.asce.is_unbalanced(roof))
        self.assertAlmostEqual(self.asce.ps(roof, 30.0, 1.0, 1.0, 1.0),
                19.0, places=0)


if __name__ == '__main__': # pragma: no cover
    unittest.main()

