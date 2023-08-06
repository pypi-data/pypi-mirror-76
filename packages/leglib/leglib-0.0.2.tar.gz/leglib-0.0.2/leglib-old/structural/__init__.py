# Building code settings
from .asce7_05 import *
from .asce7_10 import *


class BuildingCode:

    def __init__(self, index, fullname, name, asce7):
        self.index = index
        self.name = name
        self.fullname = fullname
        self.asce7 = asce7

    def __str__(self):
        return self.name


NONE = BuildingCode(0, "No Building Code Specified", "No Code", asce7_05)
IBC2009 = BuildingCode(1, "2009 International Building Code", "2009 IBC",
        asce7_05)
FBC2010 = BuildingCode(2, "2010 Florida Building Code", "2010 FBC", asce7_10)

codes = (NONE, IBC2009, FBC2010)

code = IBC2009

def set_code(new_code):
    global code
    code = new_code
    return code

