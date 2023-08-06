class Cap(float):
    "Capacity"
    def __new__(cls, Rn, phi=0.75, omega=2.00):
        assert Rn >= 0.0
        return float.__new__(cls, Rn)

    def __init__(self, Rn, phi, omega):
        assert phi <= 1.0
        assert phi > 0.0
        assert omega >= 1.0
        self.phi = phi
        self.omega = omega

    def Rn_omega(self):
        return self/self.omega

    def phiRn(self):
        return self.phi*self

    def asd(self):
        return self.Rn_omega()

    def lrfd(self):
        return self.phiRn()

    def Rn(self):
        return self
