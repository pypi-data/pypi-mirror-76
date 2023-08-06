import math

class Roof:

    def __init__(self, W, rise=0.25, slippery=True):
        self.rise = rise            # inches per foot
        self.W = W                  # eave to ridge
        self.slippery = slippery    # eave to ridge

    def theta(self):
        return math.degrees(math.atan(self.rise/12.0))

