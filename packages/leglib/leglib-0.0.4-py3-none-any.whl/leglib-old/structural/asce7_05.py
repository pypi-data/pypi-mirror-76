"ASCE 7-05 load calculation functions"

from util import almost_equal
from util import interpolate

name = "ASCE7-05"
ASD_WIND_FACTOR = 1.0

#####################################################################
# Wind loads
#####################################################################

def Kz(z, exposure="C", case=1):
    z = float(z)
    exposure = exposure.upper()
    if exposure == "B":
        alpha = 7.0
        zg = 1200.0
    elif exposure == "C":
        alpha = 9.5
        zg = 900.0
    elif exposure == "D":
        alpha = 11.5
        zg = 700.0
    else:
        raise ValueError("exposure %s not allowed" % exposure)

    if z < 15:
        retval = 2.01*((15.0/zg)**(2.0/alpha))
    else:
        retval = 2.01*((z/zg)**(2.0/alpha))
    if exposure=="B" and case==1:
        retval = max(retval, 0.7)
    return retval


def qz(V, z, exposure="C", I=1.0, case=1, Kd=0.85, Kzt=1.0):
    I = float(I)
    Kd = float(Kd)
    Kzt = float(Kzt)
    V = float(V)
    z = float(z)
    _Kz = round(Kz(z, exposure, case), 2)
    return 0.00256*Kzt*_Kz*Kd*V*V*I


def F(V, z, As, exposure="C", I=1.0, G=0.85, Cf=2.0):
    return qz(V, z, exposure, I)*G*Cf*As


#####################################################################
# Snow loads
#####################################################################
def pf(pg, I=1.0, Ce=1.0, Ct=1.0):
    "Flat-roof snow load in psf"
    retval = 0.7*Ce*Ct*I*pg     # ASCE 7-05 Eq. (7-1)
    if pg <= 20:
        retval = max(retval, pg*I)
    else:
        retval = max(retval, 20.0*I)
    return retval

def is_unbalanced(roof):
    return roof.rise > max(0.5, roof.W/70.0)

def snow_density(pg):
    "Returns snow density, gamma, in pcf per ASCE 7-05 Eq. (7-3), p. 83"
    # Limited to 30 pcf max per Eq. (7-3)
    return min(0.13*pg+14.0, 30.0)

def Cs(roof, Ct):
    if almost_equal(Ct, 1.0):
        if roof.slippery:
            x1, y1 = 5.0, 1.0
        else:
            x1, y1 = 30.0, 1.0
        x2, y2 = 70.0, 0.0
    elif almost_equal(Ct, 1.1):
        if roof.slippery:
            x1, y1 = 10.0, 1.0
        else:
            x1, y1 = 37.5, 1.0
        x2, y2 = 70.0, 0.0
    elif almost_equal(Ct, 1.2):
        if roof.slippery:
            x1, y1 = 15.0, 1.0
        else:
            x1, y1 = 45.0, 1.0
        x2, y2 = 70.0, 0.0
    else:
        raise ValueError("Ct must be 1.0, 1.1 or 1.2")
    return min(1.0, max(0.0, interpolate(x1, y1, x2, y2, roof.theta())))

def ps(roof, pg, I=1.0, Ce=1.0, Ct=1.0):
    return Cs(roof, Ct)*pf(pg, I, Ce, Ct)

class SnowDrift:

    def __init__(self, pg, lu, hc, is_leeward=True, I=1.0, Ce=1.0, Ct=1.0):
        self.pg = pg
        self.lu = lu
        self.hc = hc
        self.is_leeward = is_leeward
        self.I = I
        self.Ce = Ce
        self.Ct = Ct
        self.recalc()

    def gamma(self):
        "Snow density in pcf"
        return snow_density(self.pg)

    def recalc(self):
        "Perform calculations and store results"
        self.pf = pf(pg=self.pg, I=self.I, Ce=self.Ce,
                Ct=self.Ct)
        self.hb = self.pf/self.gamma()
        lu = max(self.lu, 25.0)
        self.hd0 = 0.43*(lu)**(1.0/3.0)*(self.pg + 10.0)**(1.0/4.0) - 1.5
        if not self.is_leeward:
            self.hd0 = self.hd0*0.75
        self.hd = min(self.hd0, self.hc - self.hb)
        self.pd = snow_density(self.pg)*self.hd
        self.pm = self.pd + self.pf
        self.is_truncated = not almost_equal(self.hd0, self.hd)
        if self.is_truncated:
            self.w = round(4.0*self.hd0**2/self.hc*2.0)/2.0
        else:
            self.w = round(4.0*self.hd*2.0)/2.0

