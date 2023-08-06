from .calc import BaseCalc
from .concrete import Concrete
from .soil import Soil
from . import asce7_05 as asce

FS_REQ1 = 1.25  # Required factor of safety per ACI 350.4R-04 Section 3.1.2
FS_REQ2 = 1.1   # Special case of flooded, empty excavation

class Pit(BaseCalc):

    def __init__(self, Lp, Bp, dp, Ltoe=1.0, tp=12.0, tf=18.0, Hg=0.0,
            dwt=0.0, concrete=Concrete(), soil=Soil(), title="",
            project=None, project_number="", by=""):
        super(Pit, self).__init__(title, project,
                project_number, by)
        self.Lp = Lp        # Length of pit, feet
        self.Bp = Bp        # Width of pit, feet
        self.dp = dp        # Depth of pit, feet
        self.Ltoe = Ltoe    # Toe length, feet
        self.tp = tp        # Wall thickness, inches
        self.tf = tf        # Footing thickness, inches
        self.Hg = Hg        # Top of wall to top of grade, feet
        self.dwt = dwt      # Depth to water table from top of wall, feet
        self.concrete = concrete
        self.soil = soil
        self.gamma_w = 62.4 # Density of water in pcf


    def recalc(self):
        # Total height of pit
        self.Hp = self.dp + self.Hg

        # Volume of concrete in the walls in cubic feet
        self.Vp = ((self.Bp + 2.0*self.tp/12.0)*(self.Lp + 2.0*self.tp/12.0) -
            self.Bp*self.Lp)*self.Hp

        # Dimensions of pit
        self.Lpo = self.Lp + 2.0*self.tp/12.0
        self.Bpo = self.Bp + 2.0*self.tp/12.0
        self.Hp = self.dp + self.Hg

        # Weight of concrete in walls, kips
        self.Wp = self.Vp*self.concrete.gamma_c/1000.0

        # Width of footing, feet
        self.Bf = self.Bp + 2.0*(self.tp/12.0 + self.Ltoe)

        # Length of footing, feet
        self.Lf = self.Lp + 2.0*(self.tp/12.0 + self.Ltoe)

        # Area of footing, feet
        self.A = self.Lf*self.Bf

        # Volume of concrete in the footing in cubic feet
        self.Vf = self.Lf*self.Bf*self.tf/12.0

        # Weight of concrete in footing, kips
        self.Wf = self.Vf*self.concrete.gamma_c/1000.0

        # Total volume of concrete, cubic feet
        self.Vc = self.Vp + self.Vf

        # Total weight of concrete, kips
        self.Wc = self.Vc*self.concrete.gamma_c/1000.0

        # Volume of soil in cubic feet
        self.Vs = (self.Lf*self.Bf - (self.Lpo)*(self.Bpo))*(self.dp)

        # Volume and weight of dry soil in cubic feet
        self.Vdry = (self.A - self.Lpo*self.Bpo)*min(self.dp, self.dwt)
        self.Wdry = self.Vdry*self.soil.gamma_s/1000.0

        # Volume and weight of saturated soil in cubic feet
        self.Vsat = self.Vs - self.Vdry
        self.Wsat = self.Vsat*self.soil.gamma_sat/1000.0

        # Total weight of soil
        self.Ws = self.Wdry + self.Wsat

        # Total dead load
        self.Wtot = self.Wc + self.Ws

        self._recalc_buoyancy()
        self._recalc_bearing()
        self.U = max(self.Uup1, self.Uup2, self.Ubrg)

    def _recalc_buoyancy(self):
        # Unity check for uplift
        self.FSreq1 = FS_REQ1
        self.FSreq2 = FS_REQ2

        # Height of water above bottom of footing
        self.Hwater = self.dp + self.tf/12.0 - self.dwt

        # Buoyancy force
        self.Pup1 = self.gamma_w*self.Hwater*self.A/1000.0
        self.Pup2 = (self.Vf + self.Lpo*self.Bpo*(self.dp - self.dwt))*self.gamma_w/1000.0

        # Factor of safety and unity
        self.FSup1 = round(self.Wtot/self.Pup1, 2)
        if self.FSup1:
            self.Uup1 = round(self.FSreq1/self.FSup1, 2)
        else:
            self.Uup1 = 0.0
        self.FSup2 = round(self.Wc/self.Pup2, 2)
        if self.FSup2:
            self.Uup2 = round(self.FSreq2/self.FSup2, 2)
        else:
            self.Uup2 = 0.0

    def _recalc_bearing(self):
        # TODO: Add equipment loads:
        self.P = self.Wtot
        self.f = self.P/self.A*1000.0   # Bearing pressure in psf
        self.Ubrg = self.f/self.soil.Qa

    def design(self):
        self._design_Ltoe()

    def _design_Ltoe(self):
        "Vary Ltoe until unity is met"
        i = 12       # Starting Ltoe in inches
        self.Ltoe = i/12.0
        self.recalc()
        while self.U >= 1.00:
            i = i + 1
            self.Ltoe = i/12.0
            self.recalc()

