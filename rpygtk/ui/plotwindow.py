import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

from ui import prefs
from ui import window
from ui import openfile
from ui.wrappers import *

from lib import rsession
from lib.utils import *

from re import sub
import threading

class PlotWindow(window.Window):
    title = None

    #Data to plot, stored in RVectors
    x = None
    y = None
    data = odict()

    active_r_object = None
    plotwindow = None
    active_threads = rsession.ThreadHandler()

    #Disable certain subsets of the default dialog
    disable_x = False
    disable_y = False
    disable_points = False
    disable_lines = False
    disable_fill = False
    disable_frame = False

    multivariable = False

    def __init__(self,parent,object):
        self.active_r_object = object
        self.parent = parent
        
        #This shouldn't happen,, but it makes sure we don't cause a huge crash
        #by calling objects that don't exist
        if not object:
            error("No active object")
            return
        
        parent.child_windows.append(self)
        
        self.builder = gtk.Builder()
        self.builder.add_from_file("./ui/plot.builder")
        
        self.fill_style = self.builder.get_object("fill_style")
        self.line_style = self.builder.get_object("line_style")
        self.point_style = self.builder.get_object("point_style")
        self.frame_style = self.builder.get_object("frame_style")
        
        if parent.using_docks:
            import gdl
            unique_id = self.title + str(self.__hash__())
            plotwindow = gdl.DockItem(unique_id, self.title, None,gdl.DOCK_ITEM_BEH_NORMAL | gdl.DOCK_ITEM_BEH_CANT_ICONIFY)
            #Fetch from builder
            plotwindow.add(self.plotview)
            parent.dock.add_item(plotwindow, gdl.DOCK_TOP)
            plotwindow.dock_to(None, gdl.DOCK_FLOATING, -1)
            self.handler()
            plotwindow.show_all()
        else:
            self.window = gtk.Window()
            #Fetch from the builder
            self.window.add(self.plotview)
            self.window.set_keep_above(True)
            self.window.set_title(self.title)
            self.handler()
            self.window.show()
            self.shrink_window()

        if self.multivariable:
            self.builder.get_object("data_single").hide()
            self.builder.get_object("data_multiple").show()
        else:
            self.builder.get_object("data_single").show()
            self.builder.get_object("data_multiple").hide()

        if self.disable_lines:
            self.builder.get_object("lines_frame").hide()
        else:
            self.builder.get_object("lines_frame").show()

        if self.disable_frame:
            self.builder.get_object("frame_frame").hide()
        else:
            self.builder.get_object("frame_frame").show()

        if self.disable_points:
            self.builder.get_object("points_frame").hide()
        else:
            self.builder.get_object("points_frame").show()

        if self.disable_fill:
            self.builder.get_object("fill_frame").hide()
        else:
            self.builder.get_object("fill_frame").show()

        if not hasattr(self,'parameters'):
            #The parameter tab
            self.builder.get_object('pars').get_nth_page(2).hide()
        else:
            self.builder.get_object('pars').get_nth_page(2).show()

        if not hasattr(self,'advanced_parameters'):
            #The advanced parameter tab
            self.builder.get_object('pars').get_nth_page(3).hide()
        else:
            self.builder.get_object('pars').get_nth_page(3).show()

        #Flush the data
        self.x,self.y = None,None
        self.data = dict()

        #Flush the labels
        self.xlab.set_text('')
        self.ylab.set_text('')

        self.show_variables(object)
        self.generate_plot_parameters()

        plotbutton = self.builder.get_object("plotbutton")
        pb = plotbutton.connect('clicked', self.plot)

        exportimage = self.builder.get_object("export_as_image")
        ei = exportimage.connect('clicked', self.exportimage)

        #Switch to the current

        #This is a hack, but it forces the window to resize to fit the tab
        self.builder.get_object('pars').set_current_page(0)
        self.builder.get_object('pars').set_current_page(1)
        self.builder.get_object('pars').set_current_page(0)

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

        #Handle Multivariable selector
        if self.multivariable:
            variables = self.builder.get_object("variables")
            active_variables = self.builder.get_object("active_variables")
            add_button = self.builder.get_object("add_variable")
            del_button = self.builder.get_object("del_variable")

            ab = add_button.connect('clicked', self.select_multivar)
            db = del_button.connect('clicked', self.del_multivar)

            render(object,variables)

            treeview = active_variables

            for column in treeview.get_columns():
                treeview.remove_column(column)

            objectstore = gtk.ListStore(str)

            col = gtk.TreeViewColumn()
            col.set_property('clickable', False)

            treeview.append_column(col)

            cell = gtk.CellRendererText()
            col.pack_start(cell)
            col.add_attribute(cell,'text',0)
            treeview.set_model(objectstore)

        #Specify x,y variables
        else:
            if not self.disable_x:
                variable1 = self.builder.get_object("variable1")
                variable1.set_sensitive(True)
                variable1.connect('button-press-event', self.selectx)
                render(object,variable1)
            else:
                variable1 = self.builder.get_object("variable1")
                variable1.set_sensitive(False)
                clear(variable1)

            if not self.disable_y:
                variable2 = self.builder.get_object("variable2")
                variable2.set_sensitive(True)
                variable2.connect('button-press-event', self.selecty)
                render(object,variable2)
            else:
                variable2 = self.builder.get_object("variable2")
                variable2.set_sensitive(False)
                clear(variable2)

    def selectx(self,treeview,event):
        if event.button == 1:
            x = int(event.x)
            y = int(event.y)
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
            else:
                return

            for i,j in enumerate(treeview.get_columns()):
                if j == col:
                    index = i

            label = treeview.get_model()[path][index]

            self.x = self.active_r_object.column_data[label]

            #Set the xlabel to the variable name by default
            self.builder.get_object("xlab").set_text(label)

    def selecty(self,treeview,event):
        if event.button == 1:
            x = int(event.x)
            y = int(event.y)
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
            else:
                return

            for i,j in enumerate(treeview.get_columns()):
                if j == col:
                    index = i

            label = treeview.get_model()[path][index]

            self.y = self.active_r_object.column_data[label]

            #Set the ylabel to the variable name by default
            self.builder.get_object("ylab").set_text(label)

    def select_multivar(self,event):
        treeview = self.builder.get_object("variables")
        selected = treeview.get_selection().get_selected_rows()
        index = selected[1][0]
        label = selected[0][index][0]
        if label in self.data:
            return

        self.data[label] = self.active_r_object.column_data[label]

        self.builder.get_object("active_variables").get_model().append([label])

    def del_multivar(self,event):
        active_variables = self.builder.get_object("active_variables")
        selected = active_variables.get_selection().get_selected_rows()
        if not selected:
            return
        index = selected[1][0]
        label = selected[0][index][0]

        if label in self.data:
            del self.data[label]
        active_variables.get_model().remove(active_variables.get_selection().get_selected()[1])

    def fetch_labels(self):
        parse = rsession.r.parse
        _xlab = self.builder.get_object("xlab").get_text()
        _ylab = self.builder.get_object("ylab").get_text()
        _title = self.builder.get_object("title").get_text()
        _xmin = self.builder.get_object("xmin").get_text()
        _ymin = self.builder.get_object("ymin").get_text()
        _xmax = self.builder.get_object("xmax").get_text()
        _ymax = self.builder.get_object("ymax").get_text()

        #http://sekhon.berkeley.edu/library/grDevices/html/plotmath.html
        #Handle Plotmath for labels
        if self.builder.get_object("exp1").get_active():
            _xlab = sub('\s+', '~', _xlab)
            _xlab = parse(text=_xlab)

        if self.builder.get_object("exp2").get_active():
            _ylab = sub('\s+', '~', _ylab)
            _ylab = parse(text=_ylab)

        if self.builder.get_object("exp3").get_active():
            _title = sub('\s+', '~', _title)
            _title = parse(text=_title)

        return _xlab,_ylab,_title,_xmin,_ymin,_xmax,_ymax

    def variables_are_set(self):
        if self.multivariable and len(self.data) > 0:
            return True
        elif not self.multivariable:
            if (self.disable_x or self.x) and (self.disable_y or self.y):
                return True
            else:
                return False
        else:
            return False

    def plot(self,event,*image):
        pass

    def exportimage(self,event):
        savedialog = openfile.SaveFile(self,filetypes=['svg','png','ps','pdf'])
        uri,extension = savedialog.get_filename()

        if not uri or not extension:
            error('Invalid filename or extension')
            return

        path = get_path_from_url(uri)

        self.plot(event,(path,extension))

    def killall(self):
        '''Kill all spawned threads, and make sure they stay dead'''
        for thread in self.active_threads:
            thread.halt = True
            self.active_threads.remove(thread)

    def generate_plot_parameters(self):

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

        #Advanced Parameters
        vbox3 = self.builder.get_object("vbox3_obj")
        vbox3.set_border_width(5)
        vbox3.show()

        vbox4 = self.builder.get_object("vbox4_obj")
        vbox4.set_border_width(5)
        vbox4.show()
        
        if hasattr(self,'advanced_parameters'):
            if self.advanced_parameters:
                for l,o in self.advanced_parameters.iteritems():
                    #Work with the GTK widget
                    o = o.object
                    label = gtk.Label(l)
                    label.show()
                    vbox3.pack_start(label,False,False,0)
                    o.show()
                    vbox4.pack_start(o,False,False,0)

    def get_line_color(self):
        return gtkColorToRColor(self.builder.get_object('line_color').get_color())

    def get_fill_color(self):
        return gtkColorToRColor(self.builder.get_object('fill_color').get_color())

    def get_point_color(self):
        return gtkColorToRColor(self.builder.get_object('point_color').get_color())

    def get_fill_style(self):
        return self.fill_style.get_active()

    def get_line_style(self):
        return self.line_style.get_active()

    def get_point_style(self):
        return self.point_style.get_active()

    def get_frame_style(self):
        frames = ['n','o',"L", "7", "c", "u","]"]
        return frames[self.frame_style.get_active()]

    def fill_handler(self,event):
        #If rainbow or gray is selected we turn off the fill color selector
        if self.fill_style.get_active() == 1 or self.fill_style.get_active() == 2:
            self.builder.get_object('fill_color').set_sensitive(False)
        else:
            self.builder.get_object('fill_color').set_sensitive(True)

    @handle_errors
    def hide(self):
        #Stop sending updates from the main window
        self.parent.child_windows.remove(self)

        if prefs.get_pref('close_plots'):
            rsession.r['graphics.off']()
            self.killall()
        
        #self.window.destroy()
        return True
