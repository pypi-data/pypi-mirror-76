from structural.footing import FootingPierAssembly
from structural.report import Report
from structural.soil import Soil
from structural.tests.test_driftcalc import TestDriftCalc
import unittest


class TestReport(unittest.TestCase):

    def test_txt_report(self):
        m = FootingPierAssembly(B=5.0, L=5.0, T=1.5, Lp=2.0, Bp=2.0, Hp=3.0,
                gamma_c=0.145, soil=Soil(gamma_s=0.090))
        r = Report(m)
        # It should return a unicode string
        self.assertEqual(type(r.render("txt")), type("Joe"))
        # The string should not be empty
        self.assertGreater(len(r.render("txt")), 0)

class TestDriftCalcReport(TestDriftCalc):

    def test_driftcalc_report(self):
        r = Report(self.calc)
        self.assertEqual(type(r.render("txt")), type("Joe"))
        self.assertGreater(len(r.render("txt")), 0)

if __name__ == '__main__': # pragma: no cover
    unittest.main()
