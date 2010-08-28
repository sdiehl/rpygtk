# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

from ui import plotwindow
from ui import wrappers
from lib import rsession
from lib.utils import *


def require_vars(f):
    '''A decorator that requires that all the custom variables are set before executing the function'''
    def wrapper(*args, **kwargs):
        self = args[0]
        #Get the self object from the method
        if (self.variables_are_set()):
            f(*args, **kwargs)
        else:
            error('Required variables are not set.')
    return wrapper

# The basic logic of any of these plots is something of the form:

# class Plot(PlotWindow):
#    
#    parameters = { dictionary labels for parameters : ui.wrappers widget to get user input }
#    
#    if self.multivariable is True then PlotWindow prmopts the user for an arbitrary
#    number of variables which are stored in the dictionary self.data {label: RVector}
#    
#    self.disable_x|y can be called to disable selection of either axis, otherwise
#    the the x and y data is stored self.x and self.y and point to the RVectors for
#    each column
#    
#     @require_vars wraps the plot function and checks PlotWindow's self.variables_are_set
#     @handle_errors spits any errors out to the user in a dialog window, in this case it 
#     also catches TypeErrors 
#
#     def plot(self,event,image=None)
#        fetch_labels() fetches most of the variables that show up in plots from the window
#        xmin,xmax,ymin,ymax only get applied if they appear in a pair, see RPlotThread
#        xlab,ylab get parsed for math syntax in RPlotThread
#
#        args = rdict()
#        rdict is a dictionary which doesn't allow empty values, it avoids errors since rpy2
#        can't figure out what to do with None
#        
#        sanity checks on user input
#
#        args['r parameters'] are set piecewise and applied to the plotting function in 
#        RPlotThread via plot(**args)
#        
#        plotwindow = 
#        RPlotThread( data in dictionary form , arguments to plotting function , type of 
#            graph , image = (path,extension) if exporting as image)
#        
#        start the thread
#
#        add the thread to the PlotWindows internal list of active threads, which eventually
#        gets passed off to Main if the user has specified they want the plot windows to stay
#        open after they destroy the plot window

#-----------------------------
# Pie Plot
#-----------------------------

class PiePlot(plotwindow.PlotWindow):

    title = "Pie Plot"

    disable_lines = True
    disable_points = True
    disable_frame = True
    disable_y = True
    
    # The OOP gods demand that we put the parameters inside the handler, for reasons
    # beyond mortal understanding ... aka something is fucked with attribute overloading
    def handler(self):
        self.parameters = {'Radius':wrappers.SingleEntry(cast_type=float),
                    'Polygon Edges':wrappers.SingleEntry(cast_type=int),
                    'Fill Density':wrappers.SingleEntry(cast_type=float),
                    'Clockwise':wrappers.ComboBox(['TRUE','FALSE'],1),
                    'Initial Angle':wrappers.SingleEntry(cast_type=float),
                    }

    @require_vars
    @handle_errors
    def plot(self,event,image=None):
        _xlab,_ylab,_title,_xmin,_ymin,_xmax,_ymax = self.fetch_labels()

        data = {'x':self.x}

        args = rdict({'xlab':_xlab,
                    'ylab':_ylab,
                    'main':_title
                    })

        #Normal Parameters
        args['radius'] = self.parameters['Radius'].get()
        args['edges'] = self.parameters['Polygon Edges'].get()
        args['density'] = self.parameters['Fill Density'].get()
        args['clockwise'] = self.parameters['Clockwise'].get()
        args['init.angle'] = self.parameters['Initial Angle'].get()

        #Ask the user to confirm that they want to plot copious amounts of data
        if len(data['x'])>30:
            if not wrappers.yesNoDialog('There is a very large amount of datapoints to graph, this make take a very time or even crash, are you sure you want to continue?'):
                return
        elif len(data['x'])>200:
            error('Too many data points for pie plot')
            return

        if self.fill_style.get_active_text() == 'Rainbow':
            args['col']=rsession.r['rainbow'](len(data['x']))
        if self.fill_style.get_active_text() == 'Gray':
            #Make shades of gray
            shades = map(lambda x:x/(len(data['x'])+1.0),range(0,len(data['x'])))
            args['col']=rsession.r['gray'](shades)

        plotwindow = rsession.RPlotThread(data=data,
                                        args=args,
                                        type='pie',
                                        export=image)

        plotwindow.start()
        self.active_threads.append(plotwindow)

