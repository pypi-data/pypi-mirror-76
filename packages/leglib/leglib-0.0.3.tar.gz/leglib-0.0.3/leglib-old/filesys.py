# LegLib path, file and directory routines
import os

def del_file(path):
    "Deletes a file if it exists."
    if os.path.isfile(path):
        os.popen("rm %s" % path)
