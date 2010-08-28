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

import config

from ui import window

class About(window.Window):
        def __init__(self):
            self.window = gtk.AboutDialog()
            self.handler()
            self.window.run()
            self.window.destroy()

        def handler(self):
                self.window.set_name(config.__name__)
                self.window.set_authors(config.__authors__ + config.__credits__)
                self.window.set_version(config.__version__)
                self.window.set_license(config.__license__)
                self.window.set_website(config.__website__)
                self.window.set_comments(config.__comment__)
                self.window.set_copyright("Copyright \302\251 2009-2010 Stephen Diehl")
                self.window.set_logo(gtk.gdk.pixbuf_new_from_file('/usr/share/icons/gnome/scalable/categories/applications-utilities.svg'))