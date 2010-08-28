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
from ui import openfile
from ui.wrappers import *

from lib import rsession
from lib.utils import *

from re import sub
import threading

class TestWindow(window.Window):
    
    custom_variables = None
    active_threads = rsession.ThreadHandler()
    
    def __init__(self,parent,object):
        builder_file = "./ui/test.builder"
        self.builder = gtk.Builder()
        self.builder.add_from_file(builder_file)
        
        #This shouldn't happen,, but it makes sure we don't cause a huge crash
        #by calling objects that don't exist
        if not object:
            error("No active object")
            return
        
        self.parent = parent
        self.active_r_object = object
        
        parent.child_windows.append(self)
        
        if parent.using_docks:
            import gdl
            unique_id = self.title + str(self.__hash__())
            testwindow = gdl.DockItem(unique_id, self.title, None,gdl.DOCK_ITEM_BEH_NORMAL | gdl.DOCK_ITEM_BEH_CANT_ICONIFY)
            #Fetch from builder
            testwindow.add(self.test_vbox)
            parent.dock.add_item(testwindow, gdl.DOCK_TOP)
            testwindow.dock_to(None, gdl.DOCK_FLOATING, -1)
            self.handler()
            testwindow.show_all()
        else:
            self.window = gtk.Window()
            #Fetch from the builder
            self.window.add(self.test_vbox)
            self.window.set_keep_above(True)
            self.window.set_title(self.title)
            self.handler()
            self.window.show()
            self.shrink_window()
        
        
        self.show_variables(object)
        self.generate_test_parameters()
        
        runbutton = self.builder.get_object("runbutton")
        rb = runbutton.connect('clicked', self.run)
        
    def run(self):
        pass
    
    def variables_are_set(self):
        for var in self.custom_variables.values():
            if not var.data:
                return False
        return True
    
    def show_variables(self,object):
        
        def render(object,treeview):
            for column in treeview.get_columns():
                treeview.remove_column(column)
            
            objectstore = gtk.ListStore(str)
            
            col = gtk.TreeViewColumn()
            col.set_property('clickable', True)

            treeview.append_column(col)
            
            cell = gtk.CellRendererText()
            col.pack_start(cell)
            col.add_attribute(cell,'text',0)
            
            for v in object.columns.keys():
                objectstore.append([v])
                
            #If we're working with a time series, allow plotting of the 'hidden' time variable
            if self.active_r_object.type == 'Time Series':
                objectstore.append(['(Time)'])
            
            treeview.set_model(objectstore)
            
        def clear(treeview):
            for column in treeview.get_columns():
                treeview.remove_column(column)
        
        hbox1 = self.builder.get_object("custom_variables")
        objectlist = self.builder.get_object("variables")
        
        for key,obj in self.custom_variables.iteritems():
            hbox1.pack_end(obj.object)
            tabs = self.builder.get_object("pars")
            
            #Hack, this forces the window to resize itself
            tabs.set_current_page(1)
            tabs.set_current_page(0)
            
            hbox1.show_all()
            
        render(object,objectlist)
        
    def generate_test_parameters(self):
        #Normal Parameters
        vbox1 = self.builder.get_object("vbox1_obj")
        vbox1.set_border_width(5)
        vbox1.show()

        vbox2 = self.builder.get_object("vbox2_obj")
        vbox2.set_border_width(5)
        vbox2.show()
        
        if hasattr(self,'parameters'):
            if self.parameters:
                for l,o in self.parameters.iteritems():
                    #Work with the GTK widget
                    o = o.object
                    label = gtk.Label(l)
                    label.show()
                    vbox1.pack_start(label,True,True,0)
                    vbox2.pack_start(o,True,True,0)
                    o.show()
                    
    @handle_errors
    def hide(self):
        #Stop sending updates from the main window
        self.parent.child_windows.remove(self)
            
        #Maybe in the future we'll have stat tests that output graphs???
        if prefs.get_pref('close_plots'):
            rsession.r['graphics.off']()
            self.killall()
        
        #self.window.destroy()
        return True