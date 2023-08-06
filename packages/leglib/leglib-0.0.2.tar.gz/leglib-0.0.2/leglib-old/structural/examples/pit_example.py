from leglib.structural.project import Project
from leglib.structural.pit import Pit

pit_calc = Pit(
        Lp = 8.0,
        Ltoe = 1.5,
        Bp = 7.0,
        dp = 7.0,
        Hg = 1.0,
        tp = 8.0,
        tf = 18.0,
        dwt = 0.0,
        title="Blow-Down Tank Pit",
        by="J. Legner")

pit_calc.soil.gamma_s = 90.0
pit_calc.soil.gamma_sat = 90.0

pit_calc.design()
project = Project(name="Duke Tiger Bay Drains", number="198801254")
project.add_calc(pit_calc)
project.recalc()
project.write("pit_example.txt", "txt", overwrite=True)

