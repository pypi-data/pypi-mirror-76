from structural.roof import Roof
import unittest

class TestRoof(unittest.TestCase):

    def test_roof_slope(self):
        # Reference ASCE 7-05 Commentary Ch. 6 Example 1, p. 329
        r = Roof(rise=8, W=30)
        self.assertAlmostEqual(r.theta(), 33.6900675, places=2)


if __name__ == '__main__': # pragma: no cover
    unittest.main()

