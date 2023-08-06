from floatdict import FloatDict
from structural.frame2d import Frame2D
from structural.load_cases import calc_combos
from structural.load_cases import cases
from structural.load_cases import combos
import math
import os


# Module settings
FRAME_A = 10.0
FRAME_E = 29000.0
FRAME_IX = 100.0
MIN_L = 1.0         # beams cannot be less than 1 foot long

class AnalysisResults(dict):

    def __init__(self, _combos):
        self.EIy = [ [] for i in _combos]
        self.Mx = [ [] for i in _combos]
        self.R1 = [0.0 for i in _combos]
        self.R2 = [0.0 for i in _combos]
        self.Vx = [ [] for i in _combos]
        self.R1max = 0.0
        self.R2max = 0.0

    def is_empty(self, case_id):
        "Returns true if all zero values"
        result = self[case_id]
        if result.case.id == 1:
            # Dead Load case is never allowed to be empty
            return False
        if result.case.methodology.id != 1:
            # Load combo is empty if any one of its component cases is empty
            # So, cycle through component cases and return true if one is empty
            for i in [cs.case.id for cs in result.case.combo_set.all()]:
                if self.is_empty(i):
                    return True
            return False
        elif not result.force_empty:
            return not (result.demand0 or result.demand1 or result.demand2 or \
                    result.demand3 or result.demand4)
        else:
            return False


class BeamColumn:
    "2D frame-based flexural component."

    def __init__(self, L):
        self.L = L
        self.axialload_set = []
        self.pointload_set = []
        self.uniformload_set = []
        self.E = 29000.0    # temporary
        self.Ix = 82.8      # temporary

    def validate(self):
        "Validates entries for Lb_x and Lb_y"
        self.L = max(self.L, MIN_L)   # No less than 1 foot long
        return True

    def add_uniform(self, w):
        "Add a uniform load [D, L, Lr, ...] in kips per foot"
        self.uniformload_set.append(w)

#    def get_axial(self, case):
#        "Returns axial load in kips for given load case."
#        return sum([al.get_kips(case.id) for al in self.axialload_set()])


#    def get_uniform(self, case):
#        "Returns uniform load in kips per foot for given load case."
#        return sum([al.get_kips_per_foot(case.id) for al in \
#                self.uniformload_set()])

    def analyze(self):
        _combos = combos["ASD"]
        self.results = AnalysisResults(_combos)
        # Summarize uniform loads
        w0 = [0.0 for i in range(0, len(cases))]
        for wi in self.uniformload_set:
            w0 = [w0[i] + wi[i] for i in range(0, len(wi))]
        self._wset = calc_combos("ASD", w0)
        # Calc each combo
        for c in range(0, len(_combos)):
            self.analyze_case(c)
        # Record frame_results in an AnalysisResult
        self.results.Mmax = max(max([M for M in self.results.Mx]))
        self.results.Mmin = min(min([M for M in self.results.Mx]))
        self.results.Vmax = max(max([V for V in self.results.Vx]))
        self.results.Vmin = min(min([V for V in self.results.Vx]))
        self.results.Ymax = max(self.results.EIy[c])/(self.E*self.Ix)
        self.results.Ymin = min(self.results.EIy[c])/(self.E*self.Ix)
        self.results.R1max = max(self.results.R1)
        self.results.R2max = max(self.results.R2)

    def analyze_case(self, c):
        frame = self.get_frame2D(c)
        frame_results = frame.analyze()
        rxns = frame_results["reactions"]
        defls = frame_results["deflections"]

        # Transfer reactions to intermediate results
        self.results.xs = [n.x/12.0 for n in frame.nodes]
        i_node, j_node = [n.id for n in frame.support_nodes()]
        self.results.R1[c] = rxns[i_node][1]
        self.results.R2[c] = rxns[j_node][1]

        # Transfer deflection to results
        Ys = [y for x, y, theta in defls]
        self.results.EIy[c] = [-Ys[nid]*FRAME_E*FRAME_IX for nid in frame.node_ids()]

        # Transfer shear and moment to results
        xs_v = [0.0]
        xs_v.extend(self.results.xs)    # second shear value at x = 0
        xs_v.append(self.L)     # second shear value at x = L
        Ms = [0.0 for x in self.results.xs]
        Vs = [0.0 for x in xs_v]
        self.results.Mx[c] = [0.0 for x in self.results.xs]
        self.results.Vx[c] = [0.0 for x in self.results.xs]

        for i in range(0, len(self.results.xs)):
            x = self.results.xs[i]
            for nid in frame.node_ids():
                n = frame.nodes[nid]
                P, V, M = rxns[nid]
                if len(n.loads):
                    # Applied loads
                    Pa = sum(load[0] for load in n.loads)
                    Va = sum(load[1] for load in n.loads)
                    Ma = sum(load[2] for load in n.loads)
                else:
                    Pa = Va = Ma = 0.0
                if n.x/12.0 <= x:
                    Ms[i] = Ms[i] + (V + Va)*(x*12.0 - n.x)
                    Vs[i + 1] = Vs[i + 1] + (V + Va)
            self.results.Mx[c][i] = Ms[i]
            self.results.Vx[c][i] = Vs[i + 1]

        # Force the ends of the shear diagrams to equal the reactions
        self.results.Vx[c][i_node] = self.results.R1[c]
        self.results.Vx[c][j_node] = -self.results.R2[c]

    def get_frame2D(self, c):
        "Returns a Frame2D object."
        w = self._wset[c]
        frame = Frame2D()

        # Add starting node
        frame.add_node(0.0, 0.0).pin()

        # Add nodes for each span and midspan
        frame.add_node(self.L*12.0, 0.0).roller_x()
        frame.add_node(self.L*12.0/2.0, 0.0)
        L = self.L

