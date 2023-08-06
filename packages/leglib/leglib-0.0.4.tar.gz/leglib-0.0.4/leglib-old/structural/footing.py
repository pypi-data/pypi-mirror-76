from .load_cases import calc_combos
from .load_cases import cases
from .load_cases import combos
from shapes import RectangularPrism
from .soil import Soil
import fmt
import math


class RectFooting(RectangularPrism):

    def __init__(self, B=4.0, L=4.0, T=1.0, gamma_c=0.145):
        RectangularPrism.__init__(self, B, L, T)
        self.gamma_c = gamma_c # pcf

    def __unicode__(self):
        return "Footing %s x %s x %s" % (fmt.ft_in(self.L*12.0), fmt.ft_in(self.B*12.0),
            fmt.ft_in(self.T*12.0))

    def __str__(self):
        return self.__unicode__()

    def A(self):
        "Override area of prism to return only area of bearing surface (bottom)"
        return self.B*self.L

    def Sx(self):
        return self.B*self.L**2/6.0

    def Sy(self):
        return self.L*self.B**2/6.0

    def W(self):
        "Returns weight in kips"
        return self.gamma_c*self.V()

    def analyze(self, P, M):
        "Returns (fmin, fmax)"
        P = 1000.0*P    # convert to pounds
        M = 1000.0*M    # convert to lb-ft
        fmin = 0.0
        fmax = 0.0
        e = M/P
        if e <= self.L/6.0:
            fmin = P/self.A() - M/self.Sx()
            fmax = P/self.A() + M/self.Sx()
        else:
            N = (self.L/2.0 - e)*3.0
            fmin = 0.0
            fmax = 2.0*P/(self.B*N)
        return (fmin, fmax)


class FootingPierAssemblyResults:

    def __init__(self):
        self.Mx = [0.0 for i in range(0, len(combos["ASD"]))]
        self.P = [0.0 for i in range(0, len(combos["ASD"]))]
        self.Vx = [0.0 for i in range(0, len(combos["ASD"]))]
        self.fmax = [0.0 for i in range(0, len(combos["ASD"]))]
        self.fmin = [0.0 for i in range(0, len(combos["ASD"]))]


class FootingPierAssembly:
    def __init__(self, B, L, T, Lp, Bp, Hp, gamma_c=0.150, soil=Soil()):
        self.footing = RectFooting(B, L, T, gamma_c)
        self.pier = RectangularPrism(Bp, Lp, Hp)
        self.soil = soil
        self.gamma_c = gamma_c
        self.clear_loads()

    def __unicode__(self):
        return "%s with pier %sL x %sW x %sH" % (self.footing, fmt.ft_in(self.pier.L*12.0),
            fmt.ft_in(self.pier.B*12.0), fmt.ft_in(self.pier.T*12.0))

    def __str__(self):
        return self.__unicode__()

    def is_eccentric(self):
        "Returns true if any moment on the footing"
        retval = False
        if len(self.loads_Mx) and max(self.loads_Mx):
            retval = True
        if len(self.loads_Vx) and max(self.loads_Vx):
            retval = True
        return retval

    def is_concentric(self):
        "Returns true if no moment on the footing"
        return not self.is_eccentric()

    def clear_loads(self):
        # Applied loads
        self.loads_P = []
        self.loads_Mx = []
        self.loads_Vx = []
        # Loads calculated at footing/soil interface
        self.Mx = [0.0 for i in range(0, len(cases))]
        self.P = [0.0 for i in range(0, len(cases))]
        self.Vx = [0.0 for i in range(0, len(cases))]

    def vol_soil(self):
        return (self.footing.A() - self.pier.Atop())*self.pier.T

    def vol_conc(self):
        return (self.footing.V() + self.pier.V())

    def Wp(self):
        "Returns weight of pier in kips"
        return self.gamma_c*self.pier.V()

    def Ws(self):
        "Returns weight of soil in kips"
        return self.soil.gamma_s*self.vol_soil()

    def W(self):
        "Returns weight in kips"
        return self.soil.gamma_s*self.vol_soil() + self.gamma_c*self.vol_conc()

    def add_Mx(self, Mx):
        self.loads_Mx.append(Mx)

    def add_P(self, P):
        self.loads_P.append(P)

    def add_Vx(self, Vx):
        self.loads_Vx.append(Vx)

    def H(self):
        "Returns total height from bottom of footing to top of pier"
        return self.footing.T + self.pier.T

    def analyze(self):
        self.Mx = [0.0 for i in range(0, len(cases))]
        self.P = [0.0 for i in range(0, len(cases))]
        self.Vx = [0.0 for i in range(0, len(cases))]
        for P in self.loads_P:
            for i in range(0, len(P)):
                self.P[i] = self.P[i] + P[i]
        # Add self-weight to P
        self.P[0] = self.P[0] + self.W()
        for Vx in self.loads_Vx:
            for i in range(0, len(Vx)):
                self.Vx[i] = self.Vx[i] + Vx[i]
        for Mx in self.loads_Mx:
            for i in range(0, len(Mx)):
                self.Mx[i] = self.Mx[i] + Mx[i]
        # Add effect of Vx to Mx
        for i in range(0, len(self.Vx)):
            self.Mx[i] = self.Mx[i] + self.H()*self.Vx[i]

        # Create results
        self.results = FootingPierAssemblyResults()
        self.results.P = calc_combos("ASD", self.P)
        self.results.Mx = calc_combos("ASD", self.Mx)
        self.results.Vx = calc_combos("ASD", self.Vx)

        for i in range(0, len(self.results.P)):
            fmin, fmax = self.footing.analyze(self.results.P[i], self.results.Mx[i])
            self.results.fmax[i] = fmax
            self.results.fmin[i] = fmin

