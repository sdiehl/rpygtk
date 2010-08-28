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

class VariablePrompt(window.Window):
    inputs = []
    
    def __init__(self,args):
        '''Prompt the user for variables, take a list of strings to use for returned values'''
        self.inputs = []
        
        self.window = gtk.Dialog()
        
        self.window.set_keep_above(True)
        
        self.window.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK,gtk.RESPONSE_OK)
        self.window.connect('response', lambda w, e: w.hide() or True)
        
        self.window.set_modal(True)
        
        hbox = gtk.HBox(False,5)
        hbox.show()
        self.window.get_content_area().pack_start(hbox)
        
        vbox1 = gtk.VBox(False, 5)
        vbox1.set_border_width(5)
        vbox1.show()
        
        vbox2 = gtk.VBox(False, 5)
        vbox2.set_border_width(5)
        vbox2.show()
        
        for arg in args:
            label = gtk.Label(arg)
            label.show()
            vbox1.pack_start(label,True,True,0)
            input = gtk.Entry()
            self.inputs.append(input)
            input.show()
            vbox2.pack_start(input,True,True,0)
        
        hbox.pack_start(vbox1)
        hbox.pack_start(vbox2)
        self.window.show()
        
        #Pause main loop for input
        response = self.window.run()
        if response == gtk.RESPONSE_CANCEL:
            self.hide()
        
    def get_inputs(self,allow_empty=False):
        '''Return inputted values, unless field is left empty then return None'''
        
        inputs = [input.get_text() for input in self.inputs]
        if not allow_empty:
            for value in inputs:
                if value == '':
                    print "Invalid input"
                    return
        return [input.get_text() for input in self.inputs]
