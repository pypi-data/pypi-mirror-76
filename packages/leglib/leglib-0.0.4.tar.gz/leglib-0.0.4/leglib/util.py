import datetime     # for timestamp function
import math
import re

def almost_equal(first, second, places=7):
    fmtstr = "%%.%df" % places
    return (fmtstr % first) == (fmtstr % second)

def float_eq(float1, float2, prec=1.0E-6):
    "Returns true if float1 and float2 differ by less than 1E-6."
    return (math.fabs(float1 - float2) <= prec)

def float_zero(value, prec=1.0E-6):
    "Returns True if value is very small (default < 1.0E-06)"
    return value <= prec

def str_to_feet(value="0'-0"):
    """
        Returns string converted into decimal feet.

        Acceptible formats include:

        1.  5'-7"
            5'-7 1/2"
            5'-7 1/2''
            5'-7
            5'-7 1/2

        2.  7 3/4
            -8

        The trailing quotation mark can be omitted.
    """
    # Remove optional inches mark
    value = value.replace('"', '')
    value = value.replace("''", "")
    if value.find("'") != -1:
        split_str = value.split("'")
        whole_feet = float(split_str[0])
        in_str = split_str[1]
        if in_str[0] == '-':
            a = len(in_str)
            in_str = in_str[1:a]
    else:
        whole_feet = 0.0
        in_str = value

    split_in_str = in_str.split(" ")
    whole_inches = float(split_in_str[0])
    if len(split_in_str) > 1:
        frac_split = split_in_str[1].split("/")
        numer = float(frac_split[0])
        denom = float(frac_split[1])
        sign = int(whole_inches/math.fabs(whole_inches))
        inches = sign*(math.fabs(whole_inches) + numer/denom)
    else:
        inches = whole_inches

    # Convert the inches portion
    # See if it is decimal form or fraction form"
    if whole_feet < 0:
        sign = -1
    else:
        sign = 1
    return sign*(math.fabs(whole_feet) + inches/12.0)

def hr(width=79, char='='):
    "Returns a horizontal line of characters."
    return line(width, char)

def datestamp():
    "Returns ISO 8601 date stamp."
    t = datetime.datetime.today()
    return t.strftime("%Y-%m-%d")

def timestamp():
    "Returns ISO 8601 date time stamp."
    t = datetime.datetime.today()
    return t.strftime("%Y-%m-%d %H:%M")

def line(width, char='='):
    "Returns a string composed of a number of characters repeated."
    char = char[0]
    retval = ""
    for i in range(0, width):
        retval += char
    return retval

#def adir(obj):
#    "Returns alphabetical dir() results."
#    items = dir(obj)
#    items.sort()
#    return items

#def utc_to_datetime(utc_str):
#    "Parse UTC string into datetime."
#    utc_str = utc_str.lower()
#    utc_re = re.compile("^(?P<dayname>[a-z]{3}), (?P<day>[0-9]{2}) (?P<monthname>[a-z]{3}) (?P<year>[0-9]{4}) (?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2}) (?P<tzoffset>[\+|\-][0-9]{4})")
#    m = utc_re.match(utc_str)
#    month = datetime.datetime.strptime(m.groupdict()["monthname"], "%b").month
#    year = int(m.groupdict()["year"])
#    day = int(m.groupdict()["day"])
#    hour = int(m.groupdict()["hour"])
#    minute = int(m.groupdict()["minute"])
#    second = int(m.groupdict()["second"])
#    return datetime.datetime(year, month, day, hour, minute, second)

def interpolate(x1, y1, x2, y2, x):
    "Returns y for point x given line (x1, y1) - (x2, y2)."
    x = float(x)
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    return (y1 + (y2 - y1)/(x2 - x1)*(x - x1))

#def bilinear_interpolate(x, y, x1, y1, x2, y2, Q11, Q12, Q21, Q22):
#    """Returns R which is interpolated from Q11, Q12, etc. for x, y in a
#    square grid.  See http://en.wikipedia.org/wiki/Bilinear_interpolation"""
#    denom = (x2 - x1)*(y2 - y1)
#    return Q11/denom*(x2 - x)*(y2 - y) + \
#           Q21/denom*(x - x1)*(y2 - y) + \
#           Q12/denom*(x2 - x)*(y - y1) + \
#           Q22/denom*(x - x1)*(y - y1)

#def geocode(address):
#    "Use geopy to return (placename, lat, lon) or None if geocoding fails."
#    from geopy import geocoders
#    try:
#        gn = geocoders.GeoNames()
#        g = geocoders.Google('ABQIAAAAsh_oKO4GhIzRmrsXh68uIxQ8K5bBOqwDHQamL\
#                rpVX5GcdT719xT8C1zgQPQs6LNt2AAksu9_BDy5ZA')
#        place, (lat, lng) = g.geocode(address)
#        return (place, lat, lng)
#    except:
#        # Could not geocode for some reason
#        return None

