#from structural.load_cases import calc_combos
#from structural.load_cases import case_abbrs
#from structural.load_cases import case_names
#from structural.load_cases import cases
#from structural.load_cases import combos
from structural.beamcolumn import BeamColumn
import unittest


class TestBeamColumn(unittest.TestCase):

    def setUp(self):
        self.b = BeamColumn(L=24.0)

    def test_analysis(self):
        self.b.add_uniform([2.0]) # Add D=2.0 kips/foot
        self.b.E = 29000.0
        self.b.Ix = 82.8
        # M = 2*24*24/8 = 144 kip-ft = 1728 kip-in
        # V = 2*24/2 = 24.0 kips
        # Y = 22.5(2)(24^4)/((29000)(82.8)) = 6.218
        self.b.analyze()
        self.assertAlmostEqual(self.b.results.R1max, 24.0, places=1)
        self.assertAlmostEqual(self.b.results.R2max, 24.0, places=1)
        self.assertAlmostEqual(self.b.results.Mmax, 1728.0, places=0)
        self.assertAlmostEqual(self.b.results.Mmin, 0.0, places=0)
        self.assertAlmostEqual(self.b.results.Vmax, 24.0, places=1)
        self.assertAlmostEqual(self.b.results.Ymax, 6.218, places=1)
        self.assertAlmostEqual(self.b.results.Ymin, 0.0, places=2)

if __name__ == '__main__': # pragma: no cover
    unittest.main()