#        # Add node for each point load
#        for pl in self.pointload_set():
#            if pl.x is None:
#                pl.x = 0.0
#                pl.save()
#            x = min(max(pl.x*12.0, 0.0), L*12.0)
#            if x > 0 and x < L*12.0:
#                n = frame.add_node(x, 0.0)
#                n.add_load([0.0, -pl.get_kips(load_case.id), 0.0])

        # TODO: Add nodes at start end and of each *partial* uniform load

        # Add intermediate nodes for 1 foot spacing
        self.results.xs = [n.x for n in frame.nodes]
        self.results.xs.sort()
        for i in range(1, len(self.results.xs)):
            x1, x2 = self.results.xs[i - 1], self.results.xs[i]
            d = math.fabs(x2 - x1)  # distance between nodes in inches
            # One node per 12", not less than 5 segments, but no closer
            # than 3" apart
            segments = min(max(int(d/12.0) + 1, 5), int(d/3.0))
            segment_length = d/segments
            for j in range(1, segments):
                xi = x1 + j*segment_length
                if min(math.fabs(xi - x1), math.fabs(x2 - xi)) > 0.01:
                    self.results.xs.append(xi)
        for x in self.results.xs:
            frame.add_node(x, 0.0)


        # Add members
        frame.renumber_nodes()
        node_ids = frame.node_ids()

        for i in range(1, len(node_ids)):
            m = frame.add_member(i - 1, i, A = FRAME_A, E = FRAME_E,
                    I = FRAME_IX)
            assert m.length() > 0.01, m

        # Add nodal loads for full length uniform loads
        for m in frame.members:
            P = w*m.length()/12.0/2.0
            frame.nodes[m.i.id].add_load((0.0, -P, 0.0))
            frame.nodes[m.j.id].add_load((0.0, -P, 0.0))

        total = 0.0
        for n in frame.nodes:
            for P in n.loads:
                total = total + P[1]

#        # Add nodal load for axial loads
#        for al in self.axialload_set:
#            P = al.get_kips(load_case)
#            if P:
#                frame.nodes[-1].add_load((-P, 0.0, 0.0))

        return frame

