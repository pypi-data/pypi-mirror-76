from leglib.structural.project import Project
from leglib.structural.windcalc_other import WindOtherStructureCalc

wind_calc = WindOtherStructureCalc(
        V=144.0,                # wind speed, mph (ultimate for ASCE 7-10)
        exposure='C',           # exposure class
        Kzt=1.0,                # terrain coefficient
        title="Wind on Duct Supports",
        by="J. Legner")

wind_calc.add_area(z=9.5/2, Af=9.5*6/12, Cf=2.0, name="W6 Column")
wind_calc.add_area(z=8.0, Af=4.625/12.0*11.5, Cf=0.7, name="Lower Pipe")
wind_calc.add_area(z=9.0, Af=4.625/12.0*11.5, Cf=0.7, name="Upper Pipe")
wind_calc.add_area(z=11.5, Af=16.0/12.0*11.5, Cf=2.0, name="Duct")

project = Project(name="CR Hydrated Lime Ducts", number="198801275")
project.add_calc(wind_calc)
project.recalc()
project.write("wind_other_structure_example.txt", "txt", overwrite=True)


