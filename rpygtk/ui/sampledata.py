import os
import re

import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

from lib.utils import *

from ui import window
from lib import rsession

import numpy

class SampleData(window.Window):
    def __init__(self,parent):
        self.parent = parent
        self.window = gtk.Dialog()
        self.window.add_button(gtk.STOCK_OK,gtk.RESPONSE_CLOSE)
        self.window.set_size_request(400,300)
        self.window.size_request()
        self.datalist = gtk.TreeView()
        self.datalist.set_headers_visible(False)

        self.window.set_modal(True)
        self.window.set_destroy_with_parent(True)
        self.window.set_keep_above(True)
        self.handler()
        scroll = gtk.ScrolledWindow()
        scroll.add(self.datalist)
        self.window.get_content_area().pack_start(scroll)
        self.window.show_all()
        
        response = self.window.run()
        if response == gtk.RESPONSE_CLOSE:
            if self.datalist.get_selection():
                selected = self.datalist.get_selection().get_selected_rows()
                index = selected[1][0]
                dataset = selected[0][index][0]
                
                #Get selected dataset, and *TRY* to load it.
                data = rsession.ro.r(str(dataset))
                
                rsession.env[dataset] = data
                self.parent.sync_with_r()         
            self.hide()
            
    def load_sample_datasets(self):
        #TODO: We can just call 'data()' to collect this...
        #data() can't be coerced into something readable which
        # is a issue because we'd like to be able to read all the
        #datasets in the MASS package and whatnot
        if os.path.exists('/usr/lib/R/library/datasets/CONTENTS'):
            datasets = open('/usr/lib/R/library/datasets/CONTENTS').read()
            entries = re.findall('Entry: (.*)',datasets)
            descriptions = re.findall('Description: (.*)',datasets)
            return zip(entries,descriptions)
            
    def handler(self):
        def render(object,treeview):
            for column in treeview.get_columns():
                treeview.remove_column(column)
            
            objectstore = gtk.ListStore(str,str)
            
            #Two columns
            for i in range(0,2):
                col = gtk.TreeViewColumn()
                if i==0:
                    col.set_property('clickable', True)
                treeview.append_column(col)
            
                cell = gtk.CellRendererText()
                col.pack_start(cell)
                col.add_attribute(cell,'text',i)
            
            for row in object:
                objectstore.append([row[0],row[1]])
            
            treeview.set_model(objectstore)
        
        sampledata = self.load_sample_datasets()
        render(sampledata,self.datalist)       