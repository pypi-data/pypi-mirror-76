from structural.calc import BaseCalc
from structural import FBC2010

class LightPole(BaseCalc):
    """A light pole for light pole base design"""
    def __init__(self, L, shape, size, V, Kzt=1.0, exposure="C", code=FBC2010):
        self.L = L
        self.V = V
        self.code = code
        self.exposure = exposure
        self.shape = shape.lower()
        self.size = size
        self.fixtures=[]
        self.Kzt = Kzt
        self.G = 0.85
        self.Cf = 2.0
        if self.shape not in ("square", "hexagonal", "round"):
            raise ValueError("Shape type %s not valid" % self.shape)

    def add_fixture(self, b, h, y):
        self.fixtures.append((b, h, y))

    def recalc(self):
        if self.shape == "square":
            self.Kd = 0.90
        else: # hexagonal or round
            self.Kd = 0.95
        self.Kz = self.code.asce7.Kz(z=self.L, exposure=self.exposure,
                case=1)
        self.qz = self.code.asce7.qz(self.V, z=self.L, exposure=self.exposure,
                Kd=self.Kd, Kzt=self.Kzt)
        self.Af = self.size*self.L/12.0
        self.P = self.qz*self.G*self.Cf*self.Af
        self.y = self.L/2.0
        self.Py = self.P*self.y
        for b, h, y in self.fixtures:
            self.P += self.qz*self.G*2.0*(b/12.0)*(h/12)
            self.Py += self.qz*self.G*2.0*(b/12.0)*(h/12)*y
        self.h = self.Py/self.P
        # Convert to ASD level wind
        self.P = self.P*self.code.asce7.ASD_WIND_FACTOR


class LightPoleBase(BaseCalc):
    """Embedded pier type light pole base"""
    def __init__(self, b, pole=None):
        if not isinstance(pole, LightPole):
            self.pole = LightPole(L=20.0, shape="round", size=6)
        self.b = b

