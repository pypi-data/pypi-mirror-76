from .acibars import get_bar
from .concrete import Concrete
import math

Es = 29000.0            # ksi
LBS_PER_KIP = 1000.0
sigma_c = 0.003         # ACI 318-05 Section 10.2.3, p. 119
INC = 0.1


class BarRow:
    def __init__(self, n, barsize, ds):
        self.barsize = barsize
        self.ds = ds
        self.n = n

    def __unicode__(self):
        return "%d-%s at ds = %.2f" % (self.n, self.bar(), self.ds)

    def __str__(self):
        return str(self).encode("utf-8")

    def bar(self):
        return get_bar(self.barsize)

    def Ast(self):
        return self.bar().Ab*self.n


class RectTiedColumn:
    "A square tied column with equal bars on all sides"

    def __init__(self, b=24.0, h=24.0, nx=3, ny=3, barsize=8, tiebarsize=4,
            fc=4000.0, fy=60000.0, cover=1.5):
        self.b = float(b)
        self.h = float(h)
        self.nx = int(nx)
        self.ny = int(ny)
        assert nx >= 2
        assert ny >= 2
        assert barsize in (3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 18)
        assert tiebarsize in (3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 18)
        self.barsize = barsize
        self.tiebarsize = tiebarsize
        self.fc = float(fc)
        self.fy = float(fy)
        self.cover = float(cover)
        self.phi_c = 0.65
        self.phi_b = 0.90

    def n(self):
        return 4 + 2*(self.nx - 2) + 2*(self.ny - 2)

    def Ag(self):
        return self.b*self.h

    def bar(self):
        return get_bar(self.barsize)

    def tiebar(self):
        return get_bar(self.tiebarsize)

    def concrete(self):
        return Concrete(self.fc, 145)

    def sx(self):
        "Returns spacing between vertical bars parallel to x-axis"
        return (self.b - 2*self.cover - 2*self.tiebar().db -
                self.bar().db)/(self.nx - 1)

    def sy(self):
        "Returns spacing between vertical bars parallel to y-axis"
        return (self.h - 2*self.cover - 2*self.tiebar().db -
                self.bar().db)/(self.ny - 1)

    def dx(self, i):
        "Return depth to bar row i, which is zero-indexed, x-direction"
        return self.cover + self.tiebar().db + self.bar().db/2.0 + self.sx()*i

    def dy(self, i):
        "Return depth to bar row i, which is zero-indexed, y-direction"
        return self.cover + self.tiebar().db + self.bar().db/2.0 + self.sy()*i

    def Ast(self):
        return self.bar().Ab*self.n()

    def Ast_per_side(self):
        return self.Ast()/4.0

    def Pn_max(self):
        "Returns Pn,max per ACI 318-05 Section 10.3.6.2"
        return 0.8*(0.85*self.fc*(self.Ag() - self.Ast()) +
                self.fy*self.Ast())/LBS_PER_KIP

    def phiPn_max(self):
        return self.phi_c*self.Pn_max()

    def rows_y(self):
        "Returns a list of bar rows about x-axis"
        retval = []
        for i in range(0, self.ny):
            if i == 0 or i == self.ny - 1:
                n = self.nx
            else:
                n = 2
            retval.append(BarRow(n = n, barsize = self.barsize, ds = self.dy(i)))
        return retval

    def case_1(self):
        "Return phiPn, phiMn at phiPn = phiPn_max"
        Pn_max = self.Pn_max()
        fc = self.fc/1000.0
        Pbars = self.Ast()*self.fy/1000.0
        a = (Pn_max-Pbars)/(0.85*fc*self.b)

        rows = self.rows_y()
        beta1 = self.concrete().beta1()

        dsn = max([row.ds for row in rows])

        Mvals = []
        Pvals = []

        c = 0.0
        Mn = 1.0

        while Mn > 0.0:
            c = c + INC
            a = c*beta1
            for row in rows:
                row.sigma_s = (row.ds - c)*sigma_c/c
                row.fs = max(min(row.sigma_s*Es, self.fy/1000.0), -self.fy/1000.0)
                if row.ds < a:
                    # Bar is in compression zone, so subtract conc strength
                    row.fs = row.fs - 0.85*self.fc/1000.0
                row.force = row.fs * row.Ast()
            Fs = sum([row.force for row in rows])
            Cc = a*self.b*0.85*self.fc/1000.0
            Mn = sum([row.force*(row.ds - self.h/2.0) for row in rows]) - Cc*(a/2.0 - self.h/2.0)
            Pn = min(Cc - Fs, Pn_max)
            sigma_t = max([row.sigma_s for row in rows])
            if sigma_t >= 0.005:
                # Tension controlled
                phi = self.phi_b
            elif sigma_t >= 0.002:
                # Compression controlled
                phi = self.phi_c
            else:
                # Transition zone between tension- and compression-controlled
                phi = self.phi_c + (self.phi_b - self.phi_c)/(0.005 - 0.002)*(sigma_t - 0.002)
