"""
    LaTeX helper functions, including formatting.
    2007-08-01  JML
"""
import locale
import math

DIGITS = 3

def verify_locale():
    loc = locale.getlocale(locale.LC_MONETARY)
    if loc[0] is None:
        locale.setlocale(locale.LC_ALL, 'En')
    "Sets default locale if none has been specified."

#==============================================================================
# General number formatting
#==============================================================================
def sig(num, digits = DIGITS):
    """
        Formats a number with specified number of significant digits (defaults
        to 3 significant digits.
    """
    assert(digits >= 1)
    if not isinstance(num, float):
        raise TypeError("Significant digits only apply to float values.")

    if num:
        # Order of magnitude
        order = int(math.floor(math.log10(math.fabs(num))))
    else:
        order = 0
    round_digits = digits - order - 1
    verify_locale()
    if round_digits > 0:
        fmt = "%%0.%df"% round_digits
        return locale.format(fmt, (round(num, round_digits)), grouping = True)
##        return ("%%0.%df"% (round_digits)) % (round(num, round_digits))
##        return ("%%0.%df"% (round_digits)) % (round(num, round_digits))
    else:
        return locale.format("%d", (int(round(num, round_digits))), grouping = True)
##        return "%d"% (int(round(num, round_digits)))

def money(num):
    "Returns a number formatted as currency using current locale."
    verify_locale()
    conv = locale.localeconv()
    return locale.format("%s%.*f", (conv['currency_symbol'],conv['int_frac_digits'], num), grouping=True)


#==============================================================================
# Force, pivot unit = kips
#==============================================================================
def lb(kips):
    "Formats kips as pounds "
    return "%.0f lbs"% (kips*1000.0)

def kN(kips):
    "Formats kips as kilonewtons "
    return "%.0f kN"% (kips*4.4482)

def kips(kips_in, digits = 2):
    "Format kips as kips "
    fmtstring = "%%.%df kips" % int(digits)
    return fmtstring % (kips_in)

#==============================================================================
# Length, pivot unit = inches
#==============================================================================
def ft(inches):
    "Formats inches as feet "
    return "%.2f ft"% (inches/12.0)

def m(inches):
    "Formats inches as meters "
    return "%.2f m"% (inches*0.0254)

def ft_in(inches_in, denom = 64):
    "Formats inches as feet and inches"
    feet = math.floor(inches_in/12.0)
    if feet:
        str_feet = "%d\'-"% feet
    else:
        str_feet = ""
    return "%s%s"% (str_feet, inches(inches_in - feet*12.0, denom))

def inches(inches_in, denom = 64):
    "Formats inches as inches"
    assert type(inches_in) == float
    return "%s''" % frac(inches_in, denom)

#==============================================================================
# Moment, pivot unit = kip-in
#==============================================================================
def kip_in(kip_inches):
    "Formats pivot unit of kip-inches"
    return "%.0f kip-in"% (kip_inches)

def lb_ft(kip_in):
    "Formats kip-inches as lb-ft "
    return "%.0f lb-ft"% (1000.0*kip_in/12.0)

def kip_ft(kip_in):
    "Formats kip-inches as kip-ft "
    return "%.1f kip-ft"% (kip_in/12.0)

def kN_m(kip_in):
    "Formats kilonewton-meters as kip-ft "
    return "%.1f kN-m"% (kip_in*0.11298)

#==============================================================================
# Pressure, pivot unit = kips per square inch (ksi)
#==============================================================================
def psi(ksi):
    "Formats ksi as psi "
    return "%s psi"% (sig(ksi*1000.0, 3))

def ksi(ksi):
    "Formats ksi as ksi "
    return "%s ksi"% (sig(ksi, 3))

def psf(ksi):
    "Formats ksi as psf "
    return "%s psf"% (sig(ksi*144.0*1000.0, 3))

def ksf(ksi):
    "Formats ksi as ksf "
    return "%s ksf"% (sig(ksi*144.0, 3))

def kPa(ksi):
    "Formats ksi as kilopascals "
    return "%.1f kPa"% (ksi*6894.8)

#==============================================================================
# Line loads, pivot unit = kips per inch (k/in)
#==============================================================================
def plf(kip_per_in):
    " Formats kips per inch as pounds per foot "
    return "%.0f plf" % (kip_per_in*12000.0)

def klf(kip_per_in):
    " Formats kips per inch as kips per foot "
    return "%.0f klf" % (kip_per_in*12.0)

def unity(U):
    "Formats unity value as 2-digit number with OK or NG suffix"
    if U <= 1.0:
        msg = "OK"
    elif U <= 1.03:
        msg = "SAY OK"
    else:
        msg = "\\\\textbf{NO GOOD}"
    return "\\\\uuline{%s} (%.2f)" % (msg, U)

def frac(val, denom = 64):
    "Formats a floating point number as a fraction"
    whole = math.floor(val)
    dec = val - whole
    numer = 0
    if dec:
        numer = round(dec*denom)
        while not (numer % 2) and numer:
            numer = numer/2
            denom = denom/2
        if denom == 1:
            whole += 1
            numer = 0
    if whole and numer:
        return "%d %d/%d"% (whole, numer, denom)
    elif numer:
        return "%d/%d"% (numer, denom)
    else:
        return "%d"% (whole)


#==============================================================================
# Module testing
#==============================================================================
if __name__ == '__main__':
    # Test
    a = 5.57437
    print(sig(a))
    print(sig(a, 10))
    b = 453278943.4327819432
    print(sig(b, 4))
    fb = 14.532
    print(psi(fb))
    print(psf(fb))
    print(ksf(fb))
    print(ksi(fb))
    print(money(b))
    print(frac(0.375))
    print(inches(0.3125))
