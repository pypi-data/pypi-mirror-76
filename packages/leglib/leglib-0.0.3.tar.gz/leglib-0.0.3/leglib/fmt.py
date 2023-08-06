"""
Formatting functions used to format various numerical and physical
quantities as strings.
"""
from leglib.util import almost_equal
import math

INCHES_PER_METER = 39.3701

#==============================================================================
# General number formatting
#==============================================================================
def integer(value):
    "Returns float value formated to digits decimal places."
    return "%d" % (value)


def fixed(value, digits=2):
    "Returns float value formated to digits decimal places."
    fmtstr = "%%.%df" % digits
    return fmtstr % (value)

def sigdig(value, digits=3):
    "Returns float value formatted with digits significant digits."
    if value:
        order = int(math.floor(math.log10(math.fabs(value))))
        places = digits - order - 1
    else:
        places = 2
    if places > 0:
        fmtstr = "%%.%df" % (places)
    else:
        fmtstr = "%.0f"
    try:
        retval = fmtstr % (round(value, places))
    except:
        retval = "ERROR: fmt.fixed() value not found"
    return retval


def money(num):
    "Returns a number formatted as dollars.  Negative formatted as -$#.##"
    if num < 0:
        return "-$%0.2f" % math.fabs(num)
    else:
        return "$%0.2f" % num


#==============================================================================
# Force, pivot unit = kips
#==============================================================================
def lbs(kips):
    "Formats kips as pounds "
    return "%s lbs"% (sigdig(kips*1000.0))

def kN(kips):
    "Formats kips as kilonewtons "
    return "%s kN"% (sigdig(float(kips)*4.4482))

def kips(val):
    "Format kips as kips "
    return "%s kips" % (sigdig(val))

#==============================================================================
# Length, pivot unit = inches
#==============================================================================
def ft(inches):
    "Formats inches as feet "
    return "%s ft"% (sigdig(inches/12.0))

def ft_in(inches_in, denom=16):
    "Formats inches as feet and inches"
    if inches_in < 0:
        return "-%s" % (ft_in(math.fabs(inches_in), denom))
    else:
        feet = math.floor(inches_in/12.0)
        if feet > 0:
            str_feet = "%d\'-"% feet
        else:
            return inches(inches_in, denom)
        return "%s%s"% (str_feet, inches(inches_in - feet*12.0, denom))

def inches(inches_in, denom=16):
    "Formats inches as inches"
    if not type(inches_in) == float:
        raise Exception("%s is not a float" % inches_in)

    if inches_in < 0:
        return "-%s" % (inches(math.fabs(inches_in)))
    else:
        return "%s\"" % frac(inches_in, denom)

def inches_decimal(inches_in):
    "Formats inches as decimal inches up to 4 decimal places"
    if "%d" % inches_in == "%s" % inches_in:
        return "%d" % inches_in
    else:
        return "%.3d" % inches_in

def m(inches_in, digits=3):
    "Formats inches as meters"
    return "%s m" % (sigdig(inches_in/INCHES_PER_METER, digits))

def mm(inches_in, digits=3):
    "Formats inches as millimeters"
    return "%s mm" % (sigdig(inches_in/INCHES_PER_METER*1000.0, digits))

#==============================================================================
# Moment, pivot unit = kip-in
#==============================================================================
def kip_in(kip_inches):
    "Formats pivot unit of kip-inches"
    return "%s kip-in"% (sigdig(kip_inches))

def lb_ft(kip_in):
    "Formats kip-inches as lb-ft "
    return "%s lb-ft"% (sigdig(1000.0*kip_in/12.0))

def kip_ft(kip_in):
    "Formats kip-inches as kip-ft "
    return "%s kip-ft"% (sigdig(kip_in/12.0))

def kN_m(kip_in):
    "Formats kilonewton-meters as kip-ft "
    return "%s kN-m"% (sigdig(kip_in*0.11298))

#==============================================================================
# Pressure, pivot unit = kips per square inch (ksi)
#==============================================================================
def psi(ksi):
    "Formats ksi as psi "
    return "%s psi"% (sigdig(ksi*1000.0, 3))

def ksi(ksi):
    "Formats ksi as ksi "
    return "%s ksi"% (sigdig(ksi, 3))

def psf(ksi):
    "Formats ksi as psf "
    return "%s psf"% (sigdig(ksi*144.0*1000.0, 3))

def ksf(ksi):
    "Formats ksi as ksf "
    return "%s ksf"% (sigdig(ksi*144.0, 3))

def kPa(ksi):
    "Formats ksi as kilopascals "
    return "%s kPa"% (sigdig(ksi*6894.8))

#==============================================================================
# Line loads, pivot unit = kips per foot (k/ft)
#==============================================================================
def plf(kips_per_ft):
    " Formats kips per inch as pounds per foot "
    return "%s plf" % (sigdig(kips_per_ft*1000.0))

def klf(kips_per_ft):
    " Formats kips per inch as kips per foot "
    return "%s k/ft" % (sigdig(kips_per_ft*12.0))

#==============================================================================
# Unity value = demand/capacity ratio
#==============================================================================
def unity(U):
    "Formats unity value as 2-digit number with OK or NG suffix"
    if U <= 1.0:
        msg = "PASS"
    elif U <= 1.03:
        msg = "SAY OK"
    else:
        msg = "FAIL"
    return "%.2f %s" % (U, msg)

#==============================================================================
# Fractions
#==============================================================================
def frac(val, denom = 64):
    "Formats a floating point number as a fraction"
    if val < 0:
        return "-%s" % (frac(math.fabs(val), denom))
    else:
        whole = math.floor(val)
        dec = val - whole
        numer = 0
        if dec:
            numer = round(dec*denom)
            while not (numer % 2) and numer:
                numer = numer/2
                denom = denom/2
#            if denom == 1:
#                whole += 1
#                numer = 0
        if almost_equal(numer, denom):
            numer = 0
            whole = whole + 1
        if whole and numer:
            return "%d %d/%d"% (whole, numer, denom)
        elif numer:
            return "%d/%d"% (numer, denom)
        else:
            return "%d"% (whole)


class SigdigFloat(float):
    "Used in place of a float for string formatting only.  Prints in significant digits format."
    def __init__(self, value, digits=3):
        self.value = value
        self.digits = digits

    def __str__(self):
        return sigdig(self.value, self.digits)