from . import asce7_05 as asce

class Sign:

    def __init__(self, h, B, s, V=90.0, exposure="C"):
        self.h = float(h)   # Total height
        self.B = float(B)   # Sign width
        self.V = float(V)   # Basic wind speed
        self.s = float(s)   # Sign height
        self.exposure = exposure
        self.Cf = 2.0       # Conservative see ASCE 7-05 p. 73

    def As(self):
        "Returns area of sign in sq ft (ASCE 7-05 Section 6.5.14, p. 29)"
        return self.B*self.s

    def qh(self):
        "Returns wind pressure in psf"
        return asce.qz(V=self.V, z=self.h, exposure=self.exposure, I=1.0,
                Kd=0.85, Kzt=1.0)

    def F(self):
        "Returns resultant force in pounds"
        return asce.F(As=self.As(), V=self.V, z=self.h, exposure="C", Cf=self.Cf)

    def y(self):
        "Height to resultant"
        return self.h - self.s/2.0

