import math

# D, L, Lr, S, W+, W-, E, H
cases = [
    ("D", "Dead"),
    ("L", "Live"),
    ("Lr", "Roof Live"),
    ("S", "Snow"),
    ("W+", "Wind+"),
    ("W-", "Wind-"),
    ("E", "Earthquake"),
    ("H", "Lateral Pressure"),
]

case_abbrs = [c[0] for c in cases]
case_names = [c[1] for c in cases]

combos = { }
combos["ASD"] = []
combos["LRFD"] = []
_counters = { }

def _add_combo(methodology, factors):
    global _counters
    global combos
    if methodology in list(_counters.keys()):
        _counters[methodology] = _counters[methodology] + 1
    else:
        _counters[methodology] = 0
    name = "%s%d" % (methodology, _counters[methodology])
    eq = ""
    for i in range(0, len(factors)):
        f = factors[i]
        sign = " + "
        c = cases[i][0]
        if f:
            if i == 0:
                sign = ""
            if f != 1 and f != -1:
                eq = eq + "%s%s%s" % (sign, math.fabs(f), c)
            else:
                eq = eq + "%s%s" % (sign, c)
    combos[methodology].append((name, eq, factors))

# Methodology, [D, L, Lr, S, W+, W-, E, H]
_add_combo("ASD", [1, 0, 0, 0, 0, 0, 0, 0])
_add_combo("ASD", [1, 1, 0, 0, 0, 0, 0, 1])
_add_combo("ASD", [1, 0, 1, 0, 0, 0, 0, 1])
_add_combo("ASD", [1, 0, 0, 1, 0, 0, 0, 1])
_add_combo("ASD", [1, 0.75, 0.75, 0, 0, 0, 0, 1])
_add_combo("ASD", [1, 0.75, 0, 0.75, 0, 0, 0, 1])
_add_combo("ASD", [1, 0, 0, 0, 1, 0, 0, 1])
_add_combo("ASD", [1, 0, 0, 0, 0, 1, 0, 1])
_add_combo("ASD", [1, 0, 0, 0, 0, 0, 0.7, 1])
_add_combo("ASD", [1, 0.75, 0, 0, 0.75, 0, 0, 1])
_add_combo("ASD", [1, 0.75, 0, 0, 0, 0.75, 0, 1])
_add_combo("ASD", [1, 0.75, 0, 0, 0, 0, 0.525, 1])
_add_combo("ASD", [1, 0, 0.75, 0, 0.75, 0, 0, 1])
_add_combo("ASD", [1, 0, 0.75, 0, 0, 0.75, 0, 1])
_add_combo("ASD", [1, 0, 0.75, 0, 0, 0, 0.525, 1])
_add_combo("ASD", [0.6, 0, 0, 0, 1, 0, 0, 1])
_add_combo("ASD", [0.6, 0, 0, 0, 0, 1, 0, 1])
_add_combo("ASD", [0.6, 0, 0, 0, 0, 0, 0.7, 1])
_add_combo("LRFD", [1.4, 0, 0, 0, 0, 0, 0, 0])
_add_combo("LRFD", [1.2, 1.6, 0.5, 0, 0, 0, 0, 1.6])
_add_combo("LRFD", [1.2, 1.6, 0, 0.5, 0, 0, 0, 1.6])
_add_combo("LRFD", [1.2, 1, 1.6, 0, 0, 0, 0, 0])
_add_combo("LRFD", [1.2, 1, 0, 1.6, 0, 0, 0, 0])
_add_combo("LRFD", [1.2, 1, 1.6, 0, 0.8, 0, 0, 0])
_add_combo("LRFD", [1.2, 1, 0, 1.6, 0.8, 0, 0, 0])
_add_combo("LRFD", [1.2, 1, 1.6, 0, 0, 0.8, 0, 0])
_add_combo("LRFD", [1.2, 1, 0, 1.6, 0, 0.8, 0, 0])
_add_combo("LRFD", [1.2, 1, 0.5, 0, 1.6, 0, 0, 0])
_add_combo("LRFD", [1.2, 1, 0, 0.5, 1.6, 0, 0, 0])
_add_combo("LRFD", [1.2, 1, 0, 0.2, 0, 0, 1, 0])
_add_combo("LRFD", [0.9, 0, 0, 0, 1.6, 0, 0, 1.6])
_add_combo("LRFD", [0.9, 0, 0, 0, 0, 1.6, 0, 1.6])
_add_combo("LRFD", [0.9, 0, 0, 0, 0, 0, 1, 1.6])

combo_names = { }
for k in list(combos.keys()):
    combo_names[k] = [c[0] for c in combos[k]]

def calc_combos(methodology, vector):
    retval = []
    # Determine if there are any transient loads in the vector, i.e.
    # wind (W+, W-), earthquake (E) or lateral earth pressure (H)
    if len(vector) >= 5:
        max_transient = max(max(vector[4:]), math.fabs(min(vector[4:])))
    else:
        max_transient = 0
    # Cycle through all load combinations
    for c in combos[methodology]:
        # If it is a combo with 0.6D or 0.9D and no transients, set the
        # value equal to D instead of 0.6D or 1.4D instead of 0.9D.  In other
        # words, if no transient load, treat 0.6D + W as D and treat
        # 0.9D + 1.6W as 1.4D.  This is to avoid calculating 0.6D when there
        # are no transient loads.
        if c[2][0] < 1.0 and not max_transient:
            retval.append(retval[0]) # where retval[0] = D for ASD and 1.4D for LRFD
            continue
        resultant = 0.0
        for i in range(0, len(c[2])):
            if i >= len(vector):
                val = 0.0
            else:
                val = float(vector[i])
            fact = float(c[2][i])
            resultant = resultant + val*fact
        retval.append(resultant)
    return retval

if __name__ == '__main__': # pragma: no cover
    # This code is used to generate documentation - do not alter
    # See docs/Makefile
    # See also docs/source/structural/loads.rst
    print("ASD (ALLOWABLE STRESS DESIGN):")
    for c in combos["ASD"]:
        print("%-6s: %s" % (c[0], c[1]))
    print("\nLRFD (LOAD AND RESISTANCE FACTOR DESIGN):")
    for c in combos["LRFD"]:
        print("%-6s: %s" % (c[0], c[1]))

