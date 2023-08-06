"Basic 2D geometry classes and functions"

import math
from util import almost_equal

#try:
#    import pylab
#    have_pylab = True
#except ImportError:
#    have_pylab = False

LEFT = 0
RIGHT = 1
BOTH = 2

def dist(pt1, pt2):
    if not isinstance(pt1, Point): pt1 = Point(pt1[0], pt1[1])
    if not isinstance(pt2, Point): pt2 = Point(pt2[0], pt2[1])
    return pt1.dist(pt2)

class Point:
    "A 2D point."
    def __init__(self, x, y):
        "Can initialize with x, y or a tuple such as (x, y)."
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def from_tuple(self, xy):
        return Point(xy[0], xy[1])

    @classmethod
    def from_point(self, pt):
        return Point(pt.x, pt.y)

    def __repr__(self):
        "Formal string representation."
        return "Point(%s, %s)" % (self.x, self.y)

    def __str__(self):
        "Informal string representation."
        return "(%s, %s)" % (self.x, self.y)

    def __eq__(self, other):
        return almost_equal(self.x, other.x, places=3) and almost_equal(self.y, other.y, places=3)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self, angle, base_pt = None):
        if base_pt is None:
            base_pt = Point(0.0, 0.0)
        x = self.x - base_pt.x
        y = self.y - base_pt.y
        self.x = (math.cos(angle)*x - math.sin(angle)*y) + base_pt.x
        self.y = (math.sin(angle)*x + math.cos(angle)*y) + base_pt.x

    def get_tuple(self):
        "Returns tuple of x,y coordinates."
        return (self.x, self.y)

    def dist(self, other):
        "Returns distance to another point or a line."
        if isinstance(other, Point):
            # Call as tuple instead
            return self.dist((other.x, other.y))

        if isinstance(other, tuple):
            x = other[0]
            y = other[1]
            other = Point(x, y)
            return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

        if isinstance(other, Line):
            # Create a perpendicular line
            return other.dist_to_pt(self)
        else:
            return None

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Point index out of range (0 or 1 only).")

    def copy(self, dir_vec):
        return Point(self.x + dir_vec[0], self.y + dir_vec[1])

