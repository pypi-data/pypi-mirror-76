from structural.conccol import RectTiedColumn
import unittest

class TestRectTiedColumn(unittest.TestCase):

    def setUp(self):
        self.col = RectTiedColumn(b=12.0, h=24.0, nx=2, ny=5,
               barsize=14, tiebarsize=4, fc=6000, cover=1.5)

    def test_props(self):
        self.assertEqual(self.col.n(), 10)
        self.assertAlmostEqual(self.col.Ag(), 288.0, places=2)
        self.assertAlmostEqual(self.col.Ast(), 22.50, places=2)
        self.assertAlmostEqual(self.col.sx(), 6.307, places=3)
        self.assertAlmostEqual(self.col.sy(), 4.5768, places=3)
        self.assertAlmostEqual(self.col.concrete().beta1(), 0.75, places=2)

    def test_Pn(self):
        self.assertAlmostEqual(self.col.Pn_max(), 2163.24, places=2)
        self.assertAlmostEqual(self.col.phiPn_max(), 1406.0, places=0)

    def test_ds(self):
        rows = self.col.rows_y()
        self.assertAlmostEqual(rows[0].ds, 2.8465, places=3)
        self.assertAlmostEqual(rows[1].ds, 7.423, places=3)
        self.assertAlmostEqual(rows[2].ds, 12.0, places=3)
        self.assertAlmostEqual(rows[3].ds, 16.577, places=3)
        self.assertAlmostEqual(rows[4].ds, 21.153, places=3)
        self.assertAlmostEqual(sum([r.Ast() for r in rows]), self.col.Ast())

#    def test_calcs(self):
#        self.assertAlmostEqual(self.col.case_1(), 27.3088, places=2)


if __name__ == '__main__': # pragma: no cover
    unittest.main()
