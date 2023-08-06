from leglib.structural.driftcalc import DriftCalc
from leglib.structural.project import Project

drift_calc = DriftCalc(
        pg=70.0,                # ground snow load, psf
        lu=230,                 # tributary length of roof, feet
        hc=7.0,                 # height of obstruction, feet
        Ce=1.1,                 # exposure coefficient
        Ct=1.0,                 # thermal coefficient
        I=1.1,                  # importance factor
        is_leeward=False,       # True if leeward, False if windward
        title="Drift Against Parapet",
        by="J. Legner")

project = Project(name="7 Hazen Dr Cooling Tower", number="198801125")
project.add_calc(drift_calc)
project.recalc()
project.write("project_example.txt", "txt", overwrite=True)

