import fmt
import unittest


class TestFormatting(unittest.TestCase):

    def test_sigdig(self):
        self.assertEqual(fmt.sigdig(-3.14159), "-3.14")
        self.assertEqual(fmt.sigdig(-3.14159, 3), "-3.14")
        self.assertEqual(fmt.sigdig(-3.14159, 4), "-3.142")
        self.assertEqual(fmt.sigdig(0), "0.00")
        self.assertEqual(fmt.sigdig(123), "123")
        self.assertEqual(fmt.sigdig(3.14159), "3.14")
        self.assertEqual(fmt.sigdig(3.14159, 3), "3.14")
        self.assertEqual(fmt.sigdig(3.14159, 4), "3.142")
        self.assertEqual(fmt.sigdig(4), "4.00")
        self.assertRaises(TypeError, fmt.sigdig, ("8675309"))
        self.assertRaises(TypeError, fmt.sigdig, (4, "Abc"))

    def test_money(self):
        self.assertEqual(fmt.money(4.75), "$4.75")
        self.assertEqual(fmt.money(0.75), "$0.75")
        self.assertEqual(fmt.money(-1.75), "-$1.75")
        self.assertEqual(fmt.money(-0.75), "-$0.75")

    def test_force_formats(self):
        self.assertEqual(fmt.lbs(3.221), "3220 lbs")
        self.assertEqual(fmt.kN(3.221), "14.3 kN")
        self.assertEqual(fmt.kips(3.221), "3.22 kips")

    def test_length_formats(self):
        self.assertEqual(fmt.ft(-7), "-0.583 ft")
        self.assertEqual(fmt.ft(-87), "-7.25 ft")
        self.assertEqual(fmt.ft(7), "0.583 ft")
        self.assertEqual(fmt.ft(87), "7.25 ft")
        self.assertEqual(fmt.ft_in(-87.888), "-7'-3 7/8\"")
        self.assertEqual(fmt.ft_in(-9.125), "-9 1/8\"")
        self.assertEqual(fmt.ft_in(165), "13'-9\"")
        self.assertEqual(fmt.ft_in(7.25), "7 1/4\"")
        self.assertEqual(fmt.ft_in(87.888), "7'-3 7/8\"")
        self.assertEqual(fmt.inches(-87.375, denom=32), "-87 3/8\"")
        self.assertEqual(fmt.inches(87.0938, denom=32), "87 3/32\"")
        self.assertEqual(fmt.m(-7), "-0.178 m")
        self.assertEqual(fmt.m(-87.375, digits=4), "-2.219 m")
        self.assertEqual(fmt.m(165), "4.19 m")
        self.assertEqual(fmt.m(7), "0.178 m")
        self.assertEqual(fmt.mm(-7), "-178 mm")
        self.assertEqual(fmt.mm(-87.375, digits=4), "-2219 mm")
        self.assertEqual(fmt.mm(165), "4190 mm")
        self.assertEqual(fmt.mm(165, digits=4), "4191 mm")
        self.assertEqual(fmt.mm(7), "178 mm")

    def test_moment_formats(self):
        self.assertEqual(fmt.kip_in(87.3234), "87.3 kip-in")
        self.assertEqual(fmt.lb_ft(87.3234), "7280 lb-ft")
        self.assertEqual(fmt.kip_ft(-187.3234), "-15.6 kip-ft")
        self.assertEqual(fmt.kN_m(-187.3234), "-21.2 kN-m")

    def test_pressure_formats(self):
        self.assertEqual(fmt.psi(123.434), "123000 psi")
        self.assertEqual(fmt.psi(-1123.434), "-1120000 psi")
        self.assertEqual(fmt.ksi(23.434), "23.4 ksi")
        self.assertEqual(fmt.ksi(-123.434), "-123 ksi")
        self.assertEqual(fmt.psf(5.343), "769000 psf")
        self.assertEqual(fmt.ksf(5.343), "769 ksf")
        self.assertEqual(fmt.kPa(5.343), "36800 kPa")

    def test_line_load_formats(self):
        self.assertEqual(fmt.plf(0.3432), "343 plf")
        self.assertEqual(fmt.klf(0.3432), "4.12 k/ft")

    def test_unity(self):
        self.assertEqual(fmt.unity(0.3432), "0.34 PASS")
        self.assertEqual(fmt.unity(1.3432), "1.34 FAIL")
        self.assertEqual(fmt.unity(1.027), "1.03 SAY OK")

    def test_fraction_format(self):
        self.assertEqual(fmt.frac(0.360, denom=16), "3/8")
        self.assertEqual(fmt.frac(-0.406, denom=32), "-13/32")
        self.assertEqual(fmt.frac(17.0002, denom=32), "17")


if __name__ == "__main__": # pragma: no cover
    unittest.main()
