#!/usr/bin/env python

# Copyright (c) 2010 Stephen Diehl <sdiehl@clarku.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import config
import getopt

try:
    import pygtk
    pygtk.require("2.0")
except:
    print("PyGTK is required, please install to continue.")
    sys.exit(0)

try:
    import gtk
    import gtk.glade
except:
    print("Gtk/Glade is required, please install to continue.")
    sys.exit(0)

try:
    import numpy
except:
    print("Numpy is required, please install it to continue.")
    sys.exit(0)

try:
    import rpy2
except:
    print("RPY2 is required, please install it to continue.")
    sys.exit(0)

import os, sys, platform

def get_operating_system():
    _platform = platform.system()

    if _platform == 'Linux':
        # All is well :)
        return

    if _platform == 'Windows':
        print('Windows is not supported')
        #Then run a fork bomb... just kidding
        sys.exit(0)
    elif _platform == 'Darwin':
        print('OS X is not supported but you appear to have the right libraries installed so it may work, do you want to continue?')
        if raw_input('y/n: ') != 'y':
            sys.exit(0)
    else:
        import posix
        if not posix.environ['HOME']:
            print("You're either running *nix with a strange filesystem or a non-posix enviroment, but you do appear to have the right libraries installed. Do you want to continue?")
            if raw_input('y/n: ') != 'y':
                sys.exit(0)

def determine_path ():
    try:
        root = __file__
        if os.path.islink(root):
            root = os.path.realpath(root)
        return os.path.dirname(os.path.abspath(root))
    except:
        print "Unable to determinate application path."
        sys.exit(0)

def usage():
    print(config.__name__ + ' ' + config.__version__ + '\n' + config.__comment__)
    print('''
usage: rpygtk.py [options] [files]
Options:
-h      Help information
-d      Enable debugging
-v      Display version information
'''
    )

def start():

        debug = config.__devel__

        try:
            opts, args = getopt.getopt(sys.argv[1:], "dvh",["help"])
        except:
            print("Unknown Error")
            sys.exit(1)

        for opt, optarg in opts:
            if config.__devel__:
                print opt,optarg

            if opt == "-d":
                debug = True
            elif opt == "-v":
                print(config.__name__ + ' ' + config.__version__)
                sys.exit(0)
            elif opt == "-h":
                usage()
                sys.exit(0)
            else:
                print opt,optarg

        get_operating_system()

        if config.__devel__:
            print 'Found application path in', determine_path()

        os.chdir(determine_path())

        from ui import main
        import gobject

        gobject.threads_init()
        Main = main.MainWindow(files=args)

        if debug == True:
            print 'Enable debugging'

        try:
            gtk.main()
        except KeyboardInterrupt:
            #Ensure that if the user SIGQUITs the threads shutdown properly
            Main.shutdown_cleanly()

start()

if config.__devel__:
    pass