#            print "%s, %s, %s, %.4f, %.2f" % (c, Pn, Mn, sigma_t, phi)
            Mvals.append(phi*Mn/12.0)
            Pvals.append(phi*Pn)

#        print "Pmax = %s" % max(Pvals)
#        print "Mmax = %s" % max(Mvals)

#        import matplotlib.pyplot as plt

#        plt.plot(Mvals, Pvals)
#        plt.xlabel("Moment, kip-in")
#        plt.ylabel("Axial, kip")
#        plt.axhline()
#        plt.savefig("plot.png")

    def solve(self):
        xvals = []
        yvals = []
        beta1 = self.concrete().beta1()
        fc = self.fc/1000.0
        fy = self.fy/1000.0
        rows = self.rows_y()
        ds_max = max([row.ds for row in rows])
        outer_row = None
        for row in rows:
            if math.fabs(row.ds - ds_max) <= 0.001:
                outer_row = row
        assert(outer_row is not None)
        sigma_y = fy/Es
#        print sigma_y
        Z = 1.0
        while Z >= -1000.0:
            sigma_max = Z*sigma_y
            c = sigma_c*(outer_row.ds/(sigma_c - sigma_max))
            a = min(beta1*c, self.h)
#            print "%.2f, %.6f, %.2f, %.2f" % (Z, sigma_max, c, a)
            Z = Z - INC
            for row in rows:
                row.sigma_s = sigma_c*(c - row.ds)/c
                row.fs = min(row.sigma_s*Es, fy)
                if row.fs > 0.0:
                    row.fs = row.fs - 0.85*fc
                row.force = row.Ast()*row.fs
#                print row, row.sigma_s, row.fs, row.force
            Cc = 0.85*fc*a*self.b
#            print "Cc = %.2f" % Cc
            Pn = Cc + sum([row.force for row in rows])
            # Start here:
            Mn = Cc*a/2.0 - Pn*self.h/2.0 + sum([row.force*row.ds for row in rows])
#            print "Pn = %.2f" % Pn
#            print "Mn = %.2f" % (Mn/12.0)

if __name__ == '__main__':
#    col = RectTiedColumn(b=12.0, h=24.0, nx=2, ny=5, barsize=14,
#            tiebarsize=4, fc=6000, cover=1.5)
#    col = RectTiedColumn(b=14.0, h=24.0, nx=3, ny=2, barsize=9,
#            tiebarsize=4, fc=4000, cover=1.436)
#    col = RectTiedColumn(b=24.0, h=24.0, nx=3, ny=3, barsize=6,
#            tiebarsize=4, fc=4000, cover=1.436)
#    col.case_1()
#    col = RectTiedColumn(b=12.0, h=12.0, nx=2, ny=2, barsize=8,
#            tiebarsize=4, fc=4000, cover=1.5)
    col = RectTiedColumn(b=18.0, h=18.0, nx=2, ny=2, barsize=6,
            tiebarsize=4, fc=4000.0, cover=2.0)
    x,y = col.solve()
#    import matplotlib.pyplot as plt
#    plt.plot(x, y)
#    import pdb; pdb.set_trace()
#    plt.show()


