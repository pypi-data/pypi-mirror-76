from structural.project import Project
from structural.report import Report
import filters as f
import unittest


class TestFilters(unittest.TestCase):

    def setUp(self):
        self.L = 87.55          # length in inches
        self.Lfeet = 7.29583    # length in feet
        self.tf = 0.554         # flange thickness in inches

    def test_imperial_filters(self):
        r = Report(self)
        # It should return a unicode string
        self.assertEqual(type(r.render("txt")), type("Joe"))
        # The string should not be empty
        self.assertGreater(len(r.render("txt")), 0)
        # Test various filters
        self.assertEqual(f.dim(self.tf), "9/16\"")
        self.assertEqual(f.dim(self.tf, self), "9/16\"")
        self.assertEqual(f.fixed(self.L, digits=3), "87.550")
        self.assertEqual(f.fixed(self.tf), "0.55")
        self.assertEqual(f.ft_in(self.L), "7'-3 9/16\"")
        self.assertEqual(f.ft_in_from_ft(self.Lfeet), "7'-3 9/16\"")
        self.assertEqual(f.ft_in_from_ft(10.3333), "10'-4\"")
        self.assertEqual(f.length(self.L), "7'-3 9/16\"")
        self.assertEqual(f.length(self.L, self), "7'-3 9/16\"")
        self.assertEqual(f.sigdig(self.L, 2), "88")
        self.assertEqual(f.sigdig(self.L, 3), "87.5")
        self.assertEqual(f.sigdig(self.tf, 2), "0.55")

    def test_metric_filters(self):
        self.project = Project(is_metric = True)
        r = Report(self)
        # It should return a unicode string
        self.assertEqual(type(r.render("txt")), type("Joe"))
        # The string should not be empty
        self.assertGreater(len(r.render("txt")), 0)
        # Test various filters that are affected by is_metric
        # If not passed a member (self here), default to is_metric = False
        self.assertEqual(f.dim(self.L, self), "2220 mm")
        self.assertEqual(f.dim(self.tf), "9/16\"")
        self.assertEqual(f.dim(self.tf, self), "14.1 mm")
        self.assertEqual(f.length(self.L), "7'-3 9/16\"")
        self.assertEqual(f.length(self.L, self), "2.22 m")

    def test_member_is_metric(self):
        self.project = Project(is_metric = False)
        self.is_metric = True   # should behave as if project.is_metric = True
        self.assertEqual(f.dim(self.L, self), "2220 mm")
        self.assertEqual(f.dim(self.tf), "9/16\"")
        self.assertEqual(f.dim(self.tf, self), "14.1 mm")
        self.assertEqual(f.length(self.L), "7'-3 9/16\"")
        self.assertEqual(f.length(self.L, self), "2.22 m")


if __name__ == '__main__': # pragma: no cover
    unittest.main()
