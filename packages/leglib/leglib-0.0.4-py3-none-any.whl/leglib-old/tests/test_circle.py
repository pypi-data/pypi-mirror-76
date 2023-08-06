#!/usr/bin/env python3
import unittest
import math

from leglib.shapes import Circle

DIAMETER = 16.0


class TestCircle(unittest.TestCase):

    def setUp(self):
        self.circ = Circle(d=DIAMETER)

    def test_area(self):
        self.assertAlmostEqual(self.circ.A(), math.pi *
                               DIAMETER*DIAMETER/4.0, places=3)

    def test_half_circle_area(self):
        "Test to see if we get half the circle area when we plug in y=0.0"
        self.assertAlmostEqual(self.circ.segment_area(y=0.0), math.pi *
                               DIAMETER*DIAMETER/4.0/2.0, places=3)

    def test_circular_segment_area(self):
        # Magic number value was calculated using an online calculator
        # https://rechneronline.de/pi/circular-segment.php
        self.assertAlmostEqual(self.circ.segment_area(y=6.0), 14.506, places=3)

    def test_circular_segment_moment_area(self):
        # Use a half-circle to test this function
        # https://en.wikipedia.org/wiki/List_of_centroids
        r = self.circ.R()
        A = math.pi*r**2/2.0
        y_bar = 4.0*r/(3.0*math.pi)
        self.assertAlmostEqual(
            self.circ.first_moment_segment_area(y=0.0), A*y_bar, 4)


    def test_stress_block_area(self):
        r = self.circ.R()
        self.assertAlmostEqual(
            self.circ.stress_block_area(c=8, beta1=1.0), math.pi*r**2/2.0, 4)
        self.assertAlmostEqual(
            # Test result from calculator at https://planetcalc.com/1421/
            self.circ.stress_block_area(c=4, beta1=1.0), 39.31, 2)



if __name__ == '__main__':
    unittest.main()
