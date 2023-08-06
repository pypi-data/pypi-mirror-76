from structural import IBC2009
from structural.calc import BaseCalc
from structural.roof import Roof

class SnowCalc(BaseCalc):

    def __init__(self, pg, W, rise=0.25, Ce=1.0, Ct=1.0, I=1.0,
            is_leeward=True, code=IBC2009, title="", project="",
            project_number="", by=""):
        super(SnowCalc, self).__init__(title, project, project_number, by)
        self.rise = rise
        self.W = W
        self.Ce = Ce
        self.Ct = Ct
        self.I = I
        self.code = code
        self.pg = pg
        self.is_leeward = is_leeward
        self.recalc()

    def gamma(self):
        "Snow density in pcf"
        return self.code.asce7.snow_density(self.pg)

    def recalc(self):
        self.roof = Roof(rise=self.rise, W=self.W)
        self.pf = self.code.asce7.pf(self.pg, self.I, self.Ce, self.Ct)
        self.hb = self.pf/self.gamma()
        self.Cs = self.code.asce7.Cs(self.roof, self.Ct)
        self.ps = self.code.asce7.ps(self.roof, self.pg, self.I, self.Ce, self.Ct)
