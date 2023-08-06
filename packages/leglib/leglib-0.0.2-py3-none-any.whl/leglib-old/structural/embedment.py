import math

ERROR_LIMIT = 0.005  # feet

class EmbeddedPier:
    "Reference 2006 IBC Section 1805.7.2"

    def __init__(self, b, P, h, S0, constrained = False):
        self.b = float(b)   # Width of pier in feet
        self.P = float(P)   # Lateral force in pounds
        self.h = float(h)   # Height from ground surface to P force
        self.S0 = float(S0) # Allowable lateral earth pressure (Table 1804.2)
        self.constrained = constrained
        self.depth = 1.0

    def S1(self, d):
        """Allowable lateral soil-bearing pressure as set forth in 2006 IBc
        Section 1804.3 based on a depth of 1/3 the depth of embedment in pounds
        per square foot."""
        return min(d, 12.0)/3.0*self.S0

    def S3(self, d):
        """Allowable lateral soil-bearing pressure as set forth in 2006 IBc
        Section 1804.3 based on the depth of embedment in pounds per square
        foot."""
        return min(d, 12.0)*self.S0

    def _d_con(self):
        "Returns constrained embedment in feet, 2006 IBC Eq. 18-2"
        retval = self.depth
        done = False
        while not done:
            S3 = self.S3(retval)
            dreq = math.sqrt(4.25*self.P*self.h/(S3*self.b))
            error = math.fabs(retval - dreq)
            done = error <= ERROR_LIMIT
            if not done:
                retval = (retval + dreq)/2.0
        self.depth=retval
        return round(retval, 2)

    def _d_noncon(self):
        "Returns nonconstrained embedment in feet: 2006 IBC Eq. 18-1"
        retval = self.depth
        done = False
        while not done:
            S1 = self.S1(retval)
            A = 2.34*self.P/(self.b*self.S1(retval))
            dreq = 0.5*A*(1.0 + math.sqrt(1.0 + 4.36*self.h/A))
            error = math.fabs(retval - dreq)
            done = error <= ERROR_LIMIT
            if not done:
                retval = (retval + dreq)/2.0
        self.depth=retval
        return round(retval, 2)

    def d(self):
        "Returns required embedment in feet"
        if self.constrained:
            return self._d_con()
        else:
            return self._d_noncon()

    def design_width(self, target_depth):
        "Selects width to achieve target depth."
        self.b = 1.0
        while self.d() > target_depth:
            self.b = self.b + 0.01
        return self.b

