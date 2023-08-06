"""
Utilities for importing and exporting DXF files.
Currently limited to 2D lines only.
"""
import re

# List of group codes that should be string values
STR_CODES = list(range(10))
STR_CODES.extend((100, 102, 105))
STR_CODES.extend(list(range(300, 370)))
STR_CODES.extend(list(range(390, 400)))
STR_CODES.extend(list(range(430, 440)))
STR_CODES.extend(list(range(470, 480)))
STR_CODES.extend(list(range(1000, 1010)))

# List of group codes that should be integer values
INT_CODES = list(range(60, 100))
INT_CODES.extend(list(range(170, 180)))
INT_CODES.extend(list(range(270, 290)))
INT_CODES.extend(list(range(370, 390)))
INT_CODES.extend(list(range(400, 410)))
INT_CODES.extend(list(range(420, 430)))
INT_CODES.extend(list(range(440, 460)))
INT_CODES.extend(list(range(1060, 1073)))

# List of group codes that should be integer values
FLOAT_CODES = list(range(10, 60))
FLOAT_CODES.extend(list(range(110, 150)))
FLOAT_CODES.extend(list(range(210, 240)))
FLOAT_CODES.extend(list(range(460, 470)))
FLOAT_CODES.extend(list(range(1010, 1060)))

# List of group codes that should be boolean values
BOOL_CODES = list(range(290, 300))

# Map of used group codes to entity properties
CODES = {\
        100 : "subclass",
        10 : "x1",
        11 : "x2",
        20 : "y1",
        21 : "y2",
        30 : "z1",
        31 : "z2",
        5 : "handle",
        8 : "layer",
        6 : "linetype",
        1 : "textstring",
        2 : "name",
        430 : "color"}

# Tuple of entity types from pp. 73 and 74 of DXF specification
ENTITIES = ( "3DFACE", "3DSOLID", "ACAD_PROXY_ENTITY", "ARC", "ATTDEF",
        "ATTRIB", "BODY", "CIRCLE", "DIMENSION", "ELLIPSE", "HATCH", "HELIX",
        "IMAGE", "INSERT", "LEADER", "LIGHT", "LINE", "LWPOLYLINE", "MLEADER",
        "MLEADERSTYLE", "MLINE", "MTEXT", "OLE2FRAME", "OLEFRAME", "POINT",
        "POLYLINE", "RAY", "REGION", "SECTION", "SEQEND", "SHAPE", "SOLID",
        "SPLINE", "SUN", "SURFACE", "TABLE", "TEXT", "TOLERANCE", "TRACE",
        "UNDERLAY", "VERTEX", "VIEWPORT", "WIPEOUT", "XLINE")

