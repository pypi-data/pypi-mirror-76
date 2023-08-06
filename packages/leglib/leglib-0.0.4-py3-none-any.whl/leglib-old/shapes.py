"Basic 2D shapes"

import math


class Circle:
    "Circle.  See AISC 2005 p. 17-39 for section property formulas."

    def __init__(self, d):
        self.d = d

    def R(self):
        "Radius"
        return self.d/2.0

    def r(self):
        "Radius of gyration"
        return self.R()/2.0

    def A(self):
        "Returns area of circle = pi*R**2"
        return math.pi*(self.R()**2)

    def segment_area(self, y):
        "Returns area of a circle segment above horizontal axis at y"
        r = self.R()
        return 2*((r**2.0*math.asin(r/math.fabs(r)))/2.0-(r**2*math.asin(y/math.fabs(r))+y*math.sqrt(r**2-y**2))/2.0)

    def first_moment_segment_area(self, y):
        "Returns the first moment about an axis at y = y"
        r = self.R()
        return -(2.0*math.sqrt(r**2-y**2)*(y**2-r**2))/3.0

    def stress_block_area(self, c, beta1):
        """
        a = Depth of compression block from top of circle at y=r
        c = Depth to neutral axis from top of circle at y=r
        Returns area of the stress block from y=(r - a) to y=r about an axis at y=(r - c)
        """
        a = c*beta1
        r = self.R()
        return 2.0*((r**2*math.asin(r/math.fabs(r)))/2-(r**2*math.asin((r-a)/math.fabs(r))+(r-a)*math.sqrt(2*a*r-a**2))/2)

    def stress_block_moment(self, c, beta1):
        a = c*beta1
        r = self.R()
        # return 2.0*((3.0*c*r**2*math.asin((r-a)/math.fabs(r))+math.sqrt(2.0*a*r-a**2)*((3*c+4*a)*r-3*a*c-2*a**2))/6-(c*r**2*math.asin(r/math.fabs(r)))/2)

        return 2.0*((c*r**2*math.asin(r/math.fabs(r)))/2-(3*c*r**2*math.asin((r-a)/math.fabs(r))+math.sqrt(2*a*r-a**2)*((3*c+4*a)*r-3*a*c-2*a**2))/6)

    def I(self):
        "Moment of inertia"
        return math.pi*(self.R()**4)/4.0

    def S(self):
        "Section modulus"
        return math.pi*(self.R()**3)/4.0

    def Z(self):
        "Plastic section modulus"
        return (self.d**3)/6.0


class Donut:
    def __init__(self, r1, r2):
        self.outer = Circle(d=2*max(r1, r2))
        self.inner = Circle(d=2*min(r1, r2))

    @property
    def r1(self):
        return self.outer.d/2.0

    @property
    def r2(self):
        return self.inner.d/2.0


class Cylinder:

    def __init__(self, D, L):
        self.D = D
        self.L = L

    def V(self):
        return math.pi*self.D**2/4.0*self.L

    def Aend(self):
        return math.pi*self.D**2/4.0

    def Abottom(self):
        return self.Aend()

    def Atop(self):
        return self.Aend()

    def Aside(self):
        return math.pi*self.D*self.L

    def A(self):
        return 2.0*self.Aend() + self.Aside()


class HollowCircle:
    "Hollow circle.  See AISC 2005 p. 17-39 for section property formulas."

    def __init__(self, d, d1):
        "d = Outside diameter. d1 = Inside diameter"
        self.d = d
        self.d1 = d1

    def r(self):
        "Radius of gyration"
        return math.sqrt(self.d**2 + self.d1**2)/4.0

    def A(self):
        "Returns area of hollow circle"
        return math.pi*(self.d**2 - self.d1**2)/4.0

    def I(self):
        "Moment of inertia"
        return math.pi*(self.d**4 - self.d1**4)/64.0

    def S(self):
        "Section modulus"
        return math.pi*(self.d**4 - self.d1**4)/(self.d*32.0)

    def Z(self):
        "Plastic section modulus"
        return self.d**3/6.0 - self.d1**3/6.0


class Rectangle:

    def __init__(self, b, h):
        self.b = b
        self.h = h

    def A(self):
        "Returns area"
        return self.b*self.h

    def Ix(self):
        "Moment of inertia axis through centroid parallel to b"
        return self.b*self.h**3/12.0

    def Ix_base(self):
        "Moment of inertia axis through base parallel to b"
        return self.b*self.h**3/3.0

    def Iy(self):
        "Moment of inertia axis through centroid parallel to h"
        return self.h*self.b**3/12.0

    def Iy_base(self):
        "Moment of inertia axis through base parallel to h"
        return self.h*self.b**3/3.0

    def rx(self):
        "Returns radius of gyration about x axis"
        return math.sqrt(self.Ix()/self.A())

    def ry(self):
        "Returns radius of gyration about x axis"
        return math.sqrt(self.Iy()/self.A())

    def Sx(self):
        "Returns plastic moment of inertia about x axis"
        return self.b*self.h**2/6.0

    def Sy(self):
        "Returns plastic moment of inertia about y axis"
        return self.h*self.b**2/6.0

    def Zx(self):
        "Returns plastic moment of inertia about x axis"
        return self.b*self.h**2/4.0

    def Zy(self):
        "Returns plastic moment of inertia about y axis"
        return self.h*self.b**2/4.0


class RectangularPrism:

    def __init__(self, B, L, T):
        self.B = B
        self.L = L
        self.T = T

    def V(self):
        return self.B*self.L*self.T

    def Aback(self):
        return self.L*self.T

    def Abottom(self):
        return self.L*self.B

    def Aend(self):
        return self.B*self.T

    def Atop(self):
        return self.L*self.B

    def Afront(self):
        return self.L*self.T

    def A(self):
        return 2.0*(self.Atop() + self.Afront() + self.Aend())
