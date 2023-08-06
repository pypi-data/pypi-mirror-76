import glob
import os


if __name__ == '__main__':
    # Run all structural examples
    this_path, this_filename = os.path.split(__file__)
    this_path=os.path.abspath(this_path)
    for filename in os.listdir(this_path):
        fname, ext = os.path.splitext(filename)
        if ext.lower() == ".py" and fname != "__init__":
            exec(open(os.path.join(this_path, filename)).read())
            