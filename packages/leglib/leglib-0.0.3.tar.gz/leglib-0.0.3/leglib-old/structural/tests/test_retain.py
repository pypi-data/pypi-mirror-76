from structural.retain import RetainingWall
from structural.soil import Soil
import unittest

class TestRetainingWall(unittest.TestCase):

    def setUp(self):
        self.w = RetainingWall(zwt1 = 8.0, zwt2 = 10.0)
        s1 = Soil(gamma_s=105, phi=30)
        s2 = Soil(gamma_s=110, phi=34)
        self.w.add_soil_stratum(15, s1)
        self.w.add_soil_stratum(30, s2)

    def test_analyze(self):
        self.w.analyze()
#        import matplotlib.pyplot as plt
#        import math

#        plt.plot([0.0, 0.0], [0.0, self.w.H])
#        plt.plot([n.horiz for n in self.w.nodes], [n.z for n in self.w.nodes])
#        ax = plt.gca()
#        xmax = max(max(ax.get_xlim()), math.fabs(min(ax.get_xlim())))
#        ax.set_xlim(-xmax, xmax)
#        ax.set_ylim(ax.get_ylim()[::-1])
#        plt.show()

if __name__ == '__main__': # pragma: no cover
    unittest.main()

