from structural.footing import FootingPierAssembly
from structural.footing import RectFooting
from structural.load_cases import combos
from structural.soil import Soil
import unittest


class TestRectFooting(unittest.TestCase):

    def setUp(self):
        pass

    def test_defaults(self):
        f = RectFooting(2.0, 2.0)
        self.assertEqual(f.A(), 4.0)
        self.assertEqual(f.Sx(), 4.0/3.0)
        self.assertEqual(f.gamma_c, 0.145)
        self.assertEqual(f.V(), 2.0*2.0*1.0)
        self.assertEqual(f.W(), 0.580)

    def test_properties(self):
        f = RectFooting(8.0, 12.0, 1.5, 0.145)
        self.assertEqual(f.A(), 96.0)
        self.assertEqual(f.Sx(), 192.0)
        self.assertEqual(f.gamma_c, 0.145)
        self.assertEqual(f.W(), 20.88)


class TestFootingPierAssembly(unittest.TestCase):

    def setUp(self):
        self.a = FootingPierAssembly(B=5.0, L=8.0, T=1.5, Lp=2.0, Bp=2.0, Hp=3.0,
            gamma_c=0.150, soil=Soil(gamma_s=0.090))
        self.f = self.a.footing
        self.p = self.a.pier

    def test_names(self):
        self.assertEqual("%s" % self.a.footing,
            "Footing 8'-0\" x 5'-0\" x 1'-6\"")
        self.assertEqual("%s" % self.a,
            "Footing 8'-0\" x 5'-0\" x 1'-6\" with pier 2'-0\"L x 2'-0\"W x 3'-0\"H")

    def test_footing_properties(self):
        self.assertAlmostEqual(self.f.A(), 40.0, places=2)
        self.assertAlmostEqual(self.f.Sx(), 53.33, places=2)
        self.assertAlmostEqual(self.f.Sy(), 33.33, places=2)
        self.assertAlmostEqual(self.f.gamma_c, 0.15)
        self.assertAlmostEqual(self.a.H(), 4.5, places=2)

    def test_weights(self):
        # Footing
        self.assertAlmostEqual(self.f.W(), 9.0, places=2)
        # Footing-pier assembly
        self.assertAlmostEqual(self.a.W(), 20.52, places=2)

    def test_pier_properties(self):
        self.assertAlmostEqual(self.p.Atop(), 4.0, places=3)
        self.assertAlmostEqual(self.p.V(), 12.0, places=2)

    def test_uniaxial_bending(self):
        "Rest load combinations.  See validation hand calc dated Feb 18 2014"
        # D, L, Lr, S, W+, W-
        self.a.add_P([15.0, 30.0, 0.0, 0.0, -10.0])
        self.a.add_Vx([0.0, 0.0, 0.0, 0.0, 3.0])
        self.a.add_Mx([0.0, 0.0, 0.0, 0.0, 15.0])
        self.assertTrue(self.a.is_eccentric())
        self.assertFalse(self.a.is_concentric())
        self.a.analyze()
        # Check D + 0.75L + 0.75W case, which has index of 9
        ASD9 = 9
        self.assertEqual(combos["ASD"][ASD9][1], "D + 0.75L + 0.75W+ + H")
        self.assertAlmostEqual(self.a.results.P[ASD9], 50.52, places=2)
        self.assertAlmostEqual(self.a.results.Mx[ASD9], 21.375, places=2)
        self.assertAlmostEqual(self.a.results.Vx[ASD9], 2.25, places=2)
        self.assertAlmostEqual(self.a.results.fmax[ASD9], 1664.0, places=0)
        self.assertAlmostEqual(self.a.results.fmin[ASD9], 862.0, places=0)
        # Check 0.6D + W case, which has index of 15
        ASD15 = 15
        self.assertEqual(combos["ASD"][ASD15][1], "0.6D + W+ + H")
        self.assertAlmostEqual(self.a.results.P[ASD15], 11.31, places=2)
        self.assertAlmostEqual(self.a.results.Mx[ASD15], 28.50, places=2)
        self.assertAlmostEqual(self.a.results.Vx[ASD15], 3.0, places=2)
        self.assertAlmostEqual(self.a.results.fmax[ASD15], 1019.0, places=0)
        self.assertAlmostEqual(self.a.results.fmin[ASD15], 0.0, places=0)

    def test_concentric(self):
        self.a.clear_loads()
        self.a.add_P([15.0, 30.0, 0.0, 0.0, -10.0])
        self.assertTrue(self.a.is_concentric())
        self.assertFalse(self.a.is_eccentric())


if __name__ == "__main__": # pragma: no cover
    unittest.main()
