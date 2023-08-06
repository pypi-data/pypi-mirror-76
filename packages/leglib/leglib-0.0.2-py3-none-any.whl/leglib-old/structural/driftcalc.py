from structural import IBC2009
from structural.calc import BaseCalc

class DriftCalc(BaseCalc):

    def __init__(self, pg, lu, hc, Ce=1.0, Ct=1.0, I=1.0, is_leeward=True,
            code=IBC2009, title="", project="", project_number="", by=""):
        super(DriftCalc, self).__init__(title, project, project_number, by)
        # Create a drift that is owned by DriftCalc
        self.code = code
        self.recalc
        self.drift = self.code.asce7.SnowDrift(pg=pg, lu=lu, hc=hc,
                is_leeward=is_leeward, I=I, Ce=Ce, Ct=Ct)

    @classmethod
    def from_drift(self, drift):
        assert isinstance(drift, self.code.asce7.SnowDrift)
        self.drift = drift

    def recalc(self):
        self.drift.recalc()

