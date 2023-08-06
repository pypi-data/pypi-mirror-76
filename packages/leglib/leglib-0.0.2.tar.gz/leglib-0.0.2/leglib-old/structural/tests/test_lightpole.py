from structural import FBC2010
from structural.lightpole import LightPole
from structural.lightpole import LightPoleBase
import unittest

class TestLightPoleBase(unittest.TestCase):

    def setUp(self):
        self.pole = LightPole(L=30.0, shape="square", size=5.0,
                V=145.0, exposure="B", Kzt=1.0)
        self.pole.add_fixture(b=16.4, h=7.0, y=30.0)
        self.base = LightPoleBase(pole=self.pole, b=2.0)

    def test_pole(self):
        self.pole.recalc()
        self.assertAlmostEqual(self.pole.Kd, 0.90, places=2)
        self.assertAlmostEqual(self.pole.Kz, 0.70, places=2)
        self.assertAlmostEqual(self.pole.qz, 33.9, places=1)
        self.assertAlmostEqual(self.pole.Af, 12.50, places=2)
        self.assertAlmostEqual(self.pole.P, 460.0, places=0)
        self.assertAlmostEqual(self.pole.h, 15.90, places=2)

    def test_base_design(self):
        pass


if __name__ == '__main__': # pragma: no cover
    unittest.main()
