# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

import rpy2.robjects as robjects
from rpy2 import rinterface
import time
import numpy

from ui import prefs
import threading
import thread

ri = rinterface
ro = robjects
r = robjects.r
env = robjects.r.globalenv()

#R Convience Wrappers
summary = robjects.r.summary
plot = robjects.r.plot
ls = robjects.r.ls
rm = robjects.r.rm
png = r.png
svg = r.svg
postscript = r.postscript
pdf = r.pdf
devoff = r['dev.off']
devcur = r['dev.cur']
devlist = r['dev.list']
X11 = r['X11']
typeof = lambda obj: (r['typeof'](obj))[0]
null = r['as.null']()

#TODO: We should convert these so that they actually return booleans, aka
# is_ts = lambda obj: r['is.ts'](obj)[0]
is_ts = r['is.ts']
is_array = r['is.array']
is_null = r['is.null']
#Using 'time' messes with the threads
times = r['time']
sapply = r['sapply']
df = r['data.frame']
library = r['library']

#Initialize the R Interface
rinterface.initr()

gdata_is_available = False
xtable_is_available = False
nlstools_is_available = False

#Check what libraries we have installed
try:
    library('gdata')
    gdata_is_available = True
except rinterface.RRuntimeError,RError:
    print('Could not load the gdata library, importing of Excel spreadsheets is disabled.')

try:
    library('xtable')
    xtable_is_available = True
except rinterface.RRuntimeError,RError:
    print('Could not load the xtable library, exporting LaTeX is disabled.')

try:
    library('nlstools')
    nlstools_is_available = True
except rinterface.RRuntimeError,RError:
    print('Could not load the nlstools library, summary of nls is disabled.')

class rdict(dict):
    '''A dictionary type that does not permit None types or empty strings in values'''
    def __setitem__(self, key, value):
        if value != None and value != '':
            #Fetch the parent class (dict) and invoke __setitem__ just like normal but with the
            #condition that we don't allow empty values
            super(rdict, self).__setitem__(key, value)

def arguments_to_string(d):
    '''Take a dictionary of arguments and return a string of comma seperated key,value pairs'''

    #If we end using the low-level iterface (which we do too much), then we need a way of
    #passing arguments
    argument_str = ''
    for key,value in d.iteritems():
        if type(value) is str:
            value = '"' + str(value) + '"'
        #R likes capitalized logicals
        if type(value) is bool:
            value = str(value).upper()
        argument_str += ',' + str(key)+'='+str(value)
    return argument_str

def translate_types(type, reverse=False):
    '''Translate between R types and Python types and vise versa, reverse=False implies translation to python'''

    #r -> python
    if not reverse:
        if type == 'double':
            return float
        elif type == 'string':
            return str
        elif type == 'integer':
            return int
        elif type == 'character':
            return str
        elif type == 'logical':
            return bool
        elif type == int:
            return type
        elif type == float:
            return type
        elif type == str:
            return type
        else:
            error('Cannot cast')
            return
    '''Translate between R types and Python types'''
    #python -> r
    if reverse:
        if type == int:
            return 'integer'
        elif type == float:
            return 'double'
        elif type == str:
            return 'character'
        elif type == bool:
            return 'logical'
        elif type == 'double':
            return 'double'
        elif type == 'character':
            return 'character'
        elif type == 'integer':
            return 'integer'
        else:
            error('Cannot cast')

def translate_to_vector(column):
    '''Take a vanilla list or numpy column array and return the "equivelent" r vector form'''

    if (type(column) is not numpy.ndarray) and (type(column) is not list):
        print('Cannot translate non-numpy or list object to R Vector')
        return

    if type(column) is list:
        return ro.FloatVector(column)
    if column.dtype is numpy.dtype(int):
        return ro.IntVector(column)
    elif column.dtype is numpy.dtype(float):
        return ro.FloatVector(column)
    elif column.dtype is numpy.dtype(bool):
        return ro.BoolVector(column)
    elif column.dtype is numpy.dtype(str):
        return ro.StrVector(column)
    else:
        print 'Mismatched (or strange) datatype in numpy array'
        return

def column_extractor(data,output='rvector'):
    '''Take any object (R Dataframe, List of Lists, Numpy Array, Python Array)
    and return an iterator on its columns which yields either a numpy array,
    RVector or a vanilla list

    output='rvector'|'list'|'numpy'
    '''

    if type(data) == type(r['data.frame']):
        for i in range(data.ncol()):
            column = numpy.array(data.rx2(i))
            yield translate_to_vector(column)

    elif type(data) is list:
        for i in range(len(data[0])):
            column = lambda n: [x[n] for x in data]
            yield robjects.FloatVector(column(i))

    elif type(data) is numpy.ndarray:
        #Check to see if we have a column
        if len(data.shape)<2:
            yield robjects.FloatVector(data)
        else:
            for i in range(data.shape[1]):
                column = data[:,i]
                yield robjects.FloatVector(column)

