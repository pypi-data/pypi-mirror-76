"""ACI reinforcing steel class and helper function.  See ACI 318-05 p. 407."""

class RebarSteel:
    def __init__(self, fy):
        self.fy = fy
        self.E = 29000000.0

    @property
    def ey(self):
        "Returns yield strain"
        return self.fy/self.E

    def __str__(self):
        return "Steel fy = %d psi" % int(self.fy)

a615_grade60 = RebarSteel(fy = 60000.0)


class Rebar:
    def __init__(self, name, db, Ab, wt):
        self.name = name    # e.g. "#4"
        self.db = db        # Bar diameter in inches
        self.Ab = Ab        # Bar area, sq in
        self.wt = wt        # Bar weight, lbs/foot

    def __str__(self):
        return self.name


bars = {
    "#3" : Rebar("#3", 0.375, 0.11, 0.376),
    "#4" : Rebar("#4", 0.500, 0.20, 0.668),
    "#5" : Rebar("#5", 0.625, 0.31, 1.043),
    "#6" : Rebar("#6", 0.750, 0.44, 1.502),
    "#7" : Rebar("#7", 0.875, 0.60, 2.044),
    "#8" : Rebar("#8", 1.000, 0.79, 2.670),
    "#9" : Rebar("#9", 1.128, 1.00, 3.400),
    "#10" : Rebar("#10", 1.270, 1.27, 4.303),
    "#11" : Rebar("#11", 1.410, 1.56, 5.313),
    "#14" : Rebar("#14", 1.693, 2.25, 7.650),
    "#18" : Rebar("#18", 2.257, 4.00, 13.600)
}


def get_bar(name):
    if type(name) == type("Joe"):
        return bars[name]
    elif type(name) == type(73):
        return bars["#%d" % name]
