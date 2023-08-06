from geom import Line
from geom import Point
from geom import Polygon
from geom import Segment
from geom import Vector
from geom import dist
import unittest


class TestGeom(unittest.TestCase):

    def setUp(self):
        self.p1 = Point(0.0, 0.0)
        self.p2 = Point(5.0, 5.0)
        self.p3 = Point(6.0, 4.0)
        self.p4 = Point(6.0, -1.0)
        self.seg1 = Segment(self.p1, self.p2)
        self.seg2 = Segment(self.p3, self.p4)
        self.line1 = Line(self.p1, self.p2)
        self.line2 = Line(self.p3, self.p4)
        self.pointA = Point(3,3)
        self.pointB = Point(8,8)
        self.poly = Polygon((Point(-1, -1), Point(6, -1), Point(5, 6),
            Point(0, 5)))
        self.square = Polygon((Point(0.0, 0.0), Point(6.0, 0.0),
            Point(6.0, 5.0), Point(0.0, 5.0)))

    def test_repr(self):
        self.assertEqual(self.p2.__repr__(), "Point(5.0, 5.0)")
        self.assertEqual(self.line1.__repr__(), "[(0.0, 0.0)..(5.0, 5.0)]")

    def test_get_tuple(self):
        self.assertTrue(isinstance(self.p1.get_tuple(), tuple))

    def test_point_introspection(self):
        self.assertAlmostEqual(self.p1.x, self.p1[0], places=6)
        self.assertAlmostEqual(self.p4.y, self.p4[1], places=6)
        self.assertRaises(IndexError, self.p1.__getitem__, 2)

    def test_point_copy(self):
        p = self.p1.copy((2.4, -1.22))
        self.assertAlmostEqual(p.x, 2.4, places=6)
        self.assertAlmostEqual(p.y, -1.22, places=6)

    def test_line_introspection(self):
        self.assertAlmostEqual(self.line2.x1, 6.0, places=6)
        self.assertAlmostEqual(self.line2.y1, 4.0, places=6)
        self.assertAlmostEqual(self.line2.x2, 6.0, places=6)
        self.assertAlmostEqual(self.line2.y2, -1.0, places=6)
        midpt = self.line2.midpoint()
        self.assertAlmostEqual(midpt.x, 6.0, places=6)
        self.assertAlmostEqual(midpt.y, 1.5, places=6)
        self.assertFalse(self.line1.is_vertical())
        self.assertTrue(self.line2.is_vertical())
        self.assertTrue(self.line2.slope() is None)
        self.assertAlmostEqual(self.line1.slope(), 1.0, places=6)
        self.assertAlmostEqual(self.line1.yintercept(), 0.0, places=6)
        self.assertTrue(self.line2.yintercept() is None)

    def test_point_and_dist(self):
        self.assertEqual("%s" % self.p1, "(0.0, 0.0)")
        self.assertEqual("%s" % self.p2, "(5.0, 5.0)")
        self.assertFalse(self.p1 == self.p2)
        self.assertTrue(self.p1 == self.p1)
        # Length should be sqrt(5^2 + 5^2) = 7.071
        self.assertAlmostEqual(dist(self.p1, self.p2), 7.071, places=3)
        self.assertAlmostEqual(self.p1.dist(self.p2), 7.071, places=3)
        # Test distance between a point and a line (perpendicular dist)
        # Correct answer determined using AutoCAD software
        self.assertAlmostEqual(self.p3.dist(self.line1), 1.4142, places=4)
        self.assertTrue(self.p3.dist("Joe") is None)

    def test_point_move(self):
        p = Point(1.0, 3.0)
        p.move(0.75, -2.3)
        self.assertAlmostEqual(p.x, 1.75, places=3)
        self.assertAlmostEqual(p.y, 0.70, places=3)

    def test_point_rotate(self):
        # Rotate point about origin
        p = Point(1.0, 3.0)
        p.rotate(angle=0.5)
        # Correct answer determined using AutoCAD software
        self.assertAlmostEqual(p.x, -0.56069405, places=3)
        self.assertAlmostEqual(p.y, 3.11217322, places=3)

    def test_segment(self):
        self.assertEqual("%s" % self.seg1, "(0.0, 0.0)-(5.0, 5.0)")
        self.assertEqual(self.seg1.intersection(self.seg2), None)
        self.assertEqual(self.seg1.intersection(self.seg1), None)

    def test_line(self):
        # Length should be sqrt(5^2 + 5^2) = 7.071
        self.assertAlmostEqual(self.line1.length(), 7.071, places=3)
        self.assertEqual(self.line1.intersection(self.line2), Point(6.0, 6.0))
        self.assertEqual(self.line1.intersection(self.line1), None)

    def test_polygon(self):
        self.assertTrue(self.poly.point_within(self.pointA))
        self.assertFalse(self.poly.point_within(self.pointB))
        # Area of square = 6*5 = 30
        self.assertAlmostEqual(self.square.area(), 30.0, places=2)

    def test_point_constructors(self):
        pt1 = (4.5, -5.4)
        pt2 = Point.from_tuple(pt1)
        pt3 = Point(x =4.5, y=-5.4)
        pt4 = Point.from_point(pt3)
        self.assertAlmostEqual(pt1[0], pt2.x, places=6)
        self.assertAlmostEqual(pt1[1], pt2.y, places=6)
        self.assertAlmostEqual(pt1[0], pt3.x, places=6)
        self.assertAlmostEqual(pt1[1], pt3.y, places=6)
        self.assertAlmostEqual(pt1[0], pt4.x, places=6)
        self.assertAlmostEqual(pt1[1], pt4.y, places=6)


