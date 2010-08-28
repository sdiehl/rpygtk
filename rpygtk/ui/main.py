# Copyright (c) 2010 Stephen Diehl <sdiehl@clarku.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import pango
import numpy

from lib.utils import *
from lib import readfiles
from lib import rsession

from ui.window import Window
from ui import datasheet
from ui import about
from ui.openfile import OpenFile, SaveFile

from ui import regression
from ui.plots import BarPlot, ScatterPlot, Histogram, PiePlot, MultiScatter, QQPlot, BoxPlot
from ui.textoutput import TextOutput

from ui import prefs
from ui import sampledata
from ui import randomgen
from ui import variable_prompt
from ui import stat_tests
from ui import wrappers

from config import __name__

try:
    #This is still experimental, and segfaults a lot if you push it
    if config.__devel__:
        import gdl
        using_docks = True
    else:
        using_docks = False
except:
    using_docks = False
    print 'Did not find GDL library.'

class MainWindow(Window):

    builder_file = "./ui/main.builder"
    robjects = dict()
    active_robject = None
    active_output = None

    #Variable name of column in dataview
    active_column = None
    #Numerical index of row in dataview
    active_row = None

    active_threads = rsession.ThreadHandler()

    saved = False
    saved_to = None
    dataview = None

    child_windows = []

    #-----------------------------
    # Window Methods
    #-----------------------------

    def __init__(self,files=[]):
        global __name__
        global using_docks
        self.using_docks = using_docks

        self.using_docks = False

        self.window  = self.builder.get_object( "main" )
        if self.using_docks:
            self.dock = gdl.Dock()
            layout = gdl.DockLayout(self.dock)
            self.right_dock.add(self.dock)
            self.right_dock.show_all()

            objects = gdl.DockItem("objects", "Objects", None,gdl.DOCK_ITEM_BEH_NORMAL | gdl.DOCK_ITEM_BEH_CANT_ICONIFY)
            objects.add(self.object_sidebar)
            self.dock.add_item(objects, gdl.DOCK_TOP)
            objects.dock_to(None, gdl.DOCK_TOP, -1)
            objects.show_all()
        else:
            self.right_dock.add(self.object_sidebar)


        self.window.set_title(__name__)
        self.builder.connect_signals( self )
        self.window.connect('delete-event', self.destroy)

        #Use small icons
        toolbar = self.builder.get_object("main_toolbar")
        toolbar.set_icon_size(gtk.ICON_SIZE_MENU)

        #Drag and Drop
        dnd_list = [ ( 'text/uri-list', 0, 80 ) ]
        self.window.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
                        gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
                        dnd_list,gtk.gdk.ACTION_COPY)
        self.window.connect('drag_data_received', self.on_drag_data_received)

        #self.window.maximize()

        #Resize the main window so that that the object pane fits nicely
        self.builder.get_object("main_pane").set_position(self.window.get_size()[1]+60)

        #Monospace, otherwise output looks awful
        summary = self.builder.get_object('summaryview')
        font_desc = pango.FontDescription('monospace')
        summary.modify_font(font_desc)

        self.handle_dataview()
        self.build_object_list()

        if config.__devel__ == True:
            self.render_dataframe(numpy.random.rand(25,4) ,name='devel',rownames=xrange(0,25))

        #Load any files passed with the CLI
        for file in files:
            self.import_datafile(file)

        self.window.show()

    def destroy(self,event,*args):
        if not self.saved:
            if wrappers.yesNoDialog("Are you sure you want to close without saving."):
                self.shutdown_cleanly()
                gtk.main_quit()
                sys.exit(0)
            else:
                return True
        else:
            self.shutdown_cleanly()
            gtk.main_quit()

    def resize_object_pane(self,resized_window,*args):
        if self.using_docks:
            return
        #Force the object pane to its minimum size so its doesn't disappear when we resize
        self.main_pane.set_position(5000)

    #Drag and drop files, taken verbatim from the PyGTK FAQ
    def on_drag_data_received(self,widget, context, x, y, selection, target_type, timestamp):
        uri = selection.data.strip('\r\n\x00')
        uri_splitted = uri.split() # we may have more than one file dropped
        for uri in uri_splitted:
            path = get_path_from_url(uri)
            if os.path.isfile(path): # is it file?
                self.import_datafile(uri)

    def toggle_object_toolbar(self,event):
        toggle_visible(self.builder.get_object('object_sidebar'))

    #-----------------------------
    # Data Handling Methods
    #-----------------------------

    def require_data(f):
        '''A decorator that requires that a dataframe or timeseries be active before executing method'''
        def wrapper(*args,**kwargs):
            self = args[0]
            #Get the self object from the method
            if (self.active_robject.type == 'Data Frame') or (self.active_robject.type == 'Time Series'):
                f(*args,**kwargs)
            else:
                error("The current object's datatype does not permit the operation you selected.\n\nPlease select either a Data Frame or Time Series object.")
        return wrapper

    def require_dataframe(f):
        '''A decorator that requires that a dataframe be active before executing method'''
        def wrapper(*args,**kwargs):
            self = args[0]
            #Get the self object from the method
            if (self.active_robject.type == 'Data Frame'):
                f(*args,**kwargs)
            else:
                error("The current object's datatype does not permit the operation you selected.\n\nPlease select a Data Frame.")
        return wrapper

    def require_timeseries(f):
        '''A decorator that requires that a timeseries be active before executing method'''
        def wrapper(*args,**kwargs):
            self = args[0]
            #Get the self object from the method
            if (self.active_robject.type == 'Time Series'):
                f(*args,**kwargs)
            else:
                error("The current object's datatype does not permit the operation you selected.\n\nPlease select a Time Series object.")
        return wrapper

    def unsaved(f):
        '''Decorates functions whose execution will alter the workspace, and result in changes that can be saved'''
        def wrapper(*args,**kwargs):
            self = args[0]
            self.saved = False
            self.builder.get_object("Save").set_sensitive(True)
            f(*args,**kwargs)
        return wrapper

    def handle_dataview(self,inputdata=[],columns=[],rownames=None,editable=False):
        '''Handle making the dataview, this shouldn't be called explicitly'''

        if inputdata == []:
            return

        dataview = self.builder.get_object("dataview")
        self.clear_dataview()
        dataview.set_model(model=None)

        headers = columns.keys()
        types = columns.values()

        #If we have rownames for the dataframe add them in, otherwise hide
        if rownames != None:
            view = self.builder.get_object("rownames")
            store = gtk.ListStore(str)
            col = gtk.TreeViewColumn("(Row ID)\n")
            col.set_property('clickable', False)
            view.append_column(col)
            cell = gtk.CellRendererText()
            cell.set_property('font-desc', pango.FontDescription('sans 8'))
            col.pack_start(cell)
            col.add_attribute(cell,'text',0)
            for row in rownames:
                store.append([row])
            view.set_model(store)
            self.builder.get_object("rownames").show()
        else:
            self.builder.get_object("rownames").hide()

        #Construct the list store, and translate the rtypes into python types
        #for example 'double' --> float which is then applied to ListStore([float])
        ptypes = map(rsession.translate_types,types)
        datastore = apply(gtk.ListStore,ptypes)

        self.dataview = datasheet.Datasheet(dataview,datastore,self,editable=editable)
        self.dataview.set_columns(headers,types=types)

        for i in inputdata:
            self.dataview.add_data([i])

        dataview.set_model(datastore)

    def clear_dataview(self):
        try:
            dataview = self.builder.get_object("dataview")
            for column in dataview.get_columns():
                dataview.remove_column(column)

            rownames = self.builder.get_object("rownames")
            for column in rownames.get_columns():
                rownames.remove_column(column)
        except AttributeError:
            pass

        dataview.set_model(model=None)

    # The render_ methods  are the bread and butter of this application, these are the only functions
    # that should be called explicitely from other classes since they safely handle displaying any
    # supported object from the REnviroment
    def render_dataframe(self,data,columns=None,name=None,rownames=None):
        '''Take a numpy matrix and bring it into the Python enviroment, also add it to the r session'''
        if not columns:
            columns = dict()
            #Map the columns to anoymous V1,V2,V3... variables
            for i in range(data.shape[1]):
                columns['V%s' % (i+1)] = float
        if not name:
            inc = 0
            for unmes in self.robjects.keys():
                if 'unnamed' in unmes:
                    inc += 1
            name = 'unnamed' + str(inc+1)

        #Set the main title to include the open file name.
        self.window.set_title(__name__ + ' - ' + name)

        dataframe = rsession.dataframe(data,columns,label=name,rownames=rownames)

        self.add_r_object(dataframe,name)
        self.set_active_robject(dataframe)
        self.handle_dataview(data,columns,rownames=rownames,editable=True)

    def render_timeseries(self,data,label=None,start=None,end=None,frequency=None,deltat=None,times=None):
        '''Time series are handled just like dataframes except we allow for options on frequency/start/end'''

        #This only works for ts, not mts at the moment
        ptype = rsession.typeof(data[0])
        columns = {'V1':rsession.translate_types(ptype)}

        if not label:
            inc = 0
            for unmes in self.robjects.keys():
                if 'unnamed' in unmes:
                    inc += 1
            name = 'unnamed' + str(inc+1)

        timeseries = rsession.timeseries(data,label=label,start=start,end=end,frequency=frequency,deltat=deltat)
        rownames = timeseries.rownames

        self.add_r_object(timeseries,label)
        self.set_active_robject(timeseries)
        self.handle_dataview(data,columns,rownames=rownames,editable=True)

    def render_linear_model(self,model,label=None):
        if not label:
            inc = 0
            for unmes in self.robjects.keys():
                if 'unnamed' in unmes:
                    inc += 1
            name = 'unnamed' + str(inc+1)

        linear_model = rsession.linear_model(model,label=label)
        self.add_r_object(linear_model,label)
        self.set_active_robject(linear_model)
        self.output(linear_model.object,title=label)

    def render_description(self,object,label=None):
        description = rsession.description(object,label=label)
        self.add_r_object(description,label)
        self.set_active_robject(description)
        self.output(object,title=label)

    def set_active_robject(self,object):
        #If we have a dataframe
        if object.outputsTo == "frame":
            self.active_robject = object
            self.handle_dataview(object.rawdata,object.columns,rownames=object.rownames)
            if prefs.get_pref('auto_switch'):
                self.builder.get_object('main_tabview').set_current_page(0)
            for window in self.child_windows:
                window.active_r_object = object
                window.show_variables(object)
        elif object.outputsTo == "output":
            self.active_robject = object
            self.active_output = object
            self.output(object.text)
            if prefs.get_pref('auto_switch'):
                self.builder.get_object('main_tabview').set_current_page(1)
            self.clear_dataview()
        elif object.outputsTo == 'graphics':
            pass
        else:
            error('Cannot render object.')

    def refresh_dataframe(self):
        '''Copy changes from the TreeView into the Numpy and R objects'''
        label = self.active_robject.label

        #Write changes to the numpy array
        self.active_robject.rawdata = self.get_changes()

        #Write changes to the r object as well
        rsession.env[label]=self.active_robject.refresh()

        #Tell any child windows to update their copy of the data
        for window in self.child_windows:
            window.active_r_object = self.active_robject
            window.show_variables(self.active_robject)

    def output(self,text,title=None):
        '''Output text to the output tab'''
        text = str(text)
        if title:
            text = '%s\n' % title + text
        summary = self.builder.get_object('summaryview')
        summary.get_buffer().set_text(text)
        if prefs.get_pref('auto_switch'):
            self.builder.get_object('main_tabview').set_current_page(1)

    def import_datafile(self,uri):
        '''Take a file and try to extract data from it using the lib.readfiles'''
        path = get_path_from_url(uri)
        if not os.path.isfile(path):
            return

        filename = os.path.split(uri)[1]

        #There are a lot of things that can go wrong here... R isn't friendly with external files
        try:
            (columns, data, rows) = readfiles.readfile(uri)
            dataframe = rsession.dataframe(data,columns,filename,rownames=rows)
            self.add_r_object(dataframe,filename)
            self.set_active_robject(dataframe)
        except:
            error("Could not read file: %s" % uri)
            return

    #-----------------------------
    # Menu Items
    #-----------------------------

    def new_workspace(self,event):
        if not wrappers.yesNoDialog('Are you sure you want to create a new workspace?'):
            return
        #Delete everything in R
        rsession.rm(rsession.ls())
        #Delete everything in Python
        self.clear_dataview()
        self.active_robject = None
        self.robjects.clear()
        self.refresh_object_list()

    def open_workspace(self,event):
        opendialog = OpenFile(self,filetypes=['rdata'],include_wildcard=True)
        uri,extension = opendialog.get_filename()
        path = get_path_from_url(uri)
        if not os.path.isfile(path):
            return
        rsession.r['load'](path)
        self.sync_with_r()

    def save_workspace(self,event):
        #If we've already run Save As... use that path
        if self.saved_to:
            path = self.saved_to
            rsession.r['save.image'](path)
            self.saved = True
            self.builder.get_object('Save').set_sensitive(False)
        else:
            self.save_workspace_as(event)

    def save_workspace_as(self,event):
        savedialog = SaveFile(self,filetypes=['rdata'])
        uri,extension = savedialog.get_filename()
        path = get_path_from_url(uri)

        #Store the saved path so the user can Save to it
        self.saved = True
        self.saved_to = path
        rsession.r['save.image'](path)
        self.builder.get_object('Save').set_sensitive(False)

    def import_data(self,event):
        opendialog = OpenFile(self,filetypes=['csv','xls'],include_wildcard=True)
        uri,extension = opendialog.get_filename()
        self.import_datafile(uri)

    @unsaved
    def sampledata(self,event):
        sampledata.SampleData(self)

    @unsaved
    def subset(self,event):
        condition = variable_prompt.VariablePrompt(['Condition(s):']).get_inputs()[0]
        rsession.env['subset %s' % (self.active_robject.label)] = rsession.r('subset(%s,%s)' % (self.active_robject.label,condition))
        self.sync_with_r()

    @unsaved
    def blankdata(self,event):
        prompt = variable_prompt.VariablePrompt(['Rows','Columns','Name'])
        values = prompt.get_inputs()
        if values:
            rows,cols,name = int(values[0]),int(values[1]),values[2]
            self.render_dataframe(numpy.zeros((rows,cols)),name=name)

    def about(self,event):
        about.About()

    def preferences(self,event):
        prefs.Preferences()

    @unsaved
    def generate_random(self,event):
        assistant = randomgen.RandomGen(self)

    def transform(self,event):
        cols = self.active_robject.columns.keys()
        transforms = zip(cols,variable_prompt.VariablePrompt(cols).get_inputs(allow_empty=True))
        try:
            args = rdict()
            argument_string = ''
            for col,transform in transforms:
                if col and transform:
                    argument_string += ',%s=%s' % (col,transform)
            print argument_string
            label = self.active_robject.label
            obj = rsession.env[label]
            transformed = rsession.r('transform(%s %s)' % (label,argument_string))
            #transformed = rsession.r['transform'](obj,args)
        except:
            error('Transformations were not well formed')
            return
        rsession.env[label] = transformed
        self.sync_with_r()

    def export_latex(self,event):
        try:
            rsession.r('library(xtable)')
            rprint = rsession.r['print']
            xtable = rsession.r['xtable']
            table = rsession.r['table']

            activetab = self.builder.get_object('main_tabview').get_current_page()

            #Data Tab
            if activetab == 0:
                if not self.active_robject:
                    error('No active dataframe.')
                    return
                object = self.active_robject.object
                label = self.active_robject.label
                text = str(xtable(object,caption=label))
                TextOutput(text)
            #Output Tab
            elif activetab == 1:
                if not self.active_output:
                    error('No active output.')
                    return
                object = self.active_output.object
                label = self.active_output.label
                if not label:
                    label = rsession.null
                if self.active_output.tabelize: 
                    text = str(xtable(table(object),caption=label))
                else:
                    text = str(xtable(object,caption=label))
                TextOutput(text)
            #Console Tab
            elif activetab == 2:
                console = self.builder.get_object('consoleview').get_buffer()
                lower,upper = console.get_bounds()
                text = console.get_text(lower,upper)
                TextOutput('\\begin{verbatim}\n' + text + '\n\end{verbatim}')
        except:
            error("Could not load the xtable library.")

    def export_csv(self,event):
        savedialog = SaveFile(self,filetypes=['csv'])
        uri,extension = savedialog.get_filename()
        path = get_path_from_url(uri)

        args = rdict()
        #Eventually we'll want to make this a bit more sophisticated
        if not self.active_robject.rownames:
            args['row.names'] = False
        rsession.r['write.csv'](self.active_robject.object,path,**args)

    @require_dataframe
    def linear_regression(self,event):
        stat_tests.linear_regression(self,self.active_robject)

    @require_dataframe
    def nonlinear_regression(self,event):
        stat_tests.nonlinear_regression(self,self.active_robject)

    @require_dataframe
    def polynomial_regression(self,event):
        stat_tests.polynomial_regression(self,self.active_robject)

    @require_dataframe
    def local_regression(self,event):
        stat_tests.local_regression(self,self.active_robject)

    #We use sapply a lot, it applies a R function each column
    @require_data
    def mean(self,event):
        mean = rsession.r['mean']
        #o = rsession.sapply(self.active_robject.object,mean)
        o = mean(self.active_robject.object)
        label = 'Means: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def median(self,event):
        median = rsession.r['median']
        o = rsession.sapply(self.active_robject.object,median)
        label = 'Medians: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def range(self,event):
        range = rsession.r['range']
        o = rsession.sapply(self.active_robject.object,range)
        label = 'Ranges: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def variance(self,event):
        var = rsession.r['var']
        o = var(self.active_robject.object)
        label = 'Ranges: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def sd(self,event):
        sd = rsession.r['sd']
        o = sd(self.active_robject.object)
        label = 'Standard Deviations: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def quantile(self,event):
        quantile = rsession.r['quantile']
        o = rsession.sapply(self.active_robject.object,quantile)
        label = 'Ranges: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def max(self,event):
        max = rsession.r['max']
        o = rsession.sapply(self.active_robject.object,max)
        label = 'Maximums: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def min(self,event):
        min = rsession.r['min']
        o = rsession.sapply(self.active_robject.object,min)
        label = 'Minimums: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def cor(self,event):
        cor = rsession.r['cor']
        o = cor(self.active_robject.object)
        label = 'Correlation Coefficents: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_dataframe
    def cortest(self,event):
        stat_tests.cortest(self,self.active_robject)

    @require_dataframe
    def mcnemar(self,event):
        stat_tests.mcnemar(self,self.active_robject)

    @require_data
    def cov(self,event):
        cov = rsession.r['cov']
        o = cov(self.active_robject.object)
        label = 'Covariance: ' + self.active_robject.label
        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_dataframe
    def anova(self,event):
        stat_tests.anova(self,self.active_robject)

    @require_dataframe
    def freqtable(self,event):
        condition = variable_prompt.VariablePrompt(['Condition(s):']).get_inputs()
        #This is dirty but ro.RFormula will not parse
        try:
            filter = rsession.r('with(%s,table(%s))' % (self.active_robject.label,condition[0]))
        except:
            error('Formula is not valid. \n Enter conditions seperated by commas. Ex: V1>3,V4<1')
            return
        self.output(filter,title='Frequency Table: ' + condition[0])
        self.active_output = rsession.description(filter,tabelize=False)

    @require_dataframe
    def ttest(self,event):
        stat_tests.ttest(self,self.active_robject)

    @require_dataframe
    def ftable(self,event):
        '''# 3-Way Frequency Table
            mytable <- xtabs(~A+B+c, data=mydata)
            ftable(mytable) # print table
            summary(mytable) # chi-square test of indepedence'''
        pass

    @require_dataframe
    def chisq(self,event):
        stat_tests.chisq(self,self.active_robject)

    @require_data
    def summary(self,event):
        summary_object = rsession.summary(self.active_robject.object)
        self.active_output = rsession.description(summary_object)
        self.output(summary_object)

    @require_data
    def fivenum(self,event):
        cov = rsession.r['fivenum']
        o = cov(self.active_robject.object)
        label = 'Tukey Five-Number Summary: ' + self.active_robject.label

        self.active_output = rsession.description(o,label=label,tabelize=True)
        self.output(o,title=label)

    @require_data
    def scatterplot(self,event):
        if self.active_robject.type == 'Time Series':
            info('Scatter Plots of time series are not implemented for (yet).')
            return
        object = self.active_robject
        ScatterPlot(self,object)

    @require_dataframe
    def barplot(self,event):
        object = self.active_robject
        BarPlot(self,object)

    @require_dataframe
    def boxplot(self,event):
        object = self.active_robject
        BoxPlot(self,object)

    @require_dataframe
    def histogram(self,event):
        object = self.active_robject
        Histogram(self,object)

    @require_dataframe
    def pieplot(self,event):
        object = self.active_robject
        PiePlot(self,object)

    @require_dataframe
    def mscatter(self,event):
        object = self.active_robject
        MultiScatter(self,object)

    @require_dataframe
    def qqplot(self,event):
        object = self.active_robject
        QQPlot(self,object)

    #There seems to be no way to capture the output of stem plot
    #@require_dataframe
    #def stemplot(self,event):
    #    stem = rsession.r['stem']
    #    o = rsession.sapply(self.active_robject.object,stem)
    #    label = 'Stem Plot: ' + self.active_robject.label
    #    #self.active_output = rsession.description(o,label=label,tabelize=False)
    #    self.output(o,title=label)

    #Maybe in the next release
    #@require_data
    #def mosaicplot(self,event):
    #    object = self.active_robject
    #    pass

    #-----------------------------
    # Datasheet
    #-----------------------------

    #TODO: This doesn't work with reordering.
    def col_contextmenu(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)

            if pthinfo is not None:
                path, col, cellx, celly = pthinfo

            #This is a filthy hack, but there is no get_index() for TreeViewColumn
            for i,j in enumerate(treeview.get_columns()):
                if j == col:
                    index = i

            self.active_column = self.dataview.get_column_from_index(index)
            self.active_row = path[0]

            self.popup()
            treeview.grab_focus()
            treeview.set_cursor( path, col, 0)
            return True

    def popup(self):
        context = self.builder.get_object( "colmenu" )
        context.popup(None,None,None,0,0)
        context.show()

    def context_mean(self,*args):
        object=self.active_robject.object
        column = object.r[self.active_column]
        output = rsession.r['mean'](column)
        self.output(output)

    def context_median(self,*args):
        object=self.active_robject.object
        column = object.r[self.active_column]
        output = rsession.r['median'](column)
        self.output(output)

    def context_variance(self,*args):
        object=self.active_robject.object
        column = object.r[self.active_column]
        output = rsession.r['var'](column)
        self.output(output)

    def context_sd(self,*args):
        object=self.active_robject.object
        column = object.r[self.active_column]
        output = rsession.r['sd'](column)
        self.output(output)

    def context_rename(self,*args):
        if self.active_robject.type == 'Time Series':
            return
        old_label = self.active_column
        new_label = variable_prompt.VariablePrompt(['New Label']).get_inputs()[0]
        columns = self.active_robject.columns
        columns = dict_replace_key(columns,old_label,new_label)
        self.active_robject.columns = columns
        rsession.env[self.active_robject.label] = self.active_robject.refresh()
        self.sync_with_r()

    def context_delrow(self,*args):
        label = self.active_robject.label
        index = self.active_row
        self.active_robject.rawdata = numpy.delete(self.active_robject.rawdata,index,axis=0)
        rsession.env[label]=self.active_robject.refresh()
        self.sync_with_r()

    def context_delcol(self,*args):
        #Its much easier to resolve this on the R side, rather than using numpy
        rsession.r('%s = transform(%s,%s)' % (self.active_robject.label, self.active_robject.label,self.active_column+'=NULL'))
        self.sync_with_r()

    def get_changes(self):
        '''fetches the dataview with all user changes in it'''
        return self.dataview.toArray()

    #-----------------------------
    # Object Menu
    #-----------------------------

    def selectobject(self, treeview, event):
        if event.button == 1:
            treeselection = treeview.get_selection()
            model, iter = treeselection.get_selected()

            #If nothing is selected don't bother
            if not iter:
                return

            selected = self.objectstore.get_value(iter, 1)
            parent = self.objectstore.iter_parent(iter)
            if parent:
                parent_label = self.objectstore.get_value(parent, 1)
                parent_object = self.robjects[parent_label]

            #If we already have the object open don't bother
            if parent == self.active_robject:
                return

            #If we're dealing with a top-level object
            if not parent:
                object = self.robjects[selected]
                if object == self.active_robject:
                    return
                self.set_active_robject(object)

            #If we're dealing with a child object
            else:
                #Instructions for the different object type's children

                if parent_object.type == 'Data Frame':
                    #TODO: If the type of the column is a FACTOR use a different icon
                    iter = self.objectstore.iter_parent(iter)
                    selected = self.objectstore.get_value(iter, 1)
                    object = self.robjects[selected]
                    self.set_active_robject(object)

                if parent_object.type =='Linear Model':
                    #TODO: I'd like to eventually get these to render as data
                    #if selected == 'Residuals':
                    #    resids = parent_object.residuals
                    #    self.handle_dataview(resids,{'Residual':float})
                    #    self.builder.get_object('main_tabview').set_current_page(0)
                    if selected == 'Residuals':
                        resids = parent_object.residuals
                        self.output(str(resids),title='Residuals of '+parent_label)
                    if selected == 'Fitted Values':
                        resids = parent_object.fitted
                        self.output(str(resids),title='Fitted Values of '+parent_label)
                    if selected == 'Coefficents':
                        resids = parent_object.coefs
                        self.output(str(resids),title='Coefficents of '+parent_label)
                    if selected == 'Summary':
                        summary = rsession.r['summary'](parent_object.object)
                        self.output(str(summary),title='Coefficents of '+parent_label)

    def build_object_list(self):
        '''This builds the widget to house the object list'''
        self.objectview = self.builder.get_object("objectview")
        treeselection = self.objectview.get_selection()
        treeselection.set_mode(gtk.SELECTION_SINGLE)
        self.objectstore = gtk.TreeStore(gtk.gdk.Pixbuf,str)

        #Data type icons
        col = gtk.TreeViewColumn()
        self.objectview.append_column(col)
        cell = gtk.CellRendererPixbuf()
        col.pack_start(cell)
        col.add_attribute(cell,'pixbuf',0)

        #Data labels
        col = gtk.TreeViewColumn("Objects")
        self.objectview.append_column(col)
        cell = gtk.CellRendererText()
        col.pack_start(cell)
        col.add_attribute(cell,'text',1)

        self.objectview.set_model(self.objectstore)

    def refresh_object_list(self,*args):
        self.objectstore.clear()
        column_icon = gtk.gdk.pixbuf_new_from_file('./ui/icons/column.png')
        time_icon = gtk.gdk.pixbuf_new_from_file('./ui/icons/time.png')
        description_icon = gtk.gdk.pixbuf_new_from_file('./ui/icons/description.png')

        for _label,object in self.robjects.iteritems():
            icon = gtk.gdk.pixbuf_new_from_file(object.icon)
            parent = self.objectstore.append(None,[icon,_label])

            if object.type == 'Data Frame':
                for column in object.columns.keys():
                    self.objectstore.append(parent,[column_icon,column])

            if object.type == 'Time Series':
                for column in object.columns.keys():
                    self.objectstore.append(parent,[icon,column])
                self.objectstore.append(parent,[time_icon,'(Time)'])

            if object.type == 'Description':
                pass

            if object.type == 'Linear Model':
                self.objectstore.append(parent,[description_icon,'Summary'])
                self.objectstore.append(parent,[description_icon,'Coefficents'])
                self.objectstore.append(parent,[description_icon,'Fitted Values'])
                self.objectstore.append(parent,[description_icon,'Residuals'])


    @unsaved
    @handle_errors
    def add_r_object(self,object,label):
        '''Take an rsession.robject and add it into the REnviroment'''
        #This is essentially the reverse of render_someobject which imports
        # a data.frame from the R side, this takes a rsession.dataframe and
        #creates a data.frame from it

        self.robjects[label] = object
        env = rsession.env

        env[label]=object.object
        self.refresh_object_list()

    @unsaved
    @handle_errors
    def delete_r_object(self,object):
        '''Remove a object from the REnviroment'''
        treeview = self.builder.get_object("objectview")
        selected = treeview.get_selection().get_selected_rows()
        index = selected[1][0]
        label = selected[0][index][1]

        if self.active_robject.label == label:
            self.clear_dataview()

        del self.robjects[label]
        rsession.rm(label)
        self.refresh_object_list()

    @unsaved
    @handle_errors
    def rename_r_object(self,event):
        prompt = variable_prompt.VariablePrompt(['New Label'])

        if not prompt.get_inputs():
            return

        new_label = prompt.get_inputs()[0]
        treeview = self.builder.get_object("objectview")
        selected = treeview.get_selection().get_selected_rows()
        index = selected[1][0]
        label = selected[0][index][1]

        if self.active_robject.label == label:
            self.clear_dataview()

        object = self.robjects[label]

        #Create the new named object
        self.add_r_object(object,label=new_label)

        #Delete the old object
        del self.robjects[label]
        rsession.rm(label)

        self.refresh_object_list()
        self.set_active_robject(object)

    @unsaved
    @handle_errors
    def duplicate_r_object(self,event):
        prompt = variable_prompt.VariablePrompt(['New Label'])

        if not prompt.get_inputs():
            return

        new_label = prompt.get_inputs()[0]

        treeview = self.builder.get_object("objectview")
        selected = treeview.get_selection().get_selected_rows()
        index = selected[1][0]
        label = selected[0][index][1]

        if new_label == label:
            error('Duplicate label is identical to original label')
            return

        if self.active_robject.label == label:
            self.clear_dataview()

        object = self.robjects[label]

        #Create the new named object
        self.add_r_object(object,label=new_label)

        self.refresh_object_list()
        self.set_active_robject(object)

    #-----------------------------
    # Console
    #-----------------------------

    def execute_command(self,event):
        entry = self.builder.get_object("command_entry")
        cmd = entry.get_text()

        console = self.builder.get_object('consoleview')
        font_desc = pango.FontDescription('monospace')
        console.modify_font(font_desc)

        try:
            def append_text(console,text):
                buf = console.get_buffer()
                buf.insert(buf.get_end_iter(),str(text))
                mark = buf.create_mark("end", buf.get_end_iter(), False)
            buf = console.get_buffer()
            #Make sure the user doesn't enter commands which causes rpy2 to crash
            if 'plot' in cmd:
                error("Please note that X11 interfaces need to be refreshed and this is not yet implemented.")
            elif 'quit' in cmd and config.__devel__:
                error('To avoid data loss please shut down via File->Quit.')
                return
            elif 'help' in cmd and 'htmlhelp' not in cmd:
                error('Use of a pager can cause issues... we reccomend you use\n help(topic,htmlhelp=TRUE)')
                return
            #Internal commands, mostly for debugging
            elif '!clear' in cmd:
                buf.set_text('')
                return
            elif '!cmds' in cmd:
                buf.set_text('Available ' + config.__name__ + ' commands:\n !clear \n !cmds \n !sync')
                return
            #TODO: We can replace this with a lot smarter command just str split at = and strip whitespace off
            #to find the variable we might need to sync
            elif '=' in cmd:
                buf.insert(buf.get_end_iter(),str(rsession.ro.r(str(cmd)))+'\n')
                self.sync_with_r()
                return
            elif '!sync' in cmd:
                #Force python and r to sync ojbects
                self.sync_with_r()
                return
            elif '!debug' in cmd:
                append_text(console,'Active Object:' + self.active_robject.label + '\n')
                append_text(console,'Objects:\n')
                for i in self.robjects.values():
                    append_text(console,str([i,type(i),i.label,i.type])+'\n')

                append_text(console,'Threads:\n')
                for i in self.active_threads.iter_shared():
                    append_text(console,str([i,i.halt])+'\n')
                #Spawn an interactive shell
                import code; code.interact(local=locals());
                return
            #execute the str entered as r code, errors cause the indicator to change
            buf.insert(buf.get_end_iter(),'>' + cmd + '\n' + str(rsession.ro.r(str(cmd)))+'\n')
            mark = buf.create_mark("end", buf.get_end_iter(), False)
            console.scroll_to_mark(mark, 0.05, True, 0.0, 1.0)
            entry.set_property('primary_icon_stock','Execute')
            entry.set_property('primary_icon_stock','gtk-yes')
            entry.set_property('primary_icon_tooltip_text','No Errors')
        except rsession.rinterface.RRuntimeError,RError:
            entry.set_property('primary_icon_stock','gtk-no')
            entry.set_property('primary_icon_tooltip_text',RError)
    @unsaved
    #@handle_errors
    def sync_with_r(self):
        '''Query the rsession for all objects and try to recreate using the rsession wrapper objects'''
        for obj in rsession.r.ls():
            #try:
                pyobj = rsession.ro.globalEnv.get(str(obj))
                typeof = rsession.r['class'](pyobj)[0]
                #There are also multivariable time series (is_mts) that we should worry about
                #Converting arrays to dataframes flattens the array
                if typeof == 'table':
                    info('FYI, the array object you selected is being imported as a flattened dataframe.')
                    pyobj = rsession.df(pyobj)

                if typeof == 'ts':
                    #Strip all the data needed to recreate the object
                    start = rsession.r['start'](pyobj)
                    end = rsession.r['end'](pyobj)
                    frequency = rsession.r['frequency'](pyobj)
                    times = rsession.r['time'](pyobj)
                    deltat = rsession.r['deltat'](pyobj)
                    data = numpy.array(pyobj).T
                    label = str(obj)
                    self.render_timeseries(data,label=label,start=start,end=end,frequency=frequency,deltat=deltat)

                if typeof == 'data.frame':
                    data = numpy.array(pyobj).T
                    rownames=pyobj.rownames()
                    columns = odict()
                    for col,dat in zip(pyobj.colnames(),pyobj):
                        ptype = rsession.typeof(dat)
                        columns[col] = rsession.translate_types(ptype)
                    self.render_dataframe(data,columns,name=str(obj),rownames=rownames)

                if typeof == 'htest':
                    self.render_description(pyobj,str(obj))

                if typeof == 'lm':
                    self.render_linear_model(pyobj,'Linear Model')

                if typeof == 'nls':
                    self.render_linear_model(pyobj,'Nonlinear Model')

                #Vectors
                if typeof == 'numeric':
                    #Cast into dataframe
                    pyobj = rsession.df(pyobj)
                    data = numpy.array(pyobj).T
                    rownames=pyobj.rownames()
                    columns = odict()
                    for col,dat in zip(pyobj.colnames(),pyobj):
                        ptype = rsession.typeof(dat)
                        columns[col] = rsession.translate_types(ptype)
                    self.render_dataframe(data,columns,name=str(obj),rownames=rownames)
                if config.__devel__:
                    print('Tring to import to workspace. \n'+str(type(pyobj)) + '\n')
            #except Exception,Error:
            #    if config.__devel__:
            #        print('Could not cast:\n'+ str(Error) + '\n')
    def shutdown_cleanly(self):
        '''If the user CTRL-Cs, make sure the threads die and graphics get turned off'''
        #iterate over the shared state of ThreadHandler to fetch all threads and kill them
        for thread in self.active_threads.iter_shared():
            thread.halt = True
        rsession.r('graphics.off()')
