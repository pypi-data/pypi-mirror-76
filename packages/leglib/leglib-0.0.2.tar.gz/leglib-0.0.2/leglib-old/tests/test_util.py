import unittest
import util


class TestUtilities(unittest.TestCase):

    def test_interpolate(self):
        # y = 1.3 + (1.4 - 1.3)/(7.0 - 1.0)*(1.5 - 1.0) = 1.30833
        self.assertAlmostEqual(util.interpolate(1.0, 1.3, 7.0, 1.4, 1.5),
            1.30833, places=3)

    def test_almost_equal(self):
        self.assertFalse(util.almost_equal(5.4432434, 5.4432477, places=5))
        self.assertFalse(util.almost_equal(5.4432434, 5.4432477, places=6))
        self.assertTrue(util.almost_equal(5.4432434, 5.4432477, places=3))
        self.assertTrue(util.almost_equal(5.4432434, 5.4432477, places=4))

    def test_float_eq(self):
        self.assertFalse(util.float_eq(5.4432434, 5.4432477))
        self.assertTrue(util.float_eq(5.4432434, 5.4432477, prec=0.001))
        self.assertTrue(util.float_eq(5.4432434, 5.4432477, prec=1.0E-5))

    def test_float_zero(self):
        self.assertFalse(util.float_zero(0.00003))
        self.assertTrue(util.float_zero(0.00000000003))
        self.assertTrue(util.float_zero(0.00003, prec=0.0001))

    def test_str_to_feet(self):
        self.assertAlmostEqual(util.str_to_feet("-5'-6''"), -5.5, places=3)
        self.assertAlmostEqual(util.str_to_feet("-5'-6\""), -5.5, places=3)
        self.assertAlmostEqual(util.str_to_feet("-5'-7 1/2"), -5.625, places=3)
        self.assertAlmostEqual(util.str_to_feet("-5'-7''"), -5.58333, places=3)
        self.assertAlmostEqual(util.str_to_feet("-5'-7\""), -5.58333, places=3)
        self.assertAlmostEqual(util.str_to_feet("-8 5/8\""), -0.71875, places=3)
        self.assertAlmostEqual(util.str_to_feet("-8"), -0.666667, places=3)
        self.assertAlmostEqual(util.str_to_feet("15'-7''"), 15.58333, places=3)
        self.assertAlmostEqual(util.str_to_feet("15'-7\""), 15.58333, places=3)
        self.assertAlmostEqual(util.str_to_feet("5'-6''"), 5.5, places=3)
        self.assertAlmostEqual(util.str_to_feet("5'-6\""), 5.5, places=3)
        self.assertAlmostEqual(util.str_to_feet("5'-7 1/2"), 5.625, places=3)
        self.assertAlmostEqual(util.str_to_feet("8 5/8''"), 0.71875, places=3)
        self.assertAlmostEqual(util.str_to_feet("8"), 0.666667, places=3)
        self.assertAlmostEqual(util.str_to_feet("8''"), 0.666667, places=3)
        self.assertAlmostEqual(util.str_to_feet("8\""), 0.666667, places=3)

    def test_date_time_functions(self):
        self.assertEqual(len(util.datestamp()), len("2014-03-05"))
        self.assertEqual(len(util.timestamp()), len("2014-03-05 09:15"))

    def test_misc(self):
        self.assertEqual(util.hr(width=10, char='#'), "##########")
        self.assertEqual(util.line(width=11, char='@'), "@@@@@@@@@@@")

if __name__ == "__main__": # pragma: no cover
    unittest.main()
