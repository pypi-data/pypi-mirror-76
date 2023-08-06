from structural.concrete import Concrete
import unittest


class TestConcrete(unittest.TestCase):

    def test_name(self):
        self.assertEqual("2500 psi", "%s" % Concrete(2500, wc=145))
        self.assertEqual("3500 psi lightweight", "%s" % Concrete(3500, wc=100))

    def test_beta1(self):
        self.assertAlmostEqual(Concrete(2500).beta1(), 0.85)
        self.assertAlmostEqual(Concrete(3000).beta1(), 0.85)
        self.assertAlmostEqual(Concrete(4000).beta1(), 0.85)
        self.assertAlmostEqual(Concrete(5000).beta1(), 0.80)
        self.assertAlmostEqual(Concrete(6000).beta1(), 0.75)
        self.assertAlmostEqual(Concrete(7000).beta1(), 0.70)
        self.assertAlmostEqual(Concrete(8000).beta1(), 0.65)
        self.assertAlmostEqual(Concrete(10000).beta1(), 0.65)

    def test_Ec(self):
        self.assertAlmostEqual(Concrete(3000, 145).Ec(), 3156.0, places=0)
        self.assertAlmostEqual(Concrete(5000, 115).Ec(), 2878.0, places=0)
        self.assertAlmostEqual(Concrete(4000, 110).Ec(), 2408.0, places=0)
        self.assertEqual(Concrete(4000, 80).Ec(), None)
        self.assertEqual(Concrete(4000, 200).Ec(), None)


if __name__ == '__main__': # pragma: no cover
    unittest.main()
