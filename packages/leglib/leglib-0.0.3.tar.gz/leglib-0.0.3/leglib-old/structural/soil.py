import fmt
import math

class Soil:

    def __init__(self, name=None, Qa=1500.0, gamma_s=110.0, gamma_sat=None,
            phi=30.0, delta=0):
        self.name = name
        self.Qa = Qa            # psf
        self.delta = delta
        self.gamma_s = gamma_s
        # Saturated unit weight
        if gamma_sat is None:
            self.gamma_sat = 1.3*self.gamma_s   # Estimate
        else:
            self.gamma_sat = gamma_sat
        self.phi = phi

    def __unicode__(self):
        if self.name is not None:
            return str(self.name)
        else:
            return "Soil Qa=%s" % fmt.sigdig(self.Qa)

    def __str__(self):
        return self.__unicode__()

    def Ka(self, beta = 0.0, alpha = 90.0):
        alpha = math.radians(float(alpha))
        beta = math.radians(float(beta))
        delta = math.radians(self.delta)
        phi = math.radians(self.phi)
        return (math.sin(alpha + phi)**2)/(math.sin(alpha)**2*math.sin(alpha - \
                delta)*(1.0 + math.sqrt((math.sin(phi + delta)*math.sin(phi - \
                beta))/(math.sin(alpha - delta)*math.sin(alpha + beta))))**2)

    def Ka_rankine(self, beta=0.0, alpha=90.0):
        # Ref. Das p. 439
        theta = math.radians(90.0 - float(alpha))
        alpha = math.radians(float(beta))
        phi = math.radians(float(self.phi))
        psi = math.asin(math.sin(alpha)/math.sin(phi)) - alpha + 2.0*theta
        return (math.cos(alpha - theta)*math.sqrt(1.0 + math.sin(phi)**2 - \
                2.0*math.sin(phi)*math.cos(psi)))/(math.cos(theta)**2* \
                (math.cos(alpha) + math.sqrt(math.sin(phi)**2 - math.sin(alpha)**2)))

    def Kp(self, beta = 0.0, alpha = 90.0):
        alpha = math.radians(float(alpha))
        beta = math.radians(float(beta))
        delta = math.radians(self.delta)
        phi = math.radians(self.phi)
        return (math.sin(alpha - phi)**2)/(math.sin(alpha)**2*math.sin(alpha + \
                delta)*(1.0 - math.sqrt((math.sin(phi + delta)*math.sin(phi + \
                beta))/(math.sin(alpha + delta)*math.sin(alpha + beta))))**2)

    def Kp_rankine(self, beta=0.0, alpha=90.0):
        # Ref. Das p. 441
        theta = math.radians(90.0 - float(alpha))
        alpha = math.radians(float(beta))
        phi = math.radians(float(self.phi))
        psi = math.asin(math.sin(alpha)/math.sin(phi)) + alpha + 2.0*theta
        return (math.cos(alpha - theta)*math.sqrt(1.0 + math.sin(phi)**2 + \
                2.0*math.sin(phi)*math.cos(psi)))/(math.cos(theta)**2* \
                (math.cos(alpha) - math.sqrt(math.sin(phi)**2 - math.sin(alpha)**2)))


class SoilStratum(Soil):

    def __init__(self, z, soil):
        self.soil = soil
        self.z = float(z)

    def __lt__(self, other):
        return self.z < other.z

default_soil = Soil(name="Default Soil")

