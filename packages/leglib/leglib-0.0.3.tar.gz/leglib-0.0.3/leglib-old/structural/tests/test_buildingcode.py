from structural import BuildingCode
from structural import FBC2010
from structural import IBC2009
from structural import NONE
from structural import codes
import structural.asce7_10 as asce7
import unittest


class TestBuildingCode(unittest.TestCase):

    def test_name(self):
        from structural import FBC2010
        self.assertEqual("%s" % FBC2010, "2010 FBC")

    def test_default_codes(self):
        self.assertEqual(FBC2010.asce7.__name__, "structural.asce7_10")
        self.assertEqual(IBC2009.asce7.__name__, "structural.asce7_05")
        self.assertEqual(NONE.asce7.__name__, "structural.asce7_05")
        self.assertEqual(str(FBC2010), "2010 FBC")
        self.assertEqual(str(IBC2009), "2009 IBC")
        self.assertTrue(FBC2010 in codes)
        self.assertTrue(IBC2009 in codes)
        self.assertTrue(NONE in codes)


if __name__ == '__main__': # pragma: no cover
    unittest.main()