class Line:
    "Infinite 2D line passing through two specified points."

    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2

    def _x1(self):
        return self.pt1.x

    def _y1(self):
        return self.pt1.y

    def _x2(self):
        return self.pt2.x

    def _y2(self):
        return self.pt2.y

    x1 = property(_x1)
    x2 = property(_x2)
    y1 = property(_y1)
    y2 = property(_y2)

    def midpoint(self):
        return Point((self.pt1.x + self.pt2.x)/2.,
                     (self.pt1.y + self.pt2.y)/2.)

    def length(self):
        return math.sqrt((self.pt1.x - self.pt2.x)**2 +
                    (self.pt1.y - self.pt2.y)**2)

    def __repr__(self):
        "Formal string representation."
        return "[%s..%s]" % (self.pt1, self.pt2)

    def __str__(self):
        "Informal string representation."
        return "%s-%s" % (self.pt1, self.pt2)

    def is_vertical(self):
        return self.pt1.x == self.pt2.x

    def slope(self):
        if not self.is_vertical():
            return (self.pt2.y - self.pt1.y)/(self.pt2.x - self.pt1.x)
        else:
            return None

    def yintercept(self):
        if not self.is_vertical():
            return self.pt1.y - self.pt1.x * self.slope()
        else:
            return None

    def intersection(self, other):
        P1 = self.pt1
        P2 = self.pt2
        P3 = other.pt1
        P4 = other.pt2

        denom = (P4.y - P3.y)*(P2.x - P1.x) - (P4.x - P3.x)*(P2.y - P1.y)
        if not denom:
            # Lines are parallel or cooincident
            return None

        ua = ((P4.x - P3.x)*(P1.y - P3.y) - (P4.y - P3.y)*(P1.x - P3.x))/denom
        return Point(P1.x + ua*(P2.x - P1.x), P1.y + ua*(P2.y - P1.y))

    def in_bbox(self, point):
        return ((point.x <= self.pt1.x and point.x >= self.pt2.x or
                 point.x <= self.pt2.x and point.x >= self.pt1.x) and
                (point.y <= self.pt1.y and point.y >= self.pt2.y or
                 point.y <= self.pt2.y and point.y >= self.pt1.y))

    def rotate(self, angle, base_pt = None):
        if base_pt is None:
            base_pt = Point(0.0, 0.0)
        self.pt1.rotate(angle, base_pt)
        self.pt2.rotate(angle, base_pt)

    def bearing(self):
        return math.atan2((self.pt2.y - self.pt1.y), (self.pt2.x - self.pt1.x))

    def angle_of_int(self, line):
        "Returns angle of intersection with another line."
        return self.bearing() - line.bearing()

    def offset(self, dist, to_left = True):
        "Offset the line to the left or right."
        brg = self.bearing()
        if to_left:
            off_brg = brg + math.pi/2.0
        else:
            off_brg = brg - math.pi/2.0

        print(("offset bearing =", off_brg))
        self.pt1.x = round(self.pt1.x + dist*math.cos(off_brg), 6)
        self.pt1.y += dist*math.sin(off_brg)
        self.pt2.x = round(self.pt2.x + dist*math.cos(off_brg), 6)
        self.pt2.y += dist*math.sin(off_brg)

    def offset_left(self, dist):
        "Offsets the line to the left."
        self.offset(dist, True)

    def offset_right(self, dist):
        "Offsets the line to the right."
        self.offset(dist, False)

    def dir_vector(self):
        "Returns unity direction vector (x, y) as tuple."
        return (math.cos(self.bearing()), math.sin(self.bearing()))

    def copy(self, d):
        """
            Returns new line:
            dx = d[0], dy = d[1]
        """
        new_pt1 = Point(self.pt1.x + d[0], self.pt1.y + d[1])
        new_pt2 = Point(self.pt2.x + d[0], self.pt2.y + d[1])
        return Line(new_pt1, new_pt2)

    def dist_to_pt(self, point):
        "Returns distance between a point and the line."
        # Calculate u for parametric equation
        if isinstance(point, tuple):
            x3, y3 = point[0], point[1]
        else:
            x3, y3 = point.x, point.y
        x1, y1 = self.pt1.x, self.pt1.y
        x2, y2 = self.pt2.x, self.pt2.y
        u = ((x3 - x1)*(x2 - x1) + (y3 - y1)*(y2 - y1))/(self.length()**2)
        pt = Point(x1 + (x2 - x1)*u, y1 + (y2 - y1)*u)
        return pt.dist(point)


class Ray(Line):
    """A line which starts at a point with given coordinates, and goes off in a
    particular direction to infinity, possibly through a second point."""
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2

    # return the point at which two segments would intersect if they extended
    # far enough to the direction of pt2, not past pt1
    def intersection(self, other):
        P1 = self.pt1
        P2 = self.pt2
        P3 = other.pt1
        P4 = other.pt2
        denom = (P4.y - P3.y)*(P2.x - P1.x) - (P4.x - P3.x)*(P2.y - P1.y)

        if not denom:
            # Lines are parallel or cooincident
            return None

        ua = ((P4.x - P3.x)*(P1.y - P3.y) - (P4.y - P3.y)*(P1.x - P3.x))/denom

        if ua >= 0:
            if isinstance(other, Segment):
                return other.intersection(self)
            else:
                return Point(P1.x + ua*(P2.x - P1.x), P1.y + ua*(P2.y - P1.y))
        else:
            # Intersection is beyond the pt2 of the line segment
            return None

