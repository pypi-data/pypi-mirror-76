from structural.frame2d import Frame2D
import math
import unittest

FRAME_A = 10.0
FRAME_E = 29000.0
FRAME_IX = 100.0
KIPS_PER_FOOT = 2.5

# 2.5*25^2/8 = 195.3125

#class PointLoad:

#    def __init__(self, x, P):
#        self.x = x
#        self.P = P

#pointload_set = [PointLoad(5.5, 10.0), PointLoad(13.4, 8.0)]


class TestFrame2D(unittest.TestCase):

    def setUp(self):
        self.results = {}
        self.results["xs"] = []
        self.L = 25.0
        "Returns a Frame2D object."
        self.frame = Frame2D()

        # Add starting node
        self.frame.add_node(0.0, 0.0).pin()

        # Add nodes for each span
        self.frame.add_node(self.L*12.0, 0.0).roller_x()
        L = self.L

        # Add node for each point load
#        for pl in pointload_set:
#            x = min(max(pl.x*12.0, 0.0), L*12.0)
#            if x > 0 and x < L*12.0:
#                n = self.frame.add_node(x, 0.0)
#                n.add_load([0.0, -pl.P, 0.0])

        # TODO: Add nodes at start end and of each *partial* uniform load

        # Add intermediate nodes for 1 foot spacing
        self.results["xs"] = [n.x for n in self.frame.nodes]
        self.results["xs"].sort()
        for i in range(1, len(self.results["xs"])):
            x1, x2 = self.results["xs"][i - 1], self.results["xs"][i]
            d = math.fabs(x2 - x1)  # distance between nodes in inches
            # One node per 12", not less than 5 segments, but no closer
            # than 3" apart
            segments = min(max(int(d/12.0) + 1, 5), int(d/3.0))
            segment_length = d/segments
            for j in range(1, segments):
                xi = x1 + j*segment_length
                if min(math.fabs(xi - x1), math.fabs(x2 - xi)) > 0.01:
                    self.results["xs"].append(xi)
        for x in self.results["xs"]:
            self.frame.add_node(x, 0.0)

        # Add members
        self.frame.renumber_nodes()
        node_ids = self.frame.node_ids()
        for i in range(1, len(node_ids)):
            m = self.frame.add_member(i - 1, i, A = FRAME_A, E = FRAME_E,
                    I = FRAME_IX)
            assert m.length() > 0.01, m

        # Add nodal loads for full length uniform loads
        w = KIPS_PER_FOOT
        for m in self.frame.members:
            P = w*m.length()/12.0/2.0
            self.frame.nodes[m.i.id].add_load((0.0, -P, 0.0))
            self.frame.nodes[m.j.id].add_load((0.0, -P, 0.0))

#        # Add nodal load for axial loads
#        for al in self.axialload_set():
#            P = al.get_kips(load_case)
#            if P:
#                self.frame.nodes[-1].add_load((-P, 0.0, 0.0))



    def test_analysis(self):
        results = self.frame.analyze()
        # Check reactions
        # 2.5*25/2 = 31.25
        self.assertAlmostEqual(max([r[1] for r in results["reactions"]]),
                31.25, places=2)
        # Check shear
        # 2.5*25/2 = 31.25



if __name__ == '__main__': # pragma: no cover
    unittest.main()