#This is a 'Borg' design pattern, all items appended get stored
#in the master shared state. We'll use this for threads so that 
#we can kill every thread from the main thread
class ThreadHandler(list):
    #Shared state
    shared = []

    def append(self,value):
        super(ThreadHandler,self).append(value)
        self.shared.append(value)

    def remove(self,value):
        super(ThreadHandler,self).remove(value)
        self.shared.remove(value)

    def get_shared(self):
        return self.shared

    def iter_shared(self):
        for item in self.shared:
            yield item

class RPlotThread( threading.Thread ):
    halt = False
    args = {}
    data = {}

    cmd_stack = []

    #use f(**dict) to pass a dictionary of args to func
    def __init__(self,data=dict(),args=dict(),type=None,export=None,par_mode=False):
        self.args = args
        self.data = data
        self.type = type
        self.export = export
        self.par_mode = par_mode

        threading.Thread.__init__(self)

    def run (self):
        #Plot types
        plot = r.plot
        hist = r.hist
        barplot = r.barplot
        pie = r.pie
        qqnorm = r.qqnorm
        qqplot= r.qqplot

        #Export types
        if self.export:
            #Shut down all other plots before we do anything involving exporting
            r['graphics.off']()
            filename,extension = self.export

            if extension not in filename:
                extension += filename

            if extension == '.svg':
                svg(filename)
            elif extension == '.png':
                png(filename)
            elif extension == '.ps':
                postscript(filename)
            elif extension == '.pdf':
                #There is a rather strange bug where points get rendered as
                #letters unless we toggle useDingbats=False
                pdf(filename,useDingbats=False)

            if self.par_mode:
                rows, columns = self.par_mode
                r('par(mfrow=c(%s,%s))' % (rows,columns))
        else:
            #Don't bother opening a new window if there already is an open one
            #unless the user has specified that every new plot should open in a
            #new window
            if thereArePlotWindowsOpen() and prefs.get_pref('single_plot'):
                #Clear the previous plots, unless we're in par mode
                if not self.par_mode:
                    r('plot.new()')
                else:
                    rows, columns = self.par_mode
                    r('par(mfrow=c(%s,%s))' % (rows,columns))
            else:
                X11()

        if self.type=='scatter':
            x = self.data['x']
            y = self.data['y']
            plot(x,y,**self.args)

        if self.type=='scatter.smooth':
            x = self.data['x']
            y = self.data['y']

            r['scatter.smooth'](x=x,y=y,**self.args)

        if self.type=='matplot':
            df = robjects.r['data.frame'](**self.data)
            plot(df,**self.args)

        if self.type=='histogram':
            x = self.data['x']
            hist(x,**self.args)

        if self.type=='bar':
            x = self.data['x']
            barplot(x,**self.args)

        if self.type=='pie':
            x = self.data['x']
            pie(x,**self.args)

        if self.type=='qqnorm':
            x = self.data['x']
            qqnorm(x,**self.args)

        if self.type=='qqplot':
            x = self.data['x']
            y = self.data['y']
            qqplot(x,y,**self.args)

        if self.type=='boxplot':
            data = r['data.frame'](**self.data)
            r['boxplot'](data,**self.args)

        if self.type=='general':
            '''data is passed directly to plot'''
            plot(self.data,**self.args)

        if self.export:
            #Run through an secondary commands before we save the image
            for c in self.cmd_stack:
                cmd,args,kwargs = c
                apply(cmd,args,kwargs)
                self.cmd_stack.remove(c)
            devoff()
            return

        self.t = threading.Timer(0.1, self.refresh)
        self.t.start()

    def add_cmd(self,command,*args,**kwargs):
        '''Add a command to be executed after the plot is created'''
        
        #Since this is a seperate thread we have to have a stack to handle
        #commands passed after the timer is started'''

        self.cmd_stack.append((command,args,kwargs))

    def refresh(self):
        while self.halt == False:
            for c in self.cmd_stack:
                cmd,args,kwargs = c
                apply(cmd,args,kwargs)
                self.cmd_stack.remove(c)
            rinterface.process_revents()
            time.sleep(0.1)
        if self.halt == True:
            self.t.cancel()

#----------------------------------------
# RPy Wrapper Classes
#----------------------------------------

class robject(object):
    'The base class for all robjects'

    #Human readable name of object
    type = None
    #Where the object should be viewed 'frame' or 'output'
    outputsTo = None
    #Reference to the RPy2 object
    object = None
    #Label of the object, should be identical to the name of the object
    #in the globalEnv of RPy2
    label = None
    #Icon to show in object sidebar
    icon = None

    def __init__(self,*args,**kwargs):
        apply(self.construct,args,kwargs)

    def construct(self):
        pass

    def refresh(self):
        pass

