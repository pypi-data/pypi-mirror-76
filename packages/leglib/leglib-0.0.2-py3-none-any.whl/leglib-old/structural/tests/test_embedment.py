from structural.embedment import EmbeddedPier
import unittest

class TestEmbeddedPier(unittest.TestCase):

    def test_depth(self):
        self.pier = EmbeddedPier(P = 5400.0, S0=200.0, b=6.0, h=37.25,
                constrained=False)
        self.pier.constrained = False
        self.assertAlmostEqual(self.pier.d(), 11.83, places=2)
        self.pier.constrained = True
        self.assertAlmostEqual(self.pier.d(), 8.93, places=2)

    def test_design_width(self):
        self.pier = EmbeddedPier(P = 5400.0, S0=200.0, b=6.0, h=37.25,
                constrained=False)
        self.pier.constrained = False
        self.assertAlmostEqual(self.pier.design_width(target_depth = 10.0),
                9.58333, places=1)

if __name__ == '__main__': # pragma: no cover
    unittest.main()
