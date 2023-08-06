from structural.pit import Pit
import unittest

class TestPit(unittest.TestCase):

    def setUp(self):
        self.pit = Pit(Lp=10.0, Bp=5.0, dp=8.0, tp=12.0, tf=18.0, Ltoe=1.5,
                dwt=2.0, Hg=0.5)
        self.pit.soil.gamma_s = 110.0

    def test_volumes(self):
        self.pit.recalc()
        self.assertAlmostEqual(self.pit.Lf, 15.0, places=1)
        self.assertAlmostEqual(self.pit.Bf, 10.0, places=1)
        self.assertAlmostEqual(self.pit.Hp, 8.5, places=2)
        self.assertAlmostEqual(self.pit.Vp, 289.0, places=1)
        self.assertAlmostEqual(self.pit.Vf, 225.0, places=1)
        self.assertAlmostEqual(self.pit.Vc, 514.0, places=1)
        self.assertAlmostEqual(self.pit.Vs, 528.0, places=1)
        self.assertAlmostEqual(self.pit.Wc, 77.10, places=2)

if __name__ == '__main__': # pragma: no cover
    unittest.main()