#---------------------------------
# Data Storing Objects
#---------------------------------

class dataframe(robject):
    '''We store the data in three ways

    columns -- a dictionary {column name, column type}
    column_data -- a dictionary {column name, rvector}
    rawdata -- a numpy array of the data

    object -- the reference to the actual robject in the rsession
    '''

    #   Ok to summarize this non-intuitive code...
    #   Say we have a dataframe in R, when we bring it in to python
    #   we store the data in a couple of ways
    #   
    #       V1     V2
    #   1  0.1     5
    #   2  0.2     6
    #   3  0.3     7
    #   4  0.4     8
    #   5  0.5     9
    #   
    #   rawdata would hold the numpy array [  [0.1,0.2,0.3,0.4,0.5] , [5,6,7,8,9] ]
    #   rownames would hold the array [1,2,3,4,5]
    #   columns would hold column labels and their types {'V1':float , 'V2':int}
    #   column_data would hold {'V1': [0.1,0.2,0.3,0.4,0.5] , 'V2':[5,6,7,8,9]}

    columns = {}
    column_data = {}

    rawdata = None
    rownames = None

    object = None
    isColumn = False

    outputsTo = 'frame'
    icon = './ui/icons/dataframe.png'

    type = 'Data Frame'

    def construct(self,data,columns=None,label=None,rownames=None):
        '''Take an array of data and dict of columns and create a dataframe class with
        self.object as a reference to the rpy2 object
        '''

        self.rawdata = data
        self.label = label
        self.rownames = rownames
        self.columns = columns

        if len(data.shape)==1:
            self.isColumn = True

        d = dict()

        for i,col in enumerate(column_extractor(data)):
            column_name = columns.keys()[i]

            #This gets passed to R
            d[column_name] = col
            #This is stored on the python side
            self.column_data[column_name] = col

        self.object = r['data.frame'](**d)

    def refresh(self):
        '''Rebuild the R object from the internal numpy array and return the R object'''
        self.construct(data=self.rawdata,columns=self.columns,label=self.label,rownames=self.rownames)
        return self.object

    def __getitem__(self,key):
        '''Returns a string containing the R code to access the column

        data.frame $ column
        '''
        return self.label + '$' + key

class timeseries(robject):
    start = None
    end = None
    frequency = None
    times = None
    deltat = None
    times = None

    columns = {}
    column_data = {}

    rawdata = None
    rownames = None

    object = None
    isColumn = False

    outputsTo = 'frame'
    icon = './ui/icons/timeseries.png'

    def construct(self,data,label=None,start=None,end=None,frequency=None,deltat=None):
        self.rawdata = data
        self.label = label

        self.columns = {'V1':float}
        data=translate_to_vector(data)
        self.column_data = {'V1':data}

        args = rdict({
            'start':start,
            'end':end,
            'frequency':frequency,
            'deltat':deltat,
        })

        self.type = "Time Series"

        self.object = r['ts'](data,**args)
        self.times = times(self.object)
        self.rownames = self.times

        #This is a 'hidden' variable that doesn't show up in the frame view
        #but is still accessible if called directly by plots, stat tests, etc...
        self.column_data['(Time)'] = r['as.numeric'](self.times)

    def __getitem__(self,key):
        if key == '(Time)':
            return self.times

class dist(robject):
    def construct(self):
        pass

class matrix(robject):
    def construct(self):
        pass

class linear_model(robject):
    type = 'Linear Model'
    icon = './ui/icons/description.png'
    outputsTo = 'output'

    def construct(self,fit,label=None):
        self.object = fit
        self.label = label

        #This isn't going to make it into this release
        #numpy.array(r['coef'](fit))
        #self.coefficents = dataframe(coefs,columns={'Residuals':float},label=label+'$'+'coefficents')

        self.coefs = r['coef'](fit)
        self.residuals = r['resid'](fit)
        self.fitted = r['fitted'](fit)
        self.text = str(fit)

class description(robject):
    '''A text description of some stastical function: mean anova...'''
    object = None
    outputsTo = 'output'
    label = None
    text = None
    type = 'Description'

    icon = './ui/icons/description.png'

    '''XTable can't handle some data types so we need need to run table()'''
    tabelize = False

    def construct(self,object,label=None,tabelize=False):
        self.object = object
        self.label = label
        self.tabelize = tabelize
        #Cache the output text so we aren't calling it constantly
        self.text = str(object)

def thereArePlotWindowsOpen():
    #dev.list is a vector, so is_null returns a vector apparently
    window_list_is_empty = is_null(r['dev.list']())[0]
    if window_list_is_empty:
        return False
    else:
        return True


