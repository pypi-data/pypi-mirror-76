from structural.driftcalc import DriftCalc
from structural.project import Project
import unittest

class TestBasicProject(unittest.TestCase):

    def setUp(self):
        self.p = Project(name="Test Project")

    def test_str_unicode(self):
        # Start without any project number
        self.assertEqual("%s" % self.p, "Test Project")
        self.assertEqual(str(self.p), "Test Project")
        self.assertEqual(str(self.p), "Test Project")
        # Add a project number and re-test
        self.p.number = 889
        self.assertEqual("%s" % self.p, "889 - Test Project")
        self.assertEqual(str(self.p), "889 - Test Project")
        self.assertEqual(str(self.p), "889 - Test Project")

    def test_calc_handling(self):
        d1 = DriftCalc(pg=20.0, lu=100.0, hc=10.0)
        d2 = DriftCalc(pg=20.0, lu=100.0, hc=10.0)
        # Get calc records
        calc1 = self.p.add_calc(d1)
        calc2 = self.p.add_calc(d2)
        self.assertTrue(calc1 is d1)
        self.assertTrue(calc2 is d2)
        self.assertFalse(calc1 is d2)
        self.assertEqual(calc1.name, "DriftCalc1")
        self.assertEqual(calc2.name, "DriftCalc2")
        # Check that 2 variables reference the same object
        self.assertTrue(d1 is self.p.calcs["DriftCalc1"])
        self.assertTrue(d2 is self.p.calcs["DriftCalc2"])
        self.assertFalse(d1 is self.p.calcs["DriftCalc2"])
        # Check that the drift calc is performed; if not pf will not be defined
        self.p.recalc()
        self.assertAlmostEqual(self.p.calcs["DriftCalc1"].drift.pf, 20.0)
        # See that _update_calc set the calc's project to the owner
        self.assertTrue(self.p.calcs["DriftCalc1"].project is self.p)
        # Test single recalc()
        d1.drift.pg = 19.0
        self.assertTrue(self.p.recalc("DriftCalc1"))
        self.assertAlmostEqual(self.p.calcs["DriftCalc1"].drift.pf, 19.0)
        self.assertFalse(self.p.recalc("DriftCalc42"))
        # Test deletion
        self.assertTrue(self.p.del_calc("DriftCalc1"))
        self.assertFalse(self.p.del_calc("DriftCalc42"))
        self.assertFalse("DriftCalc1" in self.p.calcs)
        self.assertTrue("DriftCalc2" in self.p.calcs)

    def test_render(self):
        self.assertTrue(len(self.p.render("txt")) > 0)

class TestProjectCalcOwnership(unittest.TestCase):

    def setUp(self):
        self.p = Project(name="Test Project")
        self.d1 = DriftCalc(pg=20.0, lu=100.0, hc=10.0)
        self.d2 = DriftCalc(pg=20.0, lu=100.0, hc=10.0)
        self.calc1 = self.p.add_calc(self.d1)
        self.calc2 = self.p.add_calc(self.d2)

    def test_add_calc(self):
        self.assertTrue(self.calc1 is self.d1)
        self.assertTrue(self.calc2 is self.d2)
        self.assertFalse(self.calc1 is self.d2)
        self.assertEqual(self.calc1.name, "DriftCalc1")
        self.assertEqual(self.calc2.name, "DriftCalc2")
        self.assertTrue(self.d1 is self.p.calcs["DriftCalc1"])
        self.assertTrue(self.d2 is self.p.calcs["DriftCalc2"])
        self.assertFalse(self.d1 is self.p.calcs["DriftCalc2"])

    def test_recalc(self):
        # Check that 2 variables reference the same object
        # Check that the drift calc is performed; if not pf will not be defined
        self.p.recalc()
        self.assertAlmostEqual(self.p.calcs["DriftCalc1"].drift.pf, 20.0)
        # See that _update_calc set the calc's project to the owner
        self.assertTrue(self.p.calcs["DriftCalc1"].project is self.p)
        # Test single recalc()
        self.d1.drift.pg = 19.0
        self.assertTrue(self.p.recalc("DriftCalc1"))
        self.assertAlmostEqual(self.p.calcs["DriftCalc1"].drift.pf, 19.0)
        self.assertFalse(self.p.recalc("DriftCalc42"))

    def test_full_report(self):
        r = self.p.render("txt")
        # Make sure the 2 calc names appear in the full project report
        self.assertTrue(r.find("DriftCalc1") != -1)
        self.assertTrue(r.find("DriftCalc2") != -1)
        self.assertTrue(r.find(self.p.name) != -1)

    def test_deletion(self):
        self.p.del_calc("DriftCalc1")
        self.assertFalse("DriftCalc1" in self.p.calcs)
        self.assertTrue("DriftCalc2" in self.p.calcs)


if __name__ == '__main__': # pragma: no cover
    unittest.main()

