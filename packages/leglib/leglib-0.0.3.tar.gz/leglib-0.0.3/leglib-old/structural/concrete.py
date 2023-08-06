"""Concrete helper classes and functions"""

import math

class Concrete:
    def __init__(self, fc=3000.0, wc=145.0, gamma_c=150.0):
        self.fc = float(fc)
        self.wc = float(wc)             # Unreinforced unit weight, pcf
        self.gamma_c = float(gamma_c)   # Reinforced unit weight, pcf
        self.ec = 0.003                 # Default concrete strain at failure

    def __str__(self):
        if self.wc > 115.0:
            return "%.0f psi" % (self.fc)
        else:
            return "%.0f psi lightweight" % (self.fc)

    def beta1(self):
        "ACI 318-05 Section 10.2.7.3, p. 121"
        return max(min(0.85, 0.85 - 0.05*(self.fc - 4000.0)/1000.0), 0.65)

    def Ec(self):
        "Returns Ec in ksi per ACI 318-05 Section 8.5.1, p. 99"
        if self.wc < 90 or self.wc > 155:
            return None
        return self.wc**1.5*33.0*math.sqrt(self.fc)/1000.0
