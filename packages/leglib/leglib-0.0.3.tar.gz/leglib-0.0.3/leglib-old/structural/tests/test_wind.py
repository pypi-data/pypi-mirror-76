from structural import FBC2010
from structural import IBC2009
from structural import set_code
import unittest


# =============================================================================
# ASCE 7-05
# =============================================================================
class TestWindASCE705(unittest.TestCase):

    def setUp(self):
        code = set_code(IBC2009)
        self.asce = code.asce7

    def test_illegal_exposure(self):
        self.assertRaises(ValueError, self.asce.Kz, z=15, exposure="E")

    def test_Kz(self):
        self.assertAlmostEqual(self.asce.Kz(z=12, exposure="B"), 0.70, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=12, exposure="B", case=2), 0.57,
                places=2)
        self.assertAlmostEqual(self.asce.Kz(z=12, exposure="C"), 0.85, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=12, exposure="D"), 1.03, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=15, exposure="B"), 0.70, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=15, exposure="B", case=2), 0.57,
                places=2)
        self.assertAlmostEqual(self.asce.Kz(z=30, exposure="B"), 0.70, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=30, exposure="C"), 0.98, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=30, exposure="D"), 1.16, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=60, exposure="B"), 0.85, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=60, exposure="C"), 1.14, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=60, exposure="D"), 1.31, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=100, exposure="B"), 0.99, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=100, exposure="C"), 1.27, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=100, exposure="D"), 1.43, places=2)

    def test_qz(self):
        self.assertAlmostEqual(self.asce.qz(V=90.0, z=40.0, exposure="C", I=1.0,
            Kd=0.85, Kzt=1.0), 18.33, places=2)
        self.assertAlmostEqual(self.asce.qz(V=90.0, z=40.0, exposure="B", I=1.0,
            Kd=0.85, Kzt=1.0), 13.4, places=2)
        self.assertAlmostEqual(self.asce.qz(V=90.0, z=35.0, exposure="B", I=1.0,
            Kd=0.85, Kzt=1.0), 12.87, places=2)

# =============================================================================
# ASCE 7-10
# =============================================================================
class TestWindASCE710(unittest.TestCase):

    def setUp(self):
        self.asce = set_code(FBC2010).asce7

    def test_Kz(self):
        self.assertAlmostEqual(self.asce.Kz(z=12, exposure="B"), 0.70, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=12, exposure="B", case=2), 0.57,
                places=2)
        self.assertAlmostEqual(self.asce.Kz(z=12, exposure="C"), 0.85, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=12, exposure="D"), 1.03, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=15, exposure="B"), 0.70, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=15, exposure="B", case=2), 0.57,
                places=2)
        self.assertAlmostEqual(self.asce.Kz(z=30, exposure="B"), 0.70, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=30, exposure="C"), 0.98, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=30, exposure="D"), 1.16, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=60, exposure="B"), 0.85, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=60, exposure="C"), 1.14, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=60, exposure="D"), 1.31, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=100, exposure="B"), 0.99, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=100, exposure="C"), 1.27, places=2)
        self.assertAlmostEqual(self.asce.Kz(z=100, exposure="D"), 1.43, places=2)

    def test_qz(self):
        self.assertAlmostEqual(self.asce.qz(V=90.0, z=40.0, exposure="C",
            Kd=0.85, Kzt=1.0), 18.33, places=2)
        self.assertAlmostEqual(self.asce.qz(V=90.0, z=40.0, exposure="B",
            Kd=0.85, Kzt=1.0), 13.4, places=2)
        self.assertAlmostEqual(self.asce.qz(V=90.0, z=35.0, exposure="B",
            Kd=0.85, Kzt=1.0), 12.87, places=2)
        # Hand calc 2014-03-25 for Project No. 215810015:
        self.assertAlmostEqual(self.asce.qz(V=142.0, z=15.0, exposure="C",
            case=1, Kd=0.85, Kzt=1.0), 37.2953344, places=2)


if __name__ == '__main__': # pragma: no cover
    unittest.main()