#-----------------------------
# Scatter Plot
#-----------------------------

class ScatterPlot(plotwindow.PlotWindow):

    title = "Scatter Plot"
    
    disable_fill = True
    
    def handler(self):
        self.parameters = {'Type':wrappers.ComboBox(['Lines','Points','Both','Overplot','High-density'],1),
                'Aspect Ratio':wrappers.MultipleEntries(1,cast_type=float)
                }

    @require_vars
    @handle_errors
    def plot(self,event,image=None):

        _xlab,_ylab,_title,_xmin,_ymin,_xmax,_ymax = self.fetch_labels()

        data = {'x':self.x,
                'y':self.y}

        #We use an rdict so that any keys with empty values get thrown out and avoid conflicts with R
        args = rdict({'xlab':_xlab,
                    'ylab':_ylab,
                    'main':_title,
                    })

        if _xmin and _xmax:
            args['xlim']=rsession.translate_to_vector([_xmin,_xmax])

        if _ymin and _ymax:
            args['ylim']=rsession.translate_to_vector([_ymin,_ymax])

        #Normal Parameters
        args['asp'] = self.parameters['Aspect Ratio'].get()
        args['col'] = self.get_point_color()
        args['bty'] = self.get_frame_style()
        #R takes the first character of the type as an argument i.e 'o' = overplot
        args['type'] = self.parameters['Type'].get()[0].lower()
        args['pch'] = self.get_point_style()
        args['lty'] = self.get_line_style()+1

        plotwindow = rsession.RPlotThread(data=data,
                                        args=args,
                                        type='scatter',
                                        export=image)

        plotwindow.start()
        self.active_threads.append(plotwindow)

#-----------------------------
# Mutliple Scatter Plots
#-----------------------------

class MultiScatter(plotwindow.PlotWindow):

    title = "Multiple Scatter Plot"

    multivariable = True
    
    disable_lines = True
    disable_fill = True
    disable_frame = True
    
    def handler(self):
            self.parameters = {'Lower Panels':wrappers.CheckBox(None,False),
                'Plot Gap':wrappers.SingleEntry(cast_type=float),
                }

    @require_vars
    @handle_errors
    def plot(self,event,image=None):
        _xlab,_ylab,_title,_xmin,_ymin,_xmax,_ymax = self.fetch_labels()

        data = self.data

        args = rdict()

        if self.parameters['Lower Panels'].get():
            args['lower.panel'] = rsession.r('panel.smooth')
        else:
            args['lower.panel'] = rsession.null

        args['gap'] = self.parameters['Plot Gap'].get()
        args['pch'] = self.get_point_style()

        #Advanced Parameters

        plotwindow = rsession.RPlotThread(data=data,
                                        args=args,
                                        type='matplot',
                                        export=image)

        plotwindow.start()
        self.active_threads.append(plotwindow)


#-----------------------------
# Histogram
#-----------------------------

class Histogram(plotwindow.PlotWindow):

    title = "Histogram"
    
    def handler(self):
        self.parameters = {'Bin Algorithm':wrappers.ComboBox(['sturges','freedman-diaconis','scott'],1),
                    'Number of Bins':wrappers.SingleEntry(cast_type=int),
                    'Count Labels':wrappers.CheckBox(None,False),
                    'Show Normal Curve':wrappers.CheckBox(None,False),
                    'Frequency':wrappers.CheckBox(None,True),
                    'Fill Density':wrappers.SingleEntry(cast_type=int)
                    }

    disable_y = True
    disable_lines = True

    @require_vars
    @handle_errors
    def plot(self,event,image=None):
        _xlab,_ylab,_title,_xmin,_ymin,_xmax,_ymax = self.fetch_labels()

        data = {'x':self.x}

        args = rdict({'xlab':_xlab,
                    'ylab':_ylab,
                    'main':_title
                    })

        if _xmin and _xmax:
            args['xlim']=rsession.translate_to_vector([_xmin,_xmax])

        if _ymin and _ymax:
            args['ylim']=rsession.translate_to_vector([_ymin,_ymax])

        #One or the other
        args['breaks'] = self.parameters['Bin Algorithm'].get()
        if self.parameters['Number of Bins']:
            args['breaks'] = self.parameters['Number of Bins'].get()

        args['col'] = self.get_fill_color()
        args['density'] = self.parameters['Fill Density'].get()
        args['freq'] = self.parameters['Frequency'].get()
        args['labels'] = self.parameters['Count Labels'].get()

        plotwindow = rsession.RPlotThread(data=data,
                                        args=args,
                                        type='histogram',
                                        export=image)

        plotwindow.start()
        self.active_threads.append(plotwindow)

