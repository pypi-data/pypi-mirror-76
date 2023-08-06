from structural.sign import Sign
import unittest

B = 31.5
s = 5.5
h = 40.0

class TestSign(unittest.TestCase):

    def setUp(self):
        self.sign = Sign(h=h, B=B, s=s)

    def test_wind_calcs(self):
        self.assertAlmostEqual(self.sign.As(), B*s, places=2)
        self.assertAlmostEqual(self.sign.qh(), 18.3, places=1)
        self.assertAlmostEqual(self.sign.F(), 5398.6, places=0)
        self.assertAlmostEqual(self.sign.y(), h-s/2, places=0)

if __name__ == '__main__': # pragma: no cover
    unittest.main()

