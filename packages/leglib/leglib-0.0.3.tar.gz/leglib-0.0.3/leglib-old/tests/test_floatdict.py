from floatdict import FloatDict
import unittest


class TestFloatDict(unittest.TestCase):

    def setUp(self):
        self.D = FloatDict({1 : 4.55, 2 : 3.78, 3: 8.22})
        self.L = FloatDict({1 : 5.4, 2 : 9.4, 4: 11.22})

    def test_division(self):
        # Division with a floatdict
        a = self.D/self.L
        # 1 - 4.55/5.4 = 0.8426
        # 2 - 3.78/9.4 = 0.40213
        # 3 - 8.22/0 = None
        # 4 - 0/11.22 = 0.0
        self.assertAlmostEqual(a[1] , 0.8426, places=3)
        self.assertAlmostEqual(a[2] , 0.40213, places=3)
        self.assertEqual(a[3] , None)
        self.assertAlmostEqual(a[4] , 0.0, places=2)
        # Division with a float
        b = self.D/-0.525
        # 1 - 4.55/-0.525 = -8.66667
        # 2 - 3.78/-0.525 = -7.2
        # 3 - 8.22/-0.525 = -15.65714
        self.assertAlmostEqual(b[1] , -8.66667, places=3)
        self.assertAlmostEqual(b[2] , -7.2, places=3)
        self.assertAlmostEqual(b[3] , -15.65714, places=3)
        # Right division with a float
        c = 0.525/self.D
        # 1 - 0.525/4.55 = 0.11538
        # 2 - 0.525/3.78 = 0.138888
        # 3 - 0.525/8.22 = 0.068686
        self.assertAlmostEqual(c[1] , 0.11538, places=4)
        self.assertAlmostEqual(c[2] , 0.13888, places=4)
        self.assertAlmostEqual(c[3] , 0.0638686, places=4)
        # Right division with a dict
        d = { 1 : 0.525, 6 : 11.4 }/self.D
        # 1 - 0.525/4.55 = 0.11538
        self.assertAlmostEqual(d[1] , 0.11538, places=4)
        self.assertAlmostEqual(d[2] , 0.0, places=4)
        self.assertAlmostEqual(d[3] , 0.0, places=4)
        self.assertAlmostEqual(d[6] , None, places=4)

    def test_multiplication(self):
        # 1 - (4.55)(5.4) = 24.57
        # 2 - (3.78)(9.4) = 35.532
        # 3 - (8.22)(0) = 0
        # 4 - (0)(11.22) = 0
        a = self.D*self.L
        self.assertAlmostEqual(a[1] , 24.57, places=2)
        self.assertAlmostEqual(a[2] , 35.532, places=2)
        self.assertAlmostEqual(a[3] , 0.0, places=2)
        self.assertAlmostEqual(a[4] , 0.0, places=2)

    def test_multiplication_addition(self):
        # 1 - 1.4(4.55) + 1.7*(5.4) = 15.55
        # 2 - 1.4(3.78) + 1.7*(9.4) = 20.332
        # 3 - 1.4(8.22) = 11.508
        # 4 - 1.7(11.22) = 19.074
        # Test __mul__, __rmul__ and __add__
        a = 1.4*self.D + self.L*1.7
        self.assertAlmostEqual(a[1] , 15.55, places=2)
        self.assertAlmostEqual(a[2] , 21.272, places=2)
        self.assertAlmostEqual(a[3] , 11.508, places=2)
        self.assertAlmostEqual(a[4] , 19.074, places=2)
        # Test float add
        b = self.D + 19.432
        # 4.55 + 19.432 = 23.982
        # 3.78 + 19.432 = 23.212
        # 8.22 + 19.432 = 27.652
        self.assertAlmostEqual(b[1] , 23.982, places=2)
        self.assertAlmostEqual(b[2] , 23.212, places=2)
        self.assertAlmostEqual(b[3] , 27.652, places=2)
        # Test floatdict add
        c = self.D + self.L
        # 4.55 + 5.4 = 9.95
        # 3.78 + 9.40 = 13.18
        # 8.22 + 0.0 = 8.22
        # 0.0 + 11.22 = 11.22
        self.assertAlmostEqual(c[1] , 9.95, places=2)
        self.assertAlmostEqual(c[2] , 13.18, places=2)
        self.assertAlmostEqual(c[3] , 8.22, places=2)
        self.assertAlmostEqual(c[4] , 11.22, places=2)

    def test_subtract(self):
        # Test float subtract
        T = self.D - 1.99
        # 4.55 - 1.99 = 2.56
        # 3.78 - 1.99 = 1.79
        # 8.22 - 1.99 = 6.23
        self.assertAlmostEqual(T[1] , 2.56, places=2)
        self.assertAlmostEqual(T[2] , 1.79, places=2)
        self.assertAlmostEqual(T[3] , 6.23, places=2)
        # Test floatdict subtract
        c = self.D - self.L
        # 4.55 - 5.4 = -0.85
        # 3.78 - 9.40 = -5.62
        # 8.22 - 0.0 = 8.22
        # 0.0 - 11.22 = -11.22
        self.assertAlmostEqual(c[1] , -0.85, places=2)
        self.assertAlmostEqual(c[2] , -5.62, places=2)
        self.assertAlmostEqual(c[3] , 8.22, places=2)
        self.assertAlmostEqual(c[4] , -11.22, places=2)


if __name__ == "__main__": # pragma: no cover
    unittest.main()
