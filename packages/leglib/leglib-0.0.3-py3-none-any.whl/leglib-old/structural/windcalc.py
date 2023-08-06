from structural import FBC2010
from structural.calc import BaseCalc

class WindCalc(BaseCalc):

    def __init__(self, V, z, exposure="C", Kd=0.85, Kzt=1.0, code=FBC2010,
            title="", project=None, project_number="", by=""):
        super(WindCalc, self).__init__(title, project, project_number, by)
        self.exposure = exposure
        self.z  = z
        self.V = V
        self.Kd = Kd
        self.Kzt = Kzt
        self.code = code
        self.name = "WindCalc"
        self.recalc()
        self.G = 0.85

    def recalc(self):
        if not hasattr(self, "G"):
            self.G = 0.85
        self.Kz = self.code.asce7.Kz(z=self.z, exposure=self.exposure,
                case=1)
        self.qz = self.code.asce7.qz(self.V, z=self.z, exposure=self.exposure,
                Kd=self.Kd, Kzt=self.Kzt)

