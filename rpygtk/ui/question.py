# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

from ui import window

class About(window.Window):
        def __init__(self):
            self.construct('question')

        def handler(self):
            pass