#-----------------------------
# Bar Plot
#-----------------------------

class BarPlot(plotwindow.PlotWindow):

    title = "Bar Plot"

    disable_points = True
    disable_lines = True
    disable_frame = True
    disable_y = True

    def handler(self):
        self.parameters = {'Fill Density':wrappers.SingleEntry()}

    @require_vars
    @handle_errors
    def plot(self,event,image=None):
        _xlab,_ylab,_title,_xmin,_ymin,_xmax,_ymax = self.fetch_labels()

        data = {'x':self.x}

        args = rdict({'xlab':_xlab,
                      'ylab':_ylab,
                      'main':_title
                     })

        if _xmin and _xmax:
            args['xlim']=rsession.translate_to_vector([_xmin,_xmax])

        if _ymin and _ymax:
            args['ylim']=rsession.translate_to_vector([_ymin,_ymax])

        plotwindow = rsession.RPlotThread(data=data,
                                        args=args,
                                        type='bar',
                                        export=image)

        args['col'] = self.get_fill_color()
        args['density'] = self.parameters['Fill Density'].get()

        plotwindow.start()
        self.active_threads.append(plotwindow)

#-----------------------------
# Q-Q Plot
#-----------------------------

class QQPlot(plotwindow.PlotWindow):

    title = "Q-Q Plot"

    disable_fill = True
    
    def handler(self):
            self.parameters = {'Show Line':wrappers.CheckBox(None,False)}

    #We'll handle variable checking on our to determine whether to use
    #qqnorm or qqplot
    @handle_errors
    def plot(self,event,image=None):
        _xlab,_ylab,_title,_xmin,_ymin,_xmax,_ymax = self.fetch_labels()

        data = {'x':self.x,
                'y':self.y}

        args = rdict({'xlab':_xlab,
                    'ylab':_ylab,
                    'main':_title
                    })

        if _xmin and _xmax:
            args['xlim']=rsession.translate_to_vector([_xmin,_xmax])

        if _ymin and _ymax:
            args['ylim']=rsession.translate_to_vector([_ymin,_ymax])

        args['col'] = self.get_point_color()
        args['bty'] = self.get_frame_style()
        args['pch'] = self.get_point_style()

        if self.x and self.y:
            plotwindow = rsession.RPlotThread(data=data,
                                            args=args,
                                            type='qqplot',
                                            export=image)
        elif self.x:
            #info('qnorm')
            plotwindow = rsession.RPlotThread(data=data,
                                type='qqnorm',
                                export=image)
        else:
            error('Required variables are not set.')
            return

        plotwindow.start()
        self.active_threads.append(plotwindow)

        if self.parameters['Show Line'].get():
            plotwindow.add_cmd(rsession.r['qqline'],self.x,col=self.get_line_color(),lty=self.get_line_style())


#-----------------------------
# Box Plot
#-----------------------------


class BoxPlot(plotwindow.PlotWindow):

    title = "Box Plot"

    disable_lines = True
    disable_points = True
    multivariable = True

    @require_vars
    @handle_errors
    def plot(self,event,image=None):
        _xlab,_ylab,_title,_xmin,_ymin,_xmax,_ymax = self.fetch_labels()

        data = self.data

        args = rdict({'xlab':_xlab,
                    'ylab':_ylab,
                    'main':_title
                    })

        if _xmin and _xmax:
            args['xlim']=rsession.translate_to_vector([_xmin,_xmax])

        if _ymin and _ymax:
            args['ylim']=rsession.translate_to_vector([_ymin,_ymax])

        args['col'] = self.get_fill_color()
        args['bty'] = self.get_frame_style()
        args['pch'] = self.get_point_style()

        plotwindow = rsession.RPlotThread(data=data,
                                            args=args,
                                            type='boxplot',
                                            export=image)
        plotwindow.start()
        self.active_threads.append(plotwindow)
