""" Text table """

ALIGN_LEFT = 1
ALIGN_RIGHT = 2

class TextTableColumn:
    def __init__(self, width = 10, align = ALIGN_RIGHT):
        self.width = width
        self.align = align

    def fmt(self, value):
        if self.align == ALIGN_RIGHT:
            return ("%%%ds" % self.width) % value
        else:
            return ("%%-%ds" % self.width) % value

class TextTable:
    def __init__(self, columns = []):
        self.cols = columns
        self.rows = []      # Stores data in tuples

    def append_column(self, name):
        "Adds a column."
        self.cols.append(name)

    def __str__(self):
        "Returns informal string representation."
        retval = ""

