class Prop(dict):
    def __init__(self, desc, name, val, units = ""):
        self["desc"] = desc
        self["name"] = name
        self["val"] = val
        self["units"] = units

class FloatDict(dict):
    "A dictionary containing float values suitable for mathematical operators."
    def __init__(self, valdict={}):
        if valdict:
            dict.__init__(self, valdict)

    def __add__(self, other):
        """Add two FloatDicts or a FloatDict and a float.  In the former
        case, add each shared term.  Unshared terms result in the value found
        in the dictionary containing the term.  For floats, each term increased
        by the amount of the float."""
        retval = FloatDict()
        if isinstance(other, dict):
            for k in list(self.keys()):
                if k in list(other.keys()):
                    retval[k] = self[k] + other[k]
                else:
                    retval[k] = self[k]
            for k in list(other.keys()):
                if k not in list(self.keys()):
                    retval[k] = other[k]
        if isinstance(other, float):
            for k in list(self.keys()):
                retval[k] = self[k] + other
        return retval

    def __mul__(self, other):
        """Multiply two FloatDicts or a FloatDict and a float.  In the former
        case, multiply each shared term.  Unshared terms result in zero in the
        result FloatDict.  For floats, each term is multiplied in turn by the
        float value."""
        retval = FloatDict()
        if isinstance(other, dict):
            for k in list(self.keys()):
                if k in list(other.keys()):
                    retval[k] = self[k] * other[k]
                else:
                    retval[k] = 0.0
            for k in list(other.keys()):
                if k not in list(self.keys()):
                    retval[k] = 0.0
        if isinstance(other, float):
            for k in list(self.keys()):
                retval[k] = self[k] * other
        return retval
    
    def __rmul__(self, other):
        retval = FloatDict()
        if isinstance(other, float):
            for k in list(self.keys()):
                retval[k] = self[k] * other
        return retval

    def __div__(self, other):
        """Divide two FloatDicts or a FloatDict and a float.  In the former
        case, multiply each shared term.  Unshared terms result in zero in the
        result FloatDict.  For floats, each term is multiplied in turn by the
        float value."""
        retval = FloatDict()
        if isinstance(other, dict):
            for k in list(self.keys()):
                if k in list(other.keys()):
                    retval[k] = self[k]/other[k]
                else:
                    retval[k] = 0.0
            for k in list(other.keys()):
                if k not in list(self.keys()):
                    retval[k] = 0.0
        if isinstance(other, float):
            for k in list(self.keys()):
                retval[k] = self[k]/other
        return retval

if __name__ == "__main__":
    D = FloatDict({1 : 4.55, 2 : 3.78, 3: 8.22})
    L = FloatDict({1 : 5.4, 2 : 9.4, 4: 11.22})
    print(D)
    print(L)
#    print D*1.4 + L*1.7
    print(1.4*D + 1.7*L)
    print(1.4*D)
