import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import gobject

import pango

import numpy

from lib.rsession import translate_types

#This is my best effor to shape gtk.TreeView into something spreadsheet-esque

#TODO: We need to be able have 'NA's in the data

class Datasheet(object):
    '''Handles the rendering of the gtk treeview that renders dataframes and time series'''
    dimensions = [None,None]
    data = []
    columns = []
    editable = False
    #Connections to destroy
    connections = []

    def __init__(self,view,store,parent,editable=False):
        self.view = view
        self.store = store
        self.parent = parent
        self.editable = True

        #Cursor movement is a big WIP for next release

        #b = self.view.connect('move-cursor', self.move_cursor)
        #a = self.view.connect('key-press-event', self.keyPressCallback)
        #self.connections.extend([(self.view,a),(self.view,b)])

        #for item in self.connections:
        #    obj = item[0]
        #    con = item[1] 
        #    obj.disconnect(con)
        #    self.connections.remove(item)
        #b = self.view.connect('move-cursor', self.move_cursor)
        #a = self.view.connect('key-press-event', self.keyPressCallback)

        #self.connections.append((self.view,a))
        #self.connections.append((self.view,b))

        #if len(self.connections) == 0:
        #    b = self.view.connect('move-cursor', self.move_cursor)
        #    a = self.view.connect('key-press-event', self.keyPressCallback)
        #    #self.connections.extend([(self.view,a),(self.view,b)])
        #    print 'signal handler',b
        #    print 'instance',self.view

    def move_cursor(self,treeview, step, count):
        treeview = self.view
        path, column = treeview.get_cursor()
        treeview.set_cursor(path, column, True)
        handler = gobject.timeout_add(100, lambda t, p, c: t.set_cursor(p, c, True),
                            treeview, path, column)

    def toArray(self):
        #Ick, but it works...
        data = []
        for i in self.store:
            row = []
            for j in i:
                row.append(j)
            data.append(row)
        return numpy.array(data)


    def set_columns(self,list_of_vars,types=None):
        self.dimensions[1] = len(list_of_vars)
        self.columns = list_of_vars

        for i,title in enumerate(list_of_vars):
            if types:
                #col = gtk.TreeViewColumn(title + '\n'+ str(translate_types(types[i],reverse=True))+'')
                col = gtk.TreeViewColumn(title + '\n'+ str(translate_types(types[i],reverse=True))+'')
            else:
                #We have to do this so the rownames line up
                col = gtk.TreeViewColumn(title + '\n')
            col.set_property('clickable', True)
            col.set_flags(gtk.CAN_FOCUS)

            self.view.append_column(col)

            cell = gtk.CellRendererText()
            cell.set_property('font-desc', pango.FontDescription('sans 8'))

            if self.editable:
                cell.set_property('editable', True)
                handler = cell.connect('edited', self.edited, (self.store, i))
                self.connections.append((cell,handler))

            col.pack_start(cell)
            col.add_attribute(cell,'text',i)

    def get_column_from_index(self,n):
        '''Returns the title (variable name) from the column index'''
        return self.columns[n]

    def get_index_from_column(self,title):
        '''Returns the column index for the title (variable name)'''
        return self.columns.index(title)

    def add_data(self,data):
        #Cough, Hack, Cough, check to see if we have one column
        if not isinstance(data[0],numpy.ndarray):
            self.store.append([data[0]])
            return
        for row in data:
            self.store.append(row)

    def edited(self,cell, path, new_text, user_data):
        liststore, column = user_data
        try:
            #This isn't pretty but it works because ints can be cast into floats
            #but it will throw a type error if we try and cast a str
            liststore[path][column] = float(new_text)
        except ValueError:
            print "Inputed value does not cast to column type"
            return
        path, column = self.view.get_cursor()
        self.parent.refresh_dataframe()
        self.view.set_model(self.store)
        #self.moveCursorToNextRow(path, column)

    def keyPressCallback(self, widget, event, data=None):
        path, column = self.view.get_cursor()
        if event.keyval == gtk.keysyms.Tab:
            self.moveCursorToNextCell(path, column)

        elif event.keyval == gtk.keysyms.Up:
            pass
            #self.moveCursorToPrevRow(path, column)

        elif event.keyval == gtk.keysyms.Left:
            self.moveCursorToPrevCell(path, column)

        elif event.keyval == gtk.keysyms.Down:
            self.moveCursorToNextRow(path, column)

        elif event.keyval == gtk.keysyms.Right:
            self.moveCursorToNextCell(path, column)
        else:
            self.view.set_cursor(path,column)

    def moveCursorToNextCell(self, path, column):
        columns = self.view.get_columns()
        index = columns.index(column) + 1
        if index == len(columns):
            index = 0
            path = (path[0]+1,)
            try:
                self.store.model.get_iter(path)
            except:
                return

        column = columns[index]
        self.view.set_cursor(path, column)

    def moveCursorToPrevCell(self, path, column):
        columns = self.view.get_columns()
        index = columns.index(column) - 1
        if index == len(columns):
            index = 0
            path = (path[0]+1,)
            try:
                self.store.model.get_iter(path)
            except:
                return

        column = columns[index]
        self.view.set_cursor(path, column)

    def moveCursorToNextRow(self, path, column):
        path = (path[0]+1,)
        try:
            self.store.get_iter(path)
        except:
            pass
            #path = (path[0]-1,)
        self.view.set_cursor(path, column)

    def moveCursorToPrevRow(self, path, column):
        path = (path[0]-1,)
        try:
            self.store.get_iter(path)
        except:
            path = (path[0]+1,)
        self.view.set_cursor(path, column)

    def __getitem__(self,key):
        return self.toArray()[key]

    def iter(self):
        return self.store
