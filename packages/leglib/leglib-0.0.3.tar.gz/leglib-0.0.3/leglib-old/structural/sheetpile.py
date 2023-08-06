import math

class Soil:

    def __init__(self, gamma = 110.0, phi = 30.0, delta = 15.0):
        self.delta = delta
        self.gamma = gamma
        self.phi = phi

    def Ka(self, beta = 0.0, alpha = 90.0):
        alpha = math.radians(float(alpha))
        beta = math.radians(float(beta))
        delta = math.radians(self.delta)
        phi = math.radians(self.phi)
        return math.cos(phi)**2/(math.sin(alpha)**2*math.sin(alpha - delta)*\
            (1.0 + math.sqrt((math.sin(phi + delta)*math.sin(phi - beta))/\
            (math.sin(alpha - delta)*math.sin(alpha + beta)))**2))
