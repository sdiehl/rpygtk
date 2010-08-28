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

class TextOutput(window.Window):
    def __init__(self,text):
        self.construct('textoutput')
        output = self.builder.get_object('output')
        output.get_buffer().set_text(text)

    def handler(self):
        close = self.builder.get_object('close_textoutput')
        close.connect('clicked', self.hide)