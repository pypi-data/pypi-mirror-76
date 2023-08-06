# Validation functions for strings
import re

# =============================================================================
# Floating-point values
# =============================================================================
def unsigned_float(txt):
    "Returns true if string is a signed or unsigned decimal."
    print("Validating string %s" % txt)
    return (re.compile(r"^\d*\.?\d*$").search(txt) is not None)

def signed_float(txt):
    "Returns true if string is a signed or unsigned decimal."
    return (re.compile(r"^(\+|-)?\d*\.?\d*$").search(txt) is not None)

# =============================================================================
# Integers
# =============================================================================
def signed_int(txt):
    "Returns true if string is a signed or unsigned integer or empty string."
    if type(txt) == int: return True
    if type(txt) == str:
        return (re.compile(r"^(\+|-)?\d*$").search(txt) is not None)
    else:
        return False

def unsigned_int(txt):
    "Returns true if string is an unsigned integer."
    if type(txt) == int:
        return (txt >= 0)
    if type(txt) == str:
        return (re.compile(r"^\d+$").search(txt) is not None)
    else:
        return False

def even_int(val):
    "Returns true if string is an even integer."
    if isinstance(val, str):
        if not unsigned_int(val):
            # It is not even an integer, so return false
            return False
        val = int(val)
    elif not isinstance(val, int):
        # Not a string representation of an int or an int itself
        return False
    # We know it is an integer, so check if it is even or not
    return not(val%2)

if __name__ == "__main__":
    print("Testing validation functions.")
    assert not signed_int("-4.11")      # False
    assert signed_int("-4")             # True
    assert not unsigned_int("-4")       # False
    assert unsigned_int("4")            # True
    assert not unsigned_int("Joe")      # False
    assert not unsigned_float("-4.22")  # True
    assert signed_float("4.22")         # True
    assert not unsigned_float("Joe")    # False
    assert not signed_float("Joe")      # False
    assert even_int("24")               # True
    assert not even_int("3")            # True
    assert not even_int(31)             # False
    assert not even_int(1.7)            # False
    print("Done. No failures.")
