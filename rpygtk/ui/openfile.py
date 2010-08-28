# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

from os import environ
import gtk
import urllib
from ui import window
from lib.utils import *

class OpenFile(window.Window):
    def __init__(self,parent,filetypes=[],include_wildcard=False):
        self.parent = parent
        self.window = gtk.FileChooserDialog(title='Open file...',
                                            action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                            buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        
        self.window.set_modal(True)
        self.window.set_keep_above(True)
        
        #Set to the user's home folder
        self.window.set_current_folder(environ['HOME'])
        
        for ft in filetypes:
            filter = gtk.FileFilter()
            filter.set_name(".%s" % ft)
            filter.add_pattern("*.%s" % ft)
            self.window.add_filter(filter)
            
        if include_wildcard:
            filter = gtk.FileFilter()
            filter.set_name("All files")
            filter.add_pattern("*.*")
            self.window.add_filter(filter)
            
        self.window.show()
        
        response = self.window.run()
        if (response == gtk.RESPONSE_CANCEL) or (response == gtk.RESPONSE_OK):
            self.hide()
            
    def get_filename(self):
        return (self.window.get_uri(),self.window.get_filter().get_name())

class SaveFile(window.Window):
    def __init__(self,parent,filetypes=[]):
        self.parent = parent
        self.window = gtk.FileChooserDialog(title='Save as...',
                                            action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                            buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        
        self.window.set_modal(True)
        self.window.set_keep_above(True)
        
        for ft in filetypes:
            filter = gtk.FileFilter()
            filter.set_name(".%s" % ft)
            filter.add_pattern("*.%s" % ft)
            self.window.add_filter(filter)
        
        self.window.show()
        
        response = self.window.run()
        if (response == gtk.RESPONSE_CANCEL) or (response == gtk.RESPONSE_OK):
            self.hide()
            
    def get_filename(self):
        return (self.window.get_uri(),self.window.get_filter().get_name())