class Segment(Line):
    "Simple 2D line segment."

    def midpoint(self):
        return Point((self.pt1.x + self.pt2.x)/2.,
                     (self.pt1.y + self.pt2.y)/2.)

    def frac_loc(self, fraction):
        return Point((self.pt1.x + (self.pt2.x - self.pt1.x)*fraction),
            (self.pt1.y + (self.pt2.y - self.pt1.y)*fraction))

    def fraction(self, pt_along):
        return float(self.pt1.dist(pt_along))/float(self.length())

    def length(self):
        return self.pt1.dist(self.pt2)

    def lengthen1(self, dist):
        "Move point 1 so that the length increases by dist."
        start_length = self.length()
        goal_length = start_length + dist
        if goal_length > 0.0:
            # Coefficients for parametric equations:
            # x = x1 + a*t
            # y = y1 + b*t
            a = self.pt1.x - self.pt2.x
            b = self.pt1.y - self.pt2.y
            t = goal_length/(math.sqrt(a**2 + b**2))
            self.pt1.x = self.pt2.x + t*a
            self.pt1.y = self.pt2.y + t*b

    def lengthen2(self, dist):
        "Move point 2 so that the length increases by dist."
        start_length = self.length()
        goal_length = start_length + dist
        if goal_length > 0.0:
            # Coefficients for parametric equations:
            # x = x1 + a*t
            # y = y1 + b*t
            a = self.pt2.x - self.pt1.x
            b = self.pt2.y - self.pt1.y
            t = goal_length/(math.sqrt(a**2 + b**2))
            self.pt2.x = self.pt1.x + t*a
            self.pt2.y = self.pt1.y + t*b

    def lengthen(self, dist):
        "Move each endpoint equally so that the length changes by dist."
        start_length = self.length()
        self.lengthen1(dist/2.0)
        self.lengthen2(dist/2.0)
        end_length = self.length()
#        assert((end_length - start_length - dist) <= 0.001)

    def shorten(self, dist):
        "Move each endpoint equally so that the length changes by dist."
        self.lengthen(-dist)

    # return the point at which two segments would intersect if they extended
    # far enough
    def intersection(self, other):
        P1 = self.pt1
        P2 = self.pt2
        P3 = other.pt1
        P4 = other.pt2
        denom = (P4.y - P3.y)*(P2.x - P1.x) - (P4.x - P3.x)*(P2.y - P1.y)

        if not denom:
            # Lines are parallel or cooincident
            return None

        ua = ((P4.x - P3.x)*(P1.y - P3.y) - (P4.y - P3.y)*(P1.x - P3.x))/denom
        if ua >= 0 and ua <= 1:
            if isinstance(other, Segment):
                P1 = other.pt1
                P2 = other.pt2
                P3 = self.pt1
                P4 = self.pt2
                denom = (P4.y - P3.y)*(P2.x - P1.x) - (P4.x - P3.x)*(P2.y - P1.y)
                ua = ((P4.x - P3.x)*(P1.y - P3.y) - (P4.y - P3.y)*(P1.x -\
                        P3.x))/denom
                if ua >= 0 and ua <= 1:
                    return Point(P1.x + ua*(P2.x - P1.x), P1.y +\
                            ua*(P2.y - P1.y))
                else:

                    return None
            else:
                return Point(P1.x + ua*(P2.x - P1.x), P1.y + ua*(P2.y - P1.y))
        else:
            # Intersection is beyond the pt2 of the line segment
            return None

    def clip(self, rect):
        "Returns new segment object which is clipped by specified rectangle."
        assert(isinstance(rect, Rectangle))
        points = rect.intersection(self)
        if len(points) == 0:
            # Check to see if both endpoints are inside
            if rect.inside(self):
                return self
            else:
                return None
        elif len(points) == 2:
            return Segment(points[0], points[1])
        else:
            if rect.inside(self.pt1):
                return Segment(self.pt1, points[0])
            else:
                return Segment(self.pt2, points[0])

    def in_bbox(self, point):
        return ((point.x <= self.pt1.x and point.x >= self.pt2.x or
                 point.x <= self.pt2.x and point.x >= self.pt1.x) and
                (point.y <= self.pt1.y and point.y >= self.pt2.y or
                 point.y <= self.pt2.y and point.y >= self.pt1.y))

    def dist_to_pt(self, point):
        "Returns distance between a point and the line."
        # Calculate u for parametric equation
        if isinstance(point, tuple):
            x3, y3 = point[0], point[1]
        else:
            x3, y3 = point.x, point.y
        x1, y1 = self.pt1.x, self.pt1.y
        x2, y2 = self.pt2.x, self.pt2.y
        if self.length():
            u = ((x3 - x1)*(x2 - x1) + (y3 - y1)*(y2 - y1))/(self.length()**2)
            pt = Point(x1 + (x2 - x1)*u, y1 + (y2 - y1)*u)
        else:
            u = 0
        if u <= 0:
            return self.pt1.dist(point)
        elif u >= 1:
            return self.pt2.dist(point)
        else:
            return pt.dist(point)