class DxfFile:
    """The DXF file is composed of pairs of group codes and values.  Each
    group code confers the meaning of the value that follows it.  Here is a list
    of the group codes per http://images.autodesk.com/adsk/files/acad_dxf0.pdf
    for the AutoCAD 2008 version of DXF:

    Group code Description

    -5      APP: persistent reactor chain

    -4      APP: conditional operator (used only with ssget)

    -3      APP: extended data (XDATA) sentinel (fixed)

    -2      APP: entity name reference (fixed)

    -1      APP: entity name. The name changes each time a drawing is opened.
            It is never saved (fixed)

    0       Text string indicating the entity type (fixed)

    1       Primary text value for an entity

    2       Name (attribute tag, block name, and so on)

    3-4     Other text or name values

    5       Entity handle; text string of up to 16 hexadecimal digits (fixed)

    6       Linetype name (fixed)

    7       Text style name (fixed)

    8       Layer name (fixed)

    9       DXF: variable name identifier (used only in HEADER section of the
            DXF file)

    10      Primary point; this is the start point of a line or text entity,
            center of a circle, and so on
            DXF: X value of the primary point (followed by Y and Z value codes
            20 and 30)
            APP: 3D point (list of three reals)

    11-18   Other points
            DXF: X value of other points (followed by Y value codes 21-28 and Z
            value codes 31-38)
            APP: 3D point (list of three reals)

    20, 30  DXF: Y and Z values of the primary point

    21-28   DXF: Y and Z values of other points

    31-37   DXF: Y and Z values of other points

    38      DXF: entity's elevation if nonzero

    39      Entity's thickness if nonzero (fixed)

    40-48   Double-precision floating-point values (text height, scale factors,
            and so on)

    48      Linetype scale; double precision floating point scalar value;
            default value is defined for all entity types.

    49      Repeated double-precision floating-point value. Multiple 49 groups
            may appear in one entity for variable-length tables (such as the
            dash lengths in the LTYPE table). A 7x group always appears before
            the first 49 group to specify the table length

    50-58   Angles (output in degrees to DXF files and radians through AutoLISP
            and ObjectARX applications)

    60      Entity visibility; integer value; absence or 0 indicates visibility;
            1indicates invisibility

    62      Color number (fixed)

    66      "Entities follow" flag (fixed)

    67      Space that is, model or paper space (fixed)

    70-78   Integer values, such as repeat counts, flag bits, or modes

    90-99   32-bit integer values

    100     Subclass data marker (with derived class name as a string). Required
            for all objects and entity classes that are derived from another
            concrete class. The subclass data marker segregates data defined by
            different classes in the inheritance chain for the same object.
            This is in addition to the requirement for DXF names for each
            distinct concrete class derived from ObjectARX (see Subclass Markers
            (page 276))

    102     Control string, followed by "{<arbitrary name>" or "}". Similar to
            the xdata 1002 group code, except that when the string begins with
            "{", it can be followed by an arbitrary string whose interpretation
            is up to the application. The only other control string allowed is
            "}" as a group terminator. AutoCAD does not interpret these strings
            except during drawing audit operations. They are for application use

    105     Object handle for DIMVAR symbol table entry

    110     UCS origin (appears only if code 72 is set to 1)
            DXF: X value; APP: 3D point

    111     UCS X-axis (appears only if code 72 is set to 1)
            DXF: X value; APP: 3D vector

    112     UCS Y-axis (appears only if code 72 is set to 1)
            DXF: X value; APP: 3D vector

    120-122 DXF: Y value of UCS origin, UCS X-axis, and UCS Y-axis

    130-132 DXF: Z value of UCS origin, UCS X-axis, and UCS Y-axis

    140-149 Double-precision floating-point values (points, elevation, and
            DIMSTYLE settings, for example)

    170-179 16-bit integer values, such as flag bits representing DIMSTYLE
            settings

    210     Extrusion direction (fixed)
            DXF: X value of extrusion direction
            APP: 3D extrusion direction vector

    220     DXF: Y and Z values of the extrusion direction

    230     DXF: Y and Z values of the extrusion direction

    270-279 16-bit integer values

    280-289 16-bit integer value

    290-299 Boolean flag value

    300-309 Arbitrary text strings

    310-319 Arbitrary binary chunks with same representation and limits as 1004
            group codes: hexadecimal strings of up to 254 characters represent
            data chunks of up to 127 bytes

    320-329 Arbitrary object handles; handle values that are taken "as is".
            They are not translated during INSERT and XREF operations

    330-339 Soft-pointer handle; arbitrary soft pointers to other objects within
            same DXF file or drawing.
            Translated during INSERT and XREF operations

    340-349 Hard-pointer handle; arbitrary hard pointers to other objects within
            same DXF file or drawing.
            Translated during INSERT and XREF operations

    350-359 Soft-owner handle; arbitrary soft ownership links to other objects
            within same DXF file or drawing.
            Translated during INSERT and XREF operations

    360-369 Hard-owner handle; arbitrary hard ownership links to other objects
            within same DXF file or drawing. Translated during INSERT and XREF
            operations

    370-379 Lineweight enum value (AcDb::LineWeight). Stored and moved around
            as a 16-bit integer. Custom non-entity objects may use the full
            range, but entity classes only use 371-379 DXF group codes in their
            representation, because AutoCAD and AutoLISP both always assume a
            370 group code is the entity's lineweight. This allows 370 to behave
            like other "common" entity fields

    380-389 PlotStyleName type enum (AcDb::PlotStyleNameType). Stored and moved
            around as a 16-bit integer. Custom non-entity objects may use the
            full range, but entity classes only use 381-389
            DXF group codes in their representation, for the same reason as the
            Lineweight range above

    390-399 String representing handle value of the PlotStyleName object,
            basically a hard pointer, but has a different range to make backward
            compatibility easier to deal with. Stored and moved around as an
            object ID (a handle in DXF files) and a special type in AutoLISP.
            Custom non-entity objects may use the full range, but entity classes
            only use 391-399 DXF group codes in their representation, for the
            same reason as the lineweight range above

    400-409 16-bit integers

    410-419 String

    420-427 32-bit integer value. When used with True Color; a 32-bit integer
            representing a 24-bit color value. The high-order byte (8 bits) is
            0, the low-order byte an unsigned char holding the Blue value
            (0-255), then the Green value, and the next-to-high order byte is
            the Red Value. Convering this integer value to hexadecimal yields
            the following bit mask: 0x00RRGGBB. For example, a true color with
            Red==200, Green==100 and Blue==50 is 0x00C86432, and in DXF, in
            decimal, 13132850

    430-437 String; when used for True Color, a string representing the name of
            the color

    440-447 32-bit integer value. When used for True Color, the transparency
            value

    450-459 Long

    460-469 Double-precision floating-point value

    470-479 String

    999     DXF: The 999 group code indicates that the line following it is a
            comment string. SAVEAS does not include such groups in a DXF output
            file, but OPEN honors them and ignores the comments. You can use the
            999 group to include comments in a DXF file that you've edited

    1000    ASCII string (up to 255 bytes long) in extended data

    1001    Registered application name (ASCII string up to 31 bytes long) for
            extended data

    1002    Extended data control string ("{" or "}")

    1003    Extended data layer name

    1004    Chunk of bytes (up to 127 bytes long) in extended data

    1005    Entity handle in extended data; text string of up to 16 hexadecimal
            digits

    1010    A point in extended data
            DXF: X value (followed by 1020 and 1030 groups)
            APP: 3D point

    1020, 1030  DXF: Y and Z values of a point

    1011        A 3D world space position in extended data
                DXF: X value (followed by 1021 and 1031 groups)
                APP: 3D point

    1021, 1031  DXF: Y and Z values of a world space position

    1012        A 3D world space displacement in extended data
                DXF: X value (followed by 1022 and 1032 groups)
                APP: 3D vector

    1022, 1032  DXF: Y and Z values of a world space displacement

    1013        A 3D world space direction in extended data
                DXF: X value (followed by 1022 and 1032 groups)
                APP: 3D vector

    1023, 1033  DXF: Y and Z values of a world space direction

    1040        Extended data double-precision floating-point value

    1041        Extended data distance value

    1042        Extended data scale factor

    1070        Extended data 16-bit signed integer

    1071        Extended data 32-bit signed long

    There are six sections in a DXF file:
    HEADER
    CLASSES
    TABLES
    BLOCKS
    ENTITIES
    OBJECTS
    """

    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        self.cur_row = 0

    def parse_group_codes(self):
        """Converts the codes and values to tuples. Starting with line 0,
        each even line is a group code and each odd line is a value.
        Values are converted to their appropriate types and saved in
        a list called self.data."""
        self.data = []  # List of (group_code, value) values
        for i in range(0, len(self.lines)):
            if not i%2:
                group_code = int(self.lines[i])
            else:
                if group_code in INT_CODES:
                    val = int(self.lines[i])
                elif group_code in STR_CODES:
                    val = self.lines[i]
                elif group_code in BOOL_CODES:
                    val = bool(self.lines[i])
                elif group_code in FLOAT_CODES:
                    val = float(self.lines[i])
                else:
                    print("Group code %d not found." % group_code)
                    val = None
                self.data.append((group_code, val))
