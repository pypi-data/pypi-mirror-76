# Functions to assist in command-line input
from . import validate

# =============================================================================
# Integers
# =============================================================================
def signed_int(prompt = "Enter a signed integer: "):
    "Keeps prompting user for an signed integer until they do."
    valid = False
    while not valid:
        txt = input(prompt).strip()
        valid = validate.signed_int(txt)
        if not valid:
            print("Value must be an integer.")
    if len(txt):
        return int(txt)
    else:
        return None

def unsigned_int(prompt = "Enter an unsigned integer: "):
    "Keeps prompting user for an unsigned integer until they do."
    valid = False
    while not valid:
        txt = input(prompt).strip()
        valid = validate.unsigned_int(txt)
        if not valid:
            print("Value must be an unsigned integer.")
    if len(txt):
        return int(txt)
    else:
        return None

# =============================================================================
# Floating-point numbers
# =============================================================================
def signed_float(prompt = "Enter a signed decimal number: "):
    "Keeps prompting user for an signed float until they do."
    valid = False
    while not valid:
        txt = input(prompt).strip()
        valid = validate.signed_float(txt)
        if not valid:
            print("Value must be a decimal number.")
    if len(txt):
        return float(txt)
    else:
        return None

def unsigned_float(prompt = "Enter an unsigned decimal number: "):
    "Keeps prompting user for an unsigned float until they do."
    valid = False
    while not valid:
        txt = input(prompt).strip()
        valid = validate.unsigned_float(txt)
        if not valid:
            print("Value must be an unsigned decimal number.")
    if len(txt):
        return float(txt)
    else:
        return None

# =============================================================================
# Yes or No
# =============================================================================
def yes(prompt = "Enter y or n: "):
    """Prompt user for a y or n entry, non-case sensitive. Returns True if
    user says 'y'"""
    valid = False
    while not valid:
        txt = input(prompt)
        if len(txt) >= 1:
            c = txt.lower().strip()
            valid = c in ("y", "n")
    return (c == 'y')

if __name__ == "__main__":
    n = signed_int("Enter a number: ")
