"Jinja2 template filters.  See http://jinja.pocoo.org/docs/api/#writing-filters"

# If you add a new filter, add it to the list of imports in structural/report.py
# Also add it to Jinja in the body of Report.render()

import fmt

def _is_metric(member):
    retval = False
    if member is not None and hasattr(member, "project"):
        retval = member.project.is_metric
    if hasattr(member, "is_metric"):
        retval = member.is_metric
    return retval


def dim(value, member=None):
    if _is_metric(member):
        # Return millimeters
        return fmt.mm(value)
    else:
        # Return feet/inches
        return fmt.inches(value)


def distance(value, member=None):
    if _is_metric(member):
        # Return meters
        return fmt.m(value)
    else:
        # Return decimal feet
        return fmt.ft(value)


def distance_from_ft(value, member=None):
    return distance(value*12.0, member)


def fixed(value, digits=2):
    return fmt.fixed(value, digits)


def ft_in(value, denom=16):
    return fmt.ft_in(value, denom=denom)


def ft_in_from_ft(value, denom=16):
    return fmt.ft_in(12.0*value, denom=denom)


def length(value, member=None):
    if _is_metric(member):
        # Return meters
        return fmt.m(value)
    else:
        # Return feet/inches
        return fmt.ft_in(value)


def mult(value, factor):
    return value*factor


def sigdig(value, digits=3):
    return fmt.sigdig(value, digits=digits)


def check(value):
    if value <= 1.03:
        pass_fail = "PASS"
    else:
        pass_fail = "FAIL"
    return "%.2f (%s)" % (value, pass_fail)


def equation(text, namespace):
    """Substitues values from namespace in equation text:
       Given:
           M = wL^2/8
           namespace.M = 20.25
           namespace.w = 0.50
           namespace.L = 18.0
       Filter output:
           M = wL^2/8 = (0.500)(18.0)^2/8 = 20.25

       If a variable is surrounded by parentheses like (A), the extra
       parentheses will be removed:

       (A)(B) = C becomes (1.00)(2.00) = 2.00, not ((1.00))((2.00)) = 2.00
       """
    left, right = text.split('=')
    left = left.strip()
    right = right.strip()

    keys = [k for k in list(namespace.__dict__.keys())]

    keys.sort(key=len, reverse=True)

    for i in keys:
        # Prepare it so (A)(B) = C does not become ((1.00))((2.00)) = 2.00
        right = right.replace("(%s)" % i, "%s" % i)
        right = right.replace(i, "(%s)" % sigdig(getattr(namespace, i)))
    for i in namespace.__dict__:
        left = left.replace(i, "%s" % sigdig(getattr(namespace, i)))
    return " = ".join([text, right, left])
