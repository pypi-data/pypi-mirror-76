from structural import FBC2010
from structural.calc import BaseCalc

class WindOtherStructureCalc(BaseCalc):

    def __init__(self, V, exposure="C", Kd=0.85, Kzt=1.0, code=FBC2010,
            title="", project=None, project_number="", by=""):
        super(WindOtherStructureCalc, self).__init__(title, project,
                project_number, by)
        self.exposure = exposure
        self.V = V
        self.Kd = Kd
        self.Kzt = Kzt
        self.code = code
        self.name = "WindOtherStructureCalc"
        self.areas=[]   # constituent areas
        self.G = 0.85
        self.recalc()

    def add_area(self, z, Af, Cf=2.0, name=None):
        if name is None:
            i = 1
            next_name = "Area%d" % i
            while next_name in [a["name"] for a in self.areas]:
                i = i + 1
                next_name = "Area%d" % i
        self.areas.append({ "z" : z, "Af" : Af, "Cf" : Cf, "name" : name })


    def recalc(self):
        # Calculate z based upon constituent areas
        self.z = 15.0       # minimum height in feet
        self.Af = 0.0       # total area in sq feet
        self.zbar = 0.0     # average height of constituent areas
        if len(self.areas):
            self.z = max(max([a["z"] for a in self.areas]), 15)
            self.Af = sum([a["Af"] for a in self.areas])
            self.CfAf = sum([a["Cf"]*a["Af"] for a in self.areas])
            self.zbar = sum([a["Af"]*a["z"] for a in self.areas])/self.Af
        self.Kz = self.code.asce7.Kz(z=self.z, exposure=self.exposure,
                case=1)
        self.qz = self.code.asce7.qz(self.V, z=self.z, exposure=self.exposure,
                Kd=self.Kd, Kzt=self.Kzt)

        # Calculate resultant force, P and moment M
        self.P = 0.0
        self.M = 0.0
        self.P = sum([a["Af"]*a["Cf"]*self.G*self.qz for a in self.areas])/1000.0
        self.M = sum([a["Af"]*a["Cf"]*a["z"]*self.G*self.qz for a in self.areas])/1000.0

        # Calculate height of resultant, h
        if self.P > 0.0:
            self.h = self.M/self.P
        else:
            self.h = None

