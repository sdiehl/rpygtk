# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

import os
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import config

#This is the base class for all windows

class Window(object):
        builder_file = "./ui/main.builder"
        builder = gtk.Builder()
        builder.add_from_file(builder_file)
        title = None
        
        def __init__(self,object):
            global __name__

            self.window = self.builder.get_object(str(object))
            if self.window == None:
                print "Could not load Window: %s" % object
                return
            
            if self.title:
                self.window.set_title(self.title)
            else:
                self.window.set_title(self.__class__.__name__)
                
            self.window.connect('delete-event', lambda w, e: w.destroy() or True)
            self.window.set_destroy_with_parent(True)
            
            if config.__devel__:
                self.window.set_modal(False)
            
            self.handler()
            self.window.show()

        def construct(self,object):
                global __name__
                self.window = self.builder.get_object(str(object))
                if self.window == None:
                    print "Could not load Window: %s" % object
                    return
                self.builder.connect_signals( self )
                
                if self.title:
                    self.window.set_title(self.title)
                else:
                    self.window.set_title(self.__class__.__name__)
                    
                if config.__devel__:
                    self.window.set_modal(False)

                self.window.connect('delete-event', lambda w, e: self.destroy() or True)
                self.handler()
                self.window.show()

        #Unique instructions usually involving data, called before window is shown
        def handler(self):
            pass
        
        def __getattr__(self, name):
            obj = self.builder.get_object(name)
            if obj:
                return obj
            else:
                raise AttributeError("%s instance has no attribute '%s'" % (self.__class__.__name__, name))

        def  __call__(self):
            return self.window
        
        def shrink_window(self,*event):
            '''Called to minimize the size of the window'''
            self.window.resize(1,1)

        def object(self):
            return self.window
            
        def hide(self,*event):
            self.window.hide()
            return True
        
        def show(self,*event):
            self.window.show()
        
        def destroy(self,*event):
            self.window.destroy()
            return True