#    # Test point rotation about another point
#    p5 = Point(8.0, 7.0)                # Original point
#    p6 = Point(8.0, 7.0)                # Original point to be rotated
#    p6.rotate(math.radians(30), p2)     # Rotate about point p2

#    # Test polygon offset
#    poly2 = Polygon((Point(0, 6), Point(4, 2), Point(10,0), Point(9, 9), Point(5, 11)))
#    poly2.offset(1, True)
#    for p in poly2.points:
#        print p
#    poly2.get_segments()
##    poly2.plot()

#    print line1.dir_vector(), line2.dir_vector()

#    print "Test distance from pt1 to pt2: %s" % (p1.dist(p2))
#    print "Test distance from %s to %s: %s" % (p1, seg2, seg2.dist_to_pt(p1))
#    seg3 = Segment(Point(1.0, 2.0), Point(3.0, 3.0))
#    print "Test distance from %s to %s: %s" % (p1, seg3, seg3.dist_to_pt(p1))

    def test_vector(self):
        v1 = Vector(7, 4)
        v2 = Vector(-6, 3)
        self.assertEqual("%s" % v1, "Vector(7.0, 4.0)")
        self.assertEqual("%s" % v2, "Vector(-6.0, 3.0)")
        # length should be sqrt(7**2 + 4**2) = 8.062
        self.assertAlmostEqual(v1.norm(), 8.062, places=3)
        # Create a unit vector and test its length
        v1u = v1.unit_vector()
        self.assertAlmostEqual(v1u.norm(), 1.00, places=3)
        v3 = v1*6.4
        self.assertTrue(isinstance(v3, Vector))
        # v3 length = 8.062(6.4) = 51.597
        self.assertAlmostEqual(v3.norm(), 51.597, places=2)
        # v1 + v2 = (1, 7); length = 7.071
        v4 = v1 + v2
        self.assertAlmostEqual(v4.norm(), 7.071, places=3)
        # Dot product of v1, v2 = (7)(-6) + (4)(3) = -30
        self.assertAlmostEqual(v1.dot(v2), -30.0, places=3)
        self.assertAlmostEqual(v2.dot(v1), -30.0, places=3)
        # Cross product of v1 x v2 = (7)(3) - (-6)(4) = 45
        self.assertAlmostEqual(v1.cross(v2), 45.0, places=3)
        # Cross product of v2 x v1 = (-6)(4) - (7)(3) = -45
        self.assertAlmostEqual(v2.cross(v1), -45.0, places=3)
        v5=v1.perp()
        self.assertAlmostEqual(v5[0], -4.0, places=3)
        self.assertAlmostEqual(v5[1], 7.0, places=3)



if __name__ == "__main__": # pragma: no cover
    unittest.main()
