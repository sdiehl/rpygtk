# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

#------------------------
# GTK Wrappers 
#------------------------

import pygtk
pygtk.require("2.0")
import gtk

#These wrappers are used for plotting/stat dialogs, they
#all have a method get() which returns the various inputs.

class ComboBox(object):
    object = None
    
    def __init__(self,items,default=None):
        combo = gtk.ComboBox()
        ls = gtk.ListStore(str)
        for i in items:
            ls.append([str(i)])
        combo.set_model(ls)
        cellr = gtk.CellRendererText()
        combo.pack_start(cellr)
        combo.add_attribute(cellr, 'text', 0)
        if default:
            combo.set_active(default)
        self.object = combo
        
    def get(self):
        '''Returns the text of the item selected'''
        return self.object.get_active_text()

class CheckBox(object):
    object = None
    
    def __init__(self,text,toggled=False):
        cb = gtk.CheckButton(text)
        cb.set_active(toggled)
        self.object = cb
        
    def get(self):
        '''Returns True or False depending on the state toggled state of the checkbox'''
        return self.object.get_active()
        
class MultipleEntries(object):
    '''Create a series of entry fields'''
    entries = []
    object = None
    
    def __init__(self,n,width=5,expand=False,cast_type=None):
        self.cast_type = cast_type
        self.entries = []
        hbox = gtk.HBox()
        for i in range(n):
            entry = gtk.Entry()
            entry.set_width_chars(width)
            self.entries.append(entry)
            hbox.pack_start(entry,expand=False)
            entry.show()
        self.object = hbox
        
    def get(self):
        '''Returns all the values entered in the multiple fields, if castType is set then the values are
        cast into the specified type'''
        
        #If all the entires are not set, return None
        for entry in self.entries:
            if entry.get_text() == None or entry.get_text() == '':
                return

        fields = [i.get_text() for i in self.entries]
            
        if self.cast_type:
            fields = map(self.cast_type,fields)
            
        if len(self.entries) == 1:
            return fields[0]
        else:
            return fields
            
    def __nonzero__(self):
        #Require all entries to be filled in, otherwise return False
        for entry in self.entries:
            if entry.get_text() == None or entry.get_text() == '':
                return False
        return True

class SingleEntry(MultipleEntries):
    '''Convience wrapper to create a single entry field'''
    def __new__(self,width=5,expand=False,cast_type=None):
        return MultipleEntries(n=1,width=width,expand=expand,cast_type=cast_type)
        
#Miscellaneous Wrappers
    
def yesNoDialog(message):
    '''Creates a Yes/No dialog, returns True if the user selects True, returns
    False if the user presses no or destroys the window'''
    
    message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE,message)
    message.add_buttons(gtk.STOCK_YES,gtk.RESPONSE_YES,gtk.STOCK_NO,gtk.RESPONSE_NO)
    message.set_modal(True)
    message.set_deletable(False)
    message.set_destroy_with_parent(True)
    resp = message.run()
    if resp == gtk.RESPONSE_CLOSE:
        message.destroy()
        return False
    elif resp == gtk.RESPONSE_YES:
        message.destroy()
        return True
    elif resp == gtk.RESPONSE_NO:
        message.destroy()
        return False

#This is used in both the Regression window and Test window classes
#this assumes parent class has an treeview widget 'variables' and
#active_robject
class VariableSelector(gtk.Object):
    
    data = None
    object = None
    
    def __init__(self,parent,label=None,maximum=None):
        '''Factory to produce custom variable selectors'''
        
        self.data = dict()
        
        frame = gtk.Frame()
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        tv = gtk.TreeView()
        tv.set_headers_visible(False)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        
        add_button = gtk.Button(stock=gtk.STOCK_ADD)
        del_button = gtk.Button(stock=gtk.STOCK_REMOVE)
        
        frame.add(vbox)
        if label:
            vbox.pack_start(gtk.Label(label))
        
        vbox.pack_start(scroll)
        scroll.add(tv)
        vbox.pack_start(hbox)
        hbox.pack_start(add_button)
        hbox.pack_start(del_button)
        
        objectstore = gtk.ListStore(str)
        
        col = gtk.TreeViewColumn()
        col.set_property('clickable', False)
        
        tv.append_column(col)
        
        cell = gtk.CellRendererText()
        col.pack_start(cell)
        col.add_attribute(cell,'text',0)
        tv.set_model(objectstore)
        
        def add_multivar(event,*arg):
            if (maximum is not None) and len(tv.get_model()) >= maximum-1:
                add_button.set_sensitive(False)
            else:
                add_button.set_sensitive(True)
            
            treeview = parent.builder.get_object("variables")
            selected = treeview.get_selection().get_selected_rows()
            index = selected[1][0]
            label = selected[0][index][0]
            
            if label not in self.data:
                self.data[label] =  parent.active_r_object.column_data[label]
                tv.get_model().append([label])
        
        def del_multivar(event,*arg):
            selected = tv.get_selection().get_selected_rows()
            
            if not selected:
                return
            
            index = selected[1][0]
            label = selected[0][index][0]
            
            del self.data[label]
            
            tv.get_model().remove(tv.get_selection().get_selected()[1])
            
            if (maximum is not None) and len(tv.get_model()) >= maximum:
                add_button.set_sensitive(False)
            else:
                add_button.set_sensitive(True)
        
        ab = add_button.connect('clicked', add_multivar,tv)
        db = del_button.connect('clicked', del_multivar,tv)
        
        self.object = frame
        
    def hide(self):
        self.object.destroy()
        
    def __getitem__(self,key):
        return self.data.items()[key]
        
    def __len__(self):
        return len(self.data)
        
    def get_first(self):
        '''Get the first data element in a data dictionary'''
        return self.data.items()[0]
