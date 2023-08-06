from shapes import Circle
from shapes import Cylinder
from shapes import HollowCircle
from shapes import Rectangle
from shapes import RectangularPrism
import math
import unittest

class CircleTest(unittest.TestCase):

    def test_properties(self):
        """Test circle properties"""
        c = Circle(d=12.0)
        self.assertAlmostEqual(c.A(), 113.097, places=2)
        self.assertAlmostEqual(c.I(), 1017.875, places=2)
        self.assertAlmostEqual(c.S(), 169.646, places=2)
        self.assertAlmostEqual(c.Z(), 288.000, places=2)
        self.assertAlmostEqual(c.r(), 3.0, places=2)


class CylinderTest(unittest.TestCase):

    def testProperties(self):
        """Test cylinder properties"""
        c = Cylinder(D=2.0, L=4.0)
        self.assertAlmostEqual(c.Atop(), 3.142, places=2)
        self.assertAlmostEqual(c.Abottom(), 3.142, places=2)
        self.assertAlmostEqual(c.A(), 31.416, places=2)
        self.assertAlmostEqual(c.Aside(), 25.133, places=2)
        self.assertAlmostEqual(c.V(), 12.566, places=2)


class HollowCircleTest(unittest.TestCase):

    def testProperties(self):
        """Test hollow circle properties"""
        hc = HollowCircle(d=10.0, d1=9.00)
        self.assertAlmostEqual(hc.A(), 14.923, places=2)
        self.assertAlmostEqual(hc.I(), 168.811, places=2)
        self.assertAlmostEqual(hc.S(), 33.762, places=2)
        self.assertAlmostEqual(hc.Z(), 45.167, places=2)
        self.assertAlmostEqual(hc.r(), 3.363, places=2)


class RectangleTest(unittest.TestCase):

    def testProperties(self):
        """Test section properties"""
        r = Rectangle(b = 12.0, h = 24.0)
        self.assertAlmostEqual(r.A(), 288.0)
        self.assertAlmostEqual(r.Ix(), 13824.0, places=0)
        self.assertAlmostEqual(r.Ix_base(), 55296.0, places=0)
        self.assertAlmostEqual(r.Iy(), 3456.0, places=0)
        self.assertAlmostEqual(r.Iy_base(), 13824.0, places=0)
        self.assertAlmostEqual(r.Sx(), 1152.0, places=0)
        self.assertAlmostEqual(r.Sy(), 576.00, places=0)
        self.assertAlmostEqual(r.rx(), math.sqrt(13824.0/288.0), places=0)
        self.assertAlmostEqual(r.ry(), math.sqrt(3456.0/288.0), places=0)
        self.assertAlmostEqual(r.Zx(), 1728.0, places=0)
        self.assertAlmostEqual(r.Zy(), 864.0, places=0)

class RectangularPrismTest(unittest.TestCase):

    def testProperties(self):
        """Test rectangular prism (box) properties"""
        p = RectangularPrism(L=3.0, B=2.0, T=1.0)
        self.assertAlmostEqual(p.V(), 6.000, places=2)
        self.assertAlmostEqual(p.Atop(), 6.0, places=2)
        self.assertAlmostEqual(p.Abottom(), 6.0, places=2)
        self.assertAlmostEqual(p.Afront(), 3.0, places=2)
        self.assertAlmostEqual(p.Aback(), 3.0, places=2)
        self.assertAlmostEqual(p.Aend(), 2.0, places=2)
        A = 2*(3.0*2.0 + 3.0*1.0 + 2.0*1.0)
        self.assertAlmostEqual(p.A(), A, places=2)


if __name__ == '__main__': # pragma: no cover
    unittest.main()