#        for d in self.data:
#            print d

    def read_drawing(self):
        "Returns a drawing object."
        f = open(self.filename, "r")
        line = f.readline()
        while line:
            self.lines.append(line.strip())
            line = f.readline()
        f.close()
        self.parse_group_codes()
        return self.interpret_data()

    def next(self, restart = False):
        "Returns the next (group_code, value) tuple from self.data."
        if restart:
            self.cur_row = 0
            return self.data[0]
        else:
            self.cur_row = self.cur_row + 1
            if self.cur_row < len(self.data):
                return self.data[self.cur_row]
            else:
                return None

    def read_entity(self):
        # Start reading the pairs and store as entity attributes
        pair = next(self)
        ent = AcDbEntity()
        while pair[0] != 0:
            code, val = pair
            ent.__setattr__(code, val)
            pair = next(self)
        self.cur_row -= 1
        return ent

    def interpret_data(self):
        """Returns a drawing object by evaluating the data in self.data which
        was created by parse_group_codes."""
        dwg = Drawing()
        pair = self.next(restart = True)
        cur_sec = None
        while pair is not None:
            if pair[0] == 0:
                val = pair[1].strip().upper()
                if val == "SECTION":
                    cur_sec = self.next()[1]
                # Ignore entities within blocks for now to avoid strange
                # results when using new bears06.framework system
                elif val in ENTITIES and cur_sec != "BLOCKS":
                    dwg.entities.append(self.read_entity())
            pair = next(self)
        return dwg


class AcDbEntity:
    def __init__(self):
        pass

    def __setattr__(self, code, value):
        if code in list(CODES.keys()):
            if value != "AcDbEntity":
                self.__dict__[CODES[code]] = value

    def __str__(self):
        return str(self.__dict__)

class EntityCollection(list):
    "A list of AutoCAD entities with filter capabilities."
    def __init__(self):
        list.__init__(self)

    def regex_filter(self, attr, regex):
        "Same as filter, except using regular expression."
        rx = re.compile(regex)
        retval = EntityCollection()
        for e in self:
            if attr in list(e.__dict__.keys()):
                if rx.match(e.__dict__[attr]) is not None:
                    retval.append(e)
        return retval


    def filter(self, attr, value):
        "Return a list of all entities with a particular value."
        retval = EntityCollection()
        for e in self:
            if attr in list(e.__dict__.keys()):
                if e.__dict__[attr] == value:
                    retval.append(e)
        return retval

class Drawing:
    def __init__(self):
        # List of drawing entities
        self.entities = EntityCollection()


def import_dxf(filename):
    f = DxfFile(filename)
    return f.read_drawing()


if __name__ == "__main__":
    fname = "/home/legeng/eng/projects/0265_bethany/dwgs/grids.dxf"
    print(import_dxf(fname))
