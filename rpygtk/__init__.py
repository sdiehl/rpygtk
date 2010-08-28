import os, sys, platform

def determine_path ():
    try:
        root = __file__
        if os.path.islink (root):
            root = os.path.realpath (root)
        return os.path.dirname (os.path.abspath (root))
    except:
        print "Unable to determinate application path."
        sys.exit ()

os.chdir(determine_path())

import rpygtk

__all__=['start']