#!/bin/env python
from .footing import Footing
from leglib import fmt
from matplotlib import pyplot as plt
from portal import PortalFrame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

interaction_polygon = (
        (0.0, 0.0),
        (596, 0.0),
        (600, 150.0),
        (608, 350),
        (627, 500),
        (632, 600),
        (632, 650),
        (600, 940),
        (574, 1080),
        (324, 1325),
        (0, 1325),
        (0, 0)
)

pg = Polygon(interaction_polygon)

MIN_ASPECT = 1.0
MAX_ASPECT = 4.0
ASPECT_INC = 0.125
PLOT_DPI = 300

def plot_interaction_24(filename="interaction24.png"):
    global interaction_polygon
    xs = [p[0] for p in interaction_polygon]
    ys = [p[1] for p in interaction_polygon]
    plt.close()
    plt.plot(xs, ys)
    plt.savefig(filename)
    plt.close()

def check(M, P):
    global pg
    pt = Point(M, P)
    return pg.contains(pt)



class PileGroup:
    """
    Rectangular group of piles
    s = Spacing in feet
    H = Exposed "stick height" in feet
    """

    def __init__(self, rows=2, cols=2, s=6.0, H=15.0):
        self.rows = rows
        self.cols = cols
        self.s = s
        self.H = H
        self.edge_dist = 2.0

    def n(self):
        return self.rows*self.cols

    def Wftg(self):
        "Returns weight of footing in kips"
        self.ftg = Footing(B=2.0*max(self.yrng()) + 2*self.edge_dist, L = 2.0*max(self.xrng()) + 2*self.edge_dist, T = 6.0)
        return self.ftg.W()

    def xrng(self):
        return [i*self.s - self.xbar() for i in range(0, self.cols)]

    def yrng(self):
        return [i*self.s - self.ybar() for i in range(0, self.rows)]

    def analyze_group_action(self, P=0.0, M=0.0):
        """Calculates worst-case force in the pile"""
        return P/self.n() + M*max(self.xrng())/self.Ix()

    def analyze(self, P, M, V):
        """
        Analyze a rectangular pile group for forces:
        P = axial downward in kips
        V = lateral in kips
        M = moment about X axis in kip-ft
        """
        # Each row becomes a portal frame
        # Each column becomes a column in the portal frame
        f = PortalFrame(H=self.H*1.5, L=self.s, cols=self.cols)
        f.analyze(V/self.rows)
        self.Mcol = f.M
        self.Pcol = f.R