class Level:
    "Notional member which defines horizontal (x, y) plane with z coordinate."
    def __init__(self, z):
        self.z = z

class Polygon:
    def __init__(self, points = []):
        assert len(points) >=3, "Not enough points to create polygon (3 required)."
        self.points = points

    def __len__(self):
        "Returns number of points forming polygon."
        return len(self.points)

    def __getitem__(self, i):
        "Used for subscripting, for example: polygon[3]."
        return self.points[i]

    def area(self):
        """
        Returns area of polygon.

        References:
        http://www.efg2.com/Lab/Graphics/PolygonArea.htm
        http://local.wasp.uwa.edu.au/~pbourke/geometry/polyarea/
        """
        retval = 0.0
        n = len(self.points)
        for i in range(0, n-1):
            retval += self.points[i].x*self.points[i + 1].y - self.points[i + 1].x*self.points[i].y
        return retval/2.0

#    def plot(self):
#        "Plots the polygon using pylab."
#        if have_pylab:
#            xvals = []
#            yvals = []
#            for i in range(0, len(self.points)):
#                xvals.append(self.points[i].x)
#                yvals.append(self.points[i].y)
#            xvals.append(self.points[0].x)
#            yvals.append(self.points[0].y)
#            pylab.plot(xvals, yvals, linewidth=4)
#            pylab.show()

    def rotate(self, angle, base_pt = None):
        if base_pt is None:
            base_pt = Point(0.0, 0.0)
        for pt in self.points:
            pt.rotate(angle, base_pt)

    def point_within(self, point):
        """
            Return True if point is contained in polygon (defined by given list of points.)

            Adapted from:
            http://mu.arete.cc/pcr/syntax/pointInPolygon/1/pointInPolygon.py
        """

        # If given values are ints, code will fail subtly. Force them to floats.
        x, y = float(point.x), float(point.y)
        xp = [float(p.x) for p in self.points]
        yp = [float(p.y) for p in self.points]

        # Initialize loop
        c = False
        i = 0
        npol = len(self.points)
        j = npol-1

        while i < npol:
            if ((((yp[i]<=y) and (y<yp[j])) or
                 ((yp[j]<=y) and(y<yp[i]))) and
                (x < (xp[j] - xp[i]) * (y - yp[i]) / (yp[j] - yp[i]) + xp[i])):
                c = not c
            j = i
            i += 1
        return c

    def offset(self, dist = 1.0, outward = True):
        "Offsets polygon points."
        pts = [self.points[len(self.points) - 1]]
        for i in range(0, len(self.points)):
            pts.append(self.points[i])
        pts.append(self.points[0])

        for i in range(0, len(self.points)):
            print(("Point %d = %s" % (i, pts[i + 1])))
            x1, y1 = pts[i + 1].x, pts[i + 1].y
            x2, y2 = pts[i].x, pts[i].y
            x3, y3 = pts[i + 2].x, pts[i + 2].y
            left_ln = Line(Point(x1, y1), Point(x2, y2))
            right_ln = Line(Point(x1, y1), Point(x3, y3))
            print(("\tLeft line before offset: %s" % left_ln))
            print(("\tRight line before offset: %s" % right_ln))
            left_ln.offset_left(1.0)
            print(("\tLeft line after offset: %s" % left_ln))
            print(("\tRight line after offset: %s" % right_ln))
            right_ln.offset_right(1.0)
            print(("\tLeft line after offset: %s" % left_ln))
            print(("\tRight line after offset: %s" % right_ln))
            inter = left_ln.intersection(right_ln)
            self.points[i].x = inter.x
            self.points[i].y = inter.y

    def get_segments(self):
        "Returns a list of all line segments."
        for i in range(0, len(self.points)):
            print(i)

