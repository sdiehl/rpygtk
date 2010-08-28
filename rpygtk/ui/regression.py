import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

from ui import window
from ui.wrappers import *
from ui.variable_prompt import VariablePrompt
from ui.openfile import SaveFile
from ui import prefs

from lib import rsession
from lib.formula_parser import FormulaAssistedEntry
from lib.utils import *

nonlinear_models = {'Linear':'y ~ A*x+B',
                    'Quadratic': 'y ~ A*x^2 + B *x + C',
                    'Sinusodial': 'y ~ A * sin(B*x+C)'
                    }

class RegressionWindow(window.Window):
    #Holds variables used for computation
    custom_variables = None

    #Widget Properties
    show_degree_slider = False
    show_model = False

    #Holds the resulting output of regression
    result = None

    active_threads = rsession.ThreadHandler()

    def __init__(self,parent,object):
        builder_file = "./ui/regression.builder"
        self.builder = gtk.Builder()
        self.builder.add_from_file(builder_file)

        #This shouldn't happen,, but it makes sure we don't cause a huge crash
        #by calling objects that don't exist
        if not object:
            error("No active object")
            return

        self.parent = parent
        parent.child_windows.append(self)

        #Widgets
        self.degree_frame = self.builder.get_object("degree_frame")
        self.degree_slider = self.builder.get_object("degree_slider")
        self.degree = self.builder.get_object("degree")
        self.model_frame = self.builder.get_object("model_frame")
        self.model = FormulaAssistedEntry()

        self.active_r_object = object

        if parent.using_docks:
            import gdl
            unique_id = self.title + str(self.__hash__())
            regwindow = gdl.DockItem(unique_id, self.title, None,gdl.DOCK_ITEM_BEH_NORMAL | gdl.DOCK_ITEM_BEH_CANT_ICONIFY)
            #Fetch from builder
            regwindow.add(self.regression_vbox)
            parent.dock.add_item(regwindow, gdl.DOCK_TOP)
            regwindow.dock_to(None, gdl.DOCK_FLOATING, -1)
            self.handler()
            regwindow.show_all()
        else:
            self.window = gtk.Window()
            #Fetch from the builder
            self.window.add(self.regression_vbox)
            self.window.set_keep_above(True)
            self.window.set_title(self.title)
            self.handler()
            self.window.show()
            self.shrink_window()

        #self.construct('regression')
        self.show_variables(object)
        self.show_models()

        self.degree.set_value(2)

        self.builder.get_object('custom_model').add(self.model.widget)
        self.model.set_text('y ~ A*x+B')

        b1 = self.plotfitbutton
        c1 = b1.connect('clicked', self.plot_fit)

        b2 = self.plotsummarybutton
        c2 = b2.connect('clicked', self.plot_summary)

        b3 = self.exportmodelbutton
        c3 = b3.connect('clicked', self.export_model)

        b4 = self.exportfitbutton
        c4 = b4.connect('clicked', self.export_fit)

        b5 = self.exportsummarybutton
        c5 = b5.connect('clicked', self.export_summary)

        if not self.show_degree_slider:
            self.degree_frame.hide()
        else:
            self.degree_frame.show()

        if not self.show_model:
            self.model_frame.hide()
        else:
            self.model_frame.show()

        #self.window.resize(1,1)
        #self.window.set_keep_above(True)

    def plot_fit(self,*args):
        pass

    def plot_summary(self,*args):
        pass

    @handle_errors
    def export_model(self,event):
        object_name = VariablePrompt(['Object Name']).get_inputs()[0]
        if object_name and self.result:
            self.parent.render_linear_model(self.result,object_name)

    @handle_errors
    def export_fit(self,event):
        savedialog = SaveFile(self,filetypes=['svg','png','ps','pdf'])
        uri,extension = savedialog.get_filename()

        if not uri or not extension:
            error('Invalid filename or extension')
            return

        path = get_path_from_url(uri)

        self.plot_fit(event,image=(path,extension))

    @handle_errors
    def export_summary(self,event):
        savedialog = SaveFile(self,filetypes=['svg','png','ps','pdf'])
        uri,extension = savedialog.get_filename()

        if not uri or not extension:
            error('Invalid filename or extension')
            return

        path = get_path_from_url(uri)

        self.plot_summary(event,image=(path,extension))

    def variables_are_set(self):
        for var in self.custom_variables.values():
            if not var.data:
                return False
        return True

    def show_models(self):
        global nonlinear_models

        treeview = self.builder.get_object('preset_models')
        objectstore = gtk.ListStore(str,str)

        for column in treeview.get_columns():
            treeview.remove_column(column)

        for i in xrange(2):
            col = gtk.TreeViewColumn()
            col.set_property('clickable', True)
            treeview.append_column(col)

            cell = gtk.CellRendererText()
            col.pack_start(cell)
            col.add_attribute(cell,'text',i)

        for label,model in nonlinear_models.iteritems():
            objectstore.append([label,model])

        treeview.connect('row-activated', self.selectmodel)
        treeview.set_model(objectstore)

    def selectmodel(self,treeview,path,viewcolumn):
        #The selected row's second column
        formula = treeview.get_model()[path][1]
        self.model.set_text(str(formula))

    def get_model(self):
        return self.model.get_text()

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

    @handle_errors
    def hide(self):
        #Stop sending updates from the main window
        self.parent.child_windows.remove(self)

        if prefs.get_pref('close_plots'):
            rsession.r['graphics.off']()
            self.killall()

        #self.window.hide()
        return True