#         f.plot()

    def xbar(self):
        return (self.cols - 1)*self.s/2.0

    def ybar(self):
        return (self.rows - 1)*self.s/2.0

    def Ix(self):
        return self.rows*sum([x**2 for x in self.xrng()])

    def Iy(self):
        return self.cols*sum([y**2 for y in self.yrng()])

    def plot_plan(self, filename):
        plt.close()
        xrng = self.xrng()
        yrng = self.yrng()
        xs = []
        ys = []

        # Calculate pile coordinates
        for i in range(0, len(xrng)):
            for j in range(0, len(yrng)):
                xs.append(xrng[i])
                ys.append(yrng[j])

        # Plot axes
        plt.plot((0, 0), (min(xs)*1.2, max(xs)*1.2), linestyle="-.", color="darkgrey")
        plt.plot((min(xs)*1.2, max(xs)*1.2), (0, 0), linestyle="-.", color="darkgrey")

        # Plot piles
        plt.scatter(xs, ys, marker='s')
        plt.scatter(0, 0, marker='+')

        # Plot footing
        x1 = min(xrng) - self.edge_dist
        x2 = max(xrng) + self.edge_dist
        y1 = min(yrng) - self.edge_dist
        y2 = max(yrng) + self.edge_dist
        xs = [x1, x2, x2, x1, x1]
        ys = [y1, y1, y2, y2, y1]
        plt.plot(xs, ys)

        # Make it square
        ymin, ymax = plt.xlim()
        plt.ylim( (ymin, ymax) )

        # Finalize and write
        plt.title("Pile Layout: %.0f feet of Water\n%d x %d = %d Piles" % (self.H, self.rows, self.cols, self.n()))
        plt.savefig(filename, dpi=PLOT_DPI)

    def plot_elev(self, filename):
        plt.close()
        xrng = self.xrng()
        xs = []
        ys_top = []
        ys_bot = []

        # Plot the piles
        for i in range(0, len(xrng)):
            xs.append(xrng[i])

        # Plot axes
        plt.plot((0, 0), (min(xs)*1.2, max(xs)*1.2), linestyle="-.", color="darkgrey")

        # Plot the piles
        for i in range(0, len(xrng)):
            plt.plot((xrng[i], xrng[i]), (-2.0, -self.H), color="black", linewidth=2.0)

        # Plot footing
        x1 = min(xrng) - self.edge_dist
        x2 = max(xrng) + self.edge_dist
        y1 = -3.0
        y2 = 3.0
        xs = [x1, x2, x2, x1, x1]
        ys = [y1, y1, y2, y2, y1]
        plt.plot(xs, ys)

        # Make it square
        ymin, ymax = plt.xlim()
        plt.ylim( (ymin, ymax) )

        # Finalize and write
        plt.title("Pile Cap Elevation: %.0f feet of Water\n%d x %d = %d Piles" % (self.H, self.rows, self.cols, self.n()))
        plt.savefig(filename, dpi=PLOT_DPI)


    def rotate(self):
        c = self.cols
        self.cols = self.rows
        self.rows = c


    def design(self, P, M, V):
        """
        Design for axial force, P (kips), moment M (kip-ft), and horizontal
        force V (kips)
        """
        aspect = MIN_ASPECT
        min_num = 10**10
        min_rows_cols = None
        while aspect <= MAX_ASPECT:
            self.rows = 2
            passes = False
            while not passes:
                self.cols = int(self.rows*aspect)
#                 print("%d rows, %d cols" % (self.rows, self.cols))
                self.analyze(P=P+1.25*self.Wftg(), M=M, V=V)
#                 print("Force in column due to portal frame action: Pu = %.1f kips" % self.Pcol)
                self.Pcol = self.Pcol + self.analyze_group_action(P=P, M=M)
#                 print("Force in column:  Pu = %.1f kips" % self.Pcol)
#                 print("Moment in column: Mu = %.0f kip-ft" % self.Mcol)
                passes = check(P=self.Pcol, M=self.Mcol)
                if passes:
                    # Check longitudinal direction
                    self.rotate()
                    self.analyze(P=P, M=0.0, V=V/2.0)
                    self.Pcol = self.Pcol + self.analyze_group_action(P=P, M=M)
                    passes = passes and check(P=self.Pcol, M=self.Mcol)
                    if passes:
                        # Passed both ways, let's see if it's the best
                        if self.n() < min_num:
                            min_num = self.n()
                            min_rows_cols = (self.rows, self.cols)
                    self.rotate() # restore it
                else:
                    self.rows = self.rows + 1
            aspect = aspect + ASPECT_INC
        self.cols, self.rows = min_rows_cols
        self.analyze(P=P+1.25*self.Wftg(), M=M, V=V)
        print(("Winning combination: %d rows x %d columns" % (self.rows,
            self.cols)))
        print(("Footing size = %s x %s x %s" % (fmt.ft_in(self.ftg.L*12),
            fmt.ft_in(self.ftg.B*12), fmt.ft_in(self.ftg.T*12))))
        print(("Footing weight = %.0f kips" % self.Wftg()))
        self.plot_plan(filename="depth%.0f_plan.png" % (self.H))
        self.plot_elev(filename="depth%.0f_elev.png" % (self.H))


if __name__ == '__main__':
    # Forces from Homework #1: PD = 1340 kips, PL = 408 kips (2 lanes), MLL =
    # 3672 kip-ft.
    for H in [15.0, 30.0, 50.0]:
        print("===============================================================")
        print(("Stick height, H = %.0f ft" % H))
        print(("Design stick height, H = 1.5(H - 3) = %.1f ft" % (1.5*(H - 3.0))))
        grp = PileGroup(H=H)
        # Combine loads per Extreme Event II
        grp.design(P=1.25*1340 + 0.5*408, M=3672*0.5, V=2000.0)

