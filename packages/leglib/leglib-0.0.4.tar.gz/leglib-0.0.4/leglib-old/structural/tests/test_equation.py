import filters as f
import unittest


class _DummyCalc:
    def __init__(self, w, L):
        self.w = w
        self.L = L
        self.M = w*L**2/8.0
        self.Kz = 0.85
        self.Kzt = 1.0
        self.Kd = 0.85
        self.V = 125.0
        self.q = 0.00256*self.Kz*self.Kzt*self.Kd*self.V**2     # 28.9


class TestEquationFilter(unittest.TestCase):

    def setUp(self):
        self.eq1 = "M = wL^2/8"
        self.eq2 = "q = 0.00256(Kz)(Kzt)(Kd)(V)^2"
        self.calc = _DummyCalc(w=0.5, L=18.0)

    def test_eq_replacement(self):
        self.assertEqual(f.equation(self.eq1, self.calc), "M = wL^2/8 = (0.500)(18.0)^2/8 = 20.2")
        self.assertEqual(f.equation(self.eq2, self.calc), "q = 0.00256(Kz)(Kzt)(Kd)(V)^2 = 0.00256(0.850)(1.00)(0.850)(125)^2 = 28.9")

if __name__ == '__main__': # pragma: no cover
    unittest.main()
