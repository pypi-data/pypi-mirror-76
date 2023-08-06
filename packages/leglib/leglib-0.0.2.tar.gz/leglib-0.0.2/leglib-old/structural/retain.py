from .soil import SoilStratum


class RetainingWall:

    def __init__(self, H=10.0, qs=200.0, beta=0.0, zwt1=None, zwt2=None,
            gamma_water = 62.4):
        self.H = float(H)
        self.qs = float(qs)
        self.beta = float(beta)
        self.zwt1 = zwt1     # Depth to water table, active side
        self.zwt2 = zwt2     # Depth to water table, passive side
        self.soil_strata = []
        self.gamma_water = float(gamma_water)

    def add_soil_stratum(self, z, soil):
        self.soil_strata.append(SoilStratum(z, soil))

    class Node:

        def __init__(self, z, soil, vert, horiz):
            self.z = z
            self.soil = soil
            self.vert = vert
            self.horiz = horiz

        def __unicode__(self):
            return "%s, %s, %s, %s" % (self.z, self.soil, self.vert, self.horiz)

    def _build_nodes(self):
        "Returns list of (i, z, soil)"
        self.nodes = []
        z1 = 0.0
        last_vert = self.qs
        if self.zwt1 is None:
            zw = 99999999.0
        else:
            zw = self.zwt1

        self.soil_strata.sort()

        for stratum in self.soil_strata:
            z2 = stratum.z
            hydro = max(0.0, (z1 - z2)*self.gamma_water)
            self.nodes.append(self.Node(z=z1, soil=stratum.soil,
                vert=last_vert, horiz=last_vert*stratum.soil.Ka()))
            new_vert = last_vert + (z2 - z1)*stratum.soil.gamma_s
            self.nodes.append(self.Node(z=z2, soil=stratum.soil,
                vert=new_vert, horiz=new_vert*stratum.soil.Ka()))
            z1 = z2
            last_vert = new_vert

    def analyze(self):
        self._build_nodes()
#        for n in self.nodes:
#            print n

if __name__ == "__main__":
    import math
    line_wt = 2
    w = RetainingWall(beta = 5.0)
    import matplotlib.pyplot as plt
    Ka = 0.333
    gamma = 110.0

    # Plot the effects of the uniform surcharge
    p1 = Ka*w.qs
    x = [0.0, p1, p1, 0.0]
    y = [0.0, 0.0, w.H, w.H]
    plt.plot(x, y, lw = line_wt)

    # Plot the effects of the active pressure
    p2 = p1 + w.H*gamma*Ka
    x = [0.0, p1, p2, 0.0]
    y = [0.0, 0.0, w.H, w.H]
    plt.plot(x, y, lw = line_wt)

    # Plot the ground surface
    ax = plt.gca()
    xmax = max(max(ax.get_xlim()), math.fabs(min(ax.get_xlim())))
#    print xmax
    x = [0.0, xmax]
    y = [0.0, -xmax*math.sin(math.radians(w.beta))*ax.get_data_ratio()]
    plt.plot(x, y, color="brown", lw=3)

    # Plot the wall itself
    x = [0.0, 0.0]
    y = [0.0, w.H]
    plt.plot(x, y, lw=4, color="black")

    # Reverse the Y axis
    # http://stackoverflow.com/questions/2051744/pyplot-reverse-y-axis
    ax = plt.gca()
    xmax = max(max(ax.get_xlim()), math.fabs(min(ax.get_xlim())))
    ax.set_xlim(-xmax, xmax)
    ax.set_ylim(ax.get_ylim()[::-1])

    # Show the plot
    plt.show()
