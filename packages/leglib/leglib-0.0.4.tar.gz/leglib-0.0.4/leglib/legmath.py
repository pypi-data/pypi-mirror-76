"leglib math routines"

from .util import almost_equal
import math

def fabsmax(list_of_values):
    "Returns the maximum absolute value of a list of values."
    abs_values = [math.fabs(i) for i in list_of_values]
    return max(abs_values)


def roundsig(value, digits = 3):
    """Rounds a float value to the specified number of significant digits and
    returns the rounded value"""
    if value:
        order = int(math.floor(math.log10(math.fabs(value))))
        places = digits - order - 1
    else:
        places = 0
    if places > 0:
        return round(value, places)
    else:
        fmtstr = "%.0f"
        return float("%.0f" % (round(value, places)))


if __name__ == "__main__":
    # Test roundsig
    assert(almost_equal(roundsig(114.525, 3), 115.0, 3))
    assert(almost_equal(roundsig(14.525, 3), 14.5, 3))
    assert(almost_equal(roundsig(4.525, 3), 4.53, 3))
    assert(almost_equal(roundsig(-4.525, 3), -4.53, 3))
