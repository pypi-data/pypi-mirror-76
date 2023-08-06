from structural.soil import Soil
from structural.soil import SoilStratum
import unittest

class TestSoil(unittest.TestCase):

    def setUp(self):
        pass

    def test_Ka_coulomb(self):
        s1 = Soil(name="Soil A1", gamma_s=110, phi=30, delta=15)
        self.assertAlmostEqual(s1.Ka(), 0.30, places = 2)
        self.assertAlmostEqual(s1.Ka(beta = 5), 0.32, places = 2)
        self.assertAlmostEqual(s1.Ka(beta = -5), 0.285, places = 2)
        self.assertAlmostEqual(s1.Ka(beta = 15), 0.37, places = 2)
        self.assertAlmostEqual(s1.Ka(beta = 15, alpha = 85), 0.42,
                places = 2)
        self.assertAlmostEqual(s1.Ka(beta = 15, alpha = 95), 0.329,
                places = 2)
        # Bowles 4th edition Example 11-1, p. 479
        s2 = Soil(name="Soil A2", gamma_s=110, phi=30.0, delta=20)
        self.assertAlmostEqual(s2.Ka(beta = 10), 0.34, places = 2)
        # Bowles 4th edition Example 11-2, p. 481
        s3 = Soil(name="Soil A3", gamma_s=110, phi=32.0, delta=0)
        self.assertAlmostEqual(s3.Ka(beta = 0), 0.307, places = 2)
        s4 = Soil(name="Soil A4", gamma_s=110, phi=30.0, delta=0)
        self.assertAlmostEqual(s4.Ka(beta = 0), 0.333, places = 2)
        # Das Table 13.2, p. 441 (alpha in Das is beta here)
        s5 = Soil(name="Soil A5", phi=30)
        self.assertAlmostEqual(s5.Ka_rankine(beta=0), 0.333, places=2)
        s6 = Soil(name="Soil A6", phi=34)
        self.assertAlmostEqual(s6.Ka_rankine(beta=20), 0.338, places=2)
        s7 = Soil(name="Soil A7", phi=38)
        self.assertAlmostEqual(s7.Ka_rankine(beta=10), 0.246, places=2)

    def test_Kp_coulomb(self):
        s1 = Soil(name="Soil B1", gamma_s=110, phi=30, delta=15)
        self.assertEqual("%s" % s1, "Soil B1")
        self.assertAlmostEqual(s1.Kp(), 4.98, places = 2)
        self.assertAlmostEqual(s1.Kp(beta = 5), 6.31, places = 2)
        self.assertAlmostEqual(s1.Kp(beta = -5), 3.96, places = 2)
        self.assertAlmostEqual(s1.Kp(beta = 15), 10.81, places = 2)
        self.assertAlmostEqual(s1.Kp(beta = 15, alpha = 85), 8.63,
                places = 2)
        self.assertAlmostEqual(s1.Kp(beta = 15, alpha = 95), 14.38,
                places = 2)
        # Das Table 13.2, p. 441 (alpha in Das is beta here)
        s5 = Soil(name="Soil B2", phi=30)
        self.assertAlmostEqual(s5.Kp_rankine(beta=0), 3.000, places=2)
        s6 = Soil(name="Soil B3", phi=34)
        self.assertAlmostEqual(s6.Kp_rankine(beta=20), 2.612, places=2)
        s7 = Soil(name="Soil B4", phi=38)
        self.assertAlmostEqual(s7.Kp_rankine(beta=10), 3.937, places=2)

class TestSoilStratum(unittest.TestCase):

    def test_sorting(self):
        ss1 = SoilStratum(0.0, Soil())
        self.assertEqual("%s" % ss1.soil, "Soil Qa=1500")
        ss2 = SoilStratum(11.2, Soil())
        ss3 = SoilStratum(9.4, Soil())
        ss4 = SoilStratum(28.0, Soil())
        strata = [ss1, ss2, ss3, ss4]
        strata.sort()
        correctly_sorted = [ss1, ss3, ss2, ss4]
        for i in range(0, len(strata)):
            self.assertEqual(strata[i], correctly_sorted[i])


if __name__ == '__main__': # pragma: no cover
    unittest.main()