class Rectangle:
    def __init__(self, pt1, pt2):
        p1 = Point(pt1)
        p2 = Point(pt2)
        x1 = min(p1.x, p2.x)
        y1 = min(p1.y, p2.y)
        x2 = max(p1.x, p2.x)
        y2 = max(p1.y, p2.y)
        top = Segment((x1, y1), (x2, y1))
        bot = Segment((x1, y2), (x2, y2))
        left = Segment((x1, y1), (x1, y2))
        right = Segment((x2, y1), (x2, y2))
        self.sides = (top, bot, left, right)

    def intersection(self, other):
        "Returns a list of intersection points."
        ints = []
        if isinstance(other, Line) or isinstance(other, Segment):
            for side in self.sides:
                i = side.intersection(other)
                if i is not None:
                    ints.append(i)
        return ints

    def inside(self, other):
        if isinstance(other, Point):
            x = [side.pt1.x for side in self.sides]
            x.extend([side.pt2.x for side in self.sides])
            y = [side.pt1.y for side in self.sides]
            y.extend([side.pt2.y for side in self.sides])
            return (other.x >= min(x)) and (other.x <= max(x)) and\
                   (other.y >= min(y)) and (other.x <= max(y))
        elif isinstance(other, Segment):
            return self.inside(other.pt1) and self.inside(other.pt2)
        else:
            return False



##class Rectangle(Polygon):
##    def __init__(self, lower_left, upper_right):
##        pts = []
##        pts.append(Point(lower_left[0], lower_left[1]))
##        pts.append(Point(upper_right[0], lower_left[1]))
##        pts.append(Point(upper_right[0], upper_right[1]))
##        pts.append(Point(lower_left[0], upper_right[1]))
##        Polygon.__init__(self, pts)
##
##    def width(self):
##        return self.points[1].x - self.points[0].x
##
##    def height(self):
##        return self.points[2].y - self.points[0].y

class Vector:
    "General 2-dimensional vector."
    def __init__(self, x = 1, y = 0):
        self.x = float(x)
        self.y = float(y)

    def __unicode__(self):
        return "Vector(%s, %s)" % (self.x, self.y)

    def __str__(self):
        return self.__unicode__()

    def norm(self):
        "Returns the length of the vector."
        return math.sqrt(self.x**2 + self.y**2)

    def unit_vector(self):
        "Returns a unit vector in the same direction."
        vhat = Vector()
        vhat.x = self.x/self.norm()
        vhat.y = self.y/self.norm()
        return vhat

    def __getitem__(self, i):
        return (self.x, self.y)[i]

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Vector addition requires vector addend.")

    def __mul__(self, other):
        "Vector to scalar multiplication."
        return Vector(self.x*float(other), self.y*float(other))

    def dot(self, other):
        "Vector dot product."
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("Vector dot product requires vector argument.")

    def cross(self, other):
        "Vector cross product."
        if isinstance(other, Vector):
            return (self.x * other.y) - (self.y * other.x)
        else:
            raise TypeError("Vector dot product requires vector argument.")

    def perp(self):
        "Returns perpendicular vector."
        return Vector(-self.y, self.x)


