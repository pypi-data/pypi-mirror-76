# Import all ASCE 7-05 and then override where necessary
from .asce7_05 import *

name = "ASCE7-10"
ASD_WIND_FACTOR = 0.6

def qz(V, z, exposure="C", case=1, Kd=0.85, Kzt=1.0):
    Kd = float(Kd)
    Kzt = float(Kzt)
    V = float(V)
    z = float(z)
    _Kz = round(Kz(z, exposure, case), 2)
    return 0.00256*Kzt*_Kz*Kd*V*V

