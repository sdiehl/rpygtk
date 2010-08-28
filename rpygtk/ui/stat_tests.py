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

import lib.rsession

from ui.variable_prompt import VariablePrompt
from ui.textoutput import TextOutput
from ui.testwindow import TestWindow
from ui.regression import RegressionWindow

from ui import wrappers
from lib import rsession
from lib.utils import *

#There seems to be an issue that this decorator won't get inherited if we include
# it in RegressionWindow class... not sure how to resolve this at this time
def require_vars(f):
    '''A decorator that requires that all the custom variables are set before executing the function'''
    def wrapper(*args,**kwargs):
        self = args[0]
        #Get the self object from the method
        if (self.variables_are_set()):
            f(*args,**kwargs)
        else:
            error('Required variables are not set.')
    return wrapper

#-----------------------------
# ANOVA
#-----------------------------
class anova(TestWindow):

    title = 'One-Way ANOVA'

    def handler(self):
        VariableSelector = wrappers.VariableSelector

        self.custom_variables = {'independent':VariableSelector(self,label='Indepenent Variable',maximum=1),
                                                'dependent':VariableSelector(self,label='Dependent Variable(s)')}

    @require_vars
    @handle_errors
    def run(self,*event):
        ilab,idata = self.custom_variables['independent'].get_first()
        dlab,ddata = self.custom_variables['dependent'].get_first()

        x = self.active_r_object[ilab]
        y = self.active_r_object[dlab]
        fit = rsession.r('lm(%s ~ %s,data=%s)' % (y,x,self.active_r_object.label))

        if idata == ddata:
            error('Variables are identical, results may not be accurate.')

        anova_output = rsession.r['anova'](fit)

        name = 'ANOVA ' + str(self.active_r_object.label)

        #This isn't good if there are variables called x,y in the workspace
        rsession.rm('x')
        rsession.rm('y')

        self.parent.render_description(anova_output,label=name)

#-----------------------------
# McNemar's Chi-squared
#-----------------------------
class mcnemar(TestWindow):

    title = "McNemar's Chi-squared Test"

    parameters = {'Apply continuity correction':wrappers.CheckBox(None,False)
                  }

    def handler(self):
        VariableSelector = wrappers.VariableSelector

        self.custom_variables = {'samples':VariableSelector(self,label='Sample(s)',maximum=2)}

    @handle_errors
    @require_vars
    def run(self,*event):

        #I tried for WAY to long to get this to work with the high-level interface
        #but it usually resulted in the output having a very long label that
        #contained all the data in the vector we passed to it, still not sure
        #how to resolve it

        args = rdict()

        args['correct'] = self.parameters['Apply continuity correction'].get()

        args = rsession.arguments_to_string(args)

        s1lab,s1data = self.custom_variables['samples'][0]
        if len(self.custom_variables['samples'])==2:
            s2lab,s2data = self.custom_variables['samples'][1]
            x = self.active_r_object[s1lab]
            y = self.active_r_object[s2lab]
            anova_output = rsession.r('mcnemar.test(x=%s,y=%s%s)' % (x, y, args))
        else:
            info('Please select two samples.')

        name = 'T-Test ' + str(self.active_r_object.label)

        self.parent.render_description(anova_output,label=name)

#-----------------------------
# T-Test
#-----------------------------

class ttest(TestWindow):

    title = 'T-Test'

    parameters = {'Mu':wrappers.SingleEntry(cast_type=float),
                  'Confidence Level':wrappers.ComboBox(['0.99','0.95','0.90','0.80'],1),
                  #'Paired':wrappers.CheckBox(None,False),
                  'Equal Variances':wrappers.CheckBox(None,False),
                  'Alternative Hypothesis':wrappers.ComboBox(['Less Than','Two Sided','Greater Than'],1),
                  }

    def handler(self):
        VariableSelector = wrappers.VariableSelector

        self.custom_variables = {'samples':VariableSelector(self,label='Sample(s)',maximum=2)}

    @handle_errors
    @require_vars
    def run(self,*event):

        #I tried for WAY to long to get this to work with the high-level interface
        #but it usually resulted in the output having a very long label that
        #contained all the data in the vector we passed to it, still not sure
        #how to resolve it

        args = rdict()

        args['mu'] = self.parameters['Mu'].get()
        args['conf.level'] = float( self.parameters['Confidence Level'].get() )
        #args['paired'] = self.parameters['Paired'].get()
        args['var.equal'] = self.parameters['Equal Variances'].get()
        #R takes the first character as an argument
        args['alternative'] = self.parameters['Alternative Hypothesis'].get().lower()[0]

        args = rsession.arguments_to_string(args)
        print args

        s1lab,s1data = self.custom_variables['samples'][0]
        if len(self.custom_variables['samples'])>1:
            s2lab,s2data = self.custom_variables['samples'][1]
            x = self.active_r_object[s1lab]
            y = self.active_r_object[s2lab]
            anova_output = rsession.r('t.test(x=%s,y=%s,data=%s,%s)' % (x, y, self.active_r_object.label, args))
        else:
            x = self.active_r_object[s1lab]
            anova_output = rsession.r('t.test(x=%s,data=%s,%s)' % (x, self.active_r_object.label, args))

        name = 'T-Test ' + str(self.active_r_object.label)

        self.parent.render_description(anova_output,label=name)

#-----------------------------
# Correlation Test
#-----------------------------

class cortest(TestWindow):

    title = 'Correlation Test'

    parameters = {'Method':wrappers.ComboBox(['Pearson','Kendall','Spearman'],1),
                  'Confidence Level':wrappers.ComboBox(['0.99','0.95','0.90','0.80'],1),
                  'Alternative Hypothesis':wrappers.ComboBox(['Less Than','Two Sided','Greater Than'],1),
                  'Exact':wrappers.CheckBox(None,False)
                  }

    def handler(self):
        VariableSelector = wrappers.VariableSelector
        self.custom_variables = {'samples':VariableSelector(self,label='Sample(s)',maximum=2)}

    @handle_errors
    @require_vars
    def run(self,*event):

        #I tried for WAY to long to get this to work with the high-level interface
        #but it usually resulted in the output having a very long label that
        #contained all the data in the vector we passed to it, still not sure
        #how to resolve it

        args = rdict()

        args['method'] = self.parameters['Method'].get().lower()[0]
        args['conf.level'] = float( self.parameters['Confidence Level'].get() )
        #R takes the first character as an argument
        args['alternative'] = self.parameters['Alternative Hypothesis'].get().lower()[0]
        args['exact'] = self.parameters['Exact'].get()

        args = rsession.arguments_to_string(args)

        s1lab,s1data = self.custom_variables['samples'][0]
        if len(self.custom_variables['samples'])==2:
            s2lab,s2data = self.custom_variables['samples'][1]
            x = self.active_r_object[s1lab]
            y = self.active_r_object[s2lab]
            anova_output = rsession.r('cor.test(x=%s,y=%s,data=%s,%s)' % (x, y, self.active_r_object.label, args))
        else:
            info('Please select two samples.')

        name = 'Correlation Test ' + str(self.active_r_object.label)

        self.parent.render_description(anova_output,label=name)

#-----------------------------
# Chi-Square Test
#-----------------------------

class chisq(TestWindow):

    title = 'Chi Square Test'

    parameters = {'Apply continuity correction':wrappers.CheckBox(None,False),
                  'Compute p-values by Monte Carlo simulation':wrappers.CheckBox(None,False),
                  }

    def handler(self):
        VariableSelector = wrappers.VariableSelector
        self.custom_variables = {'samples':VariableSelector(self,label='Sample(s)',maximum=2)}

    @handle_errors
    @require_vars
    def run(self,*event):

        #I tried for WAY to long to get this to work with the high-level interface
        #but it usually resulted in the output having a very long label that
        #contained all the data in the vector we passed to it, still not sure
        #how to resolve it

        args = rdict()

        args['simulate.p.value'] = self.parameters['Compute p-values by Monte Carlo simulation'].get()
        args['correct'] = self.parameters['Apply continuity correction'].get()

        args = rsession.arguments_to_string(args)

        s1lab,s1data = self.custom_variables['samples'][0]
        if len(self.custom_variables['samples'])==2:
            s2lab,s2data = self.custom_variables['samples'][1]
            x = self.active_r_object[s1lab]
            y = self.active_r_object[s2lab]
            anova_output = rsession.r('chisq.test(x=%s,y=%s%s)' % (x, y, args))
        else:
            info('Please select two samples.')

        name = 'Chi Square Test ' + str(self.active_r_object.label)

        self.parent.render_description(anova_output,label=name)

#-----------------------------
# Nonlinear Regression
#-----------------------------

#begin ugliness

class nonlinear_regression(RegressionWindow):
    title = 'Nonlinear Regression'

    def handler(self):
        self.show_model = True
        self.show_degree_slider = False
        VariableSelector = wrappers.VariableSelector

        self.custom_variables = {'independent':VariableSelector(self,label='Indepenent Variable',maximum=1),
                                                'dependent':VariableSelector(self,label='Dependent Variable(s)',maximum=1)}

    @require_vars
    @handle_errors
    def plot_fit(self,event,image=None):
        model = self.get_model().lower()

        dependent = model.partition('~')[0]
        independent = model.partition('~')[2]

        coefs = set()
        vars = set()

        #We're iterating over the variables, so that later it will be easier to do this in more than 2D
        for symbol in model:
            if symbol is 'x' or symbol is 'y':
                vars.add(symbol)
            elif symbol.isalpha():
                coefs.add(symbol)

        ilab,idata = self.custom_variables['independent'].get_first()
        dlab,ddata = self.custom_variables['dependent'].get_first()

        try:
            fmla = rsession.ro.RFormula(model)
        except:
            error('The model you specified is not valid.')
            return
        env = fmla.getenvironment()
        env['x'] = idata
        env['y'] = ddata

        #I love R, this would take like 30 hours to implement in python
        #this fetches all coefficents but ignores functions like sin,cos...
        coefs = list ( rsession.r['all.vars'](fmla)  )

        #Don't consider x and y as coefficents
        coefs.remove('y')
        coefs.remove('x')

        data={'x':idata,'y':ddata}
        args={'xlab':ilab,'ylab':dlab}

        object = rsession.r(self.active_r_object.label)

        startdict = {}

        for i in coefs:
            startdict[i]= 1

        startlist=rsession.r['list'](**startdict)

        seq=rsession.r['seq']
        rmin=rsession.r['min']
        rmax=rsession.r['max']

        # There is nothing truly beautiful but that which can never be of any use whatsoever; everything
        # useful is ugly; keep that in mine while reading the next 40 lines.

        #Generate a range of points so our predicted curve is smooth
        lenout = {'length.out':500}
        df = rsession.r['data.frame']
        smooth_range = rsession.r['seq'](  rsession.r['min'](idata) , rsession.r['max'](idata),**lenout)

        fit_found = False
        predicted = None

        #Try and find the fit, loop using the user provided starting values until we find a fit
        while(fit_found == False):
            try:
                #Try to find a fit
                fit = rsession.r['nls'](formula=fmla.r_repr(),data=object,start=startlist)
                #Interpolate the fit over the the range of the independent variable
                predicted = rsession.r['predict'](fit,df(x=smooth_range))

            #If we fail to achieve convergance
            except:
                #Prompt the user for more information about coefficents
                info('Fit could not be found, please adjust starting values for coefficents.')
                startvalues = VariablePrompt(startdict.keys()).get_inputs()
                if not startvalues:
                    return
                for coef,value in zip(startdict.keys(),startvalues):
                    startdict[coef] = value
                startlist=rsession.r['list'](**startdict)

            if predicted:
                #info('Fit Found')
                fit_found = True
                self.fit = fit
                self.result = fit

        plotwindow = rsession.RPlotThread(data=data,
                                args=args,
                                type='scatter',
                                export=image,
                                par_mode=(1,1))

        #print 'predicted',predicted
        #print 'smooth',smooth_range

        plotwindow.add_cmd(rsession.ro.r.lines,smooth_range,predicted,col='red')
        plotwindow.start()

        self.active_threads.append(plotwindow)

    @require_vars
    @handle_errors
    def plot_summary(self,event,image=None):
        if not rsession.nlstools_is_available:
            error('The nlstools library is not installed, summary of nls fit cannot be plotted.')
        elif self.fit:
            args = {}
            args['which'] = 0
            fit = rsession.r['nlsResiduals'](self.fit)
            plotwindow = rsession.RPlotThread(data=fit,
                                            type='general',
                                            export=image,
                                            par_mode=(2,2),
                                            args=args)

            plotwindow.start()
            self.active_threads.append(plotwindow)
        else:
            info('Please run Plot Fit to generate fit parameters first.')

#end ugliness

#-----------------------------
# Linear Regression
#-----------------------------

class linear_regression(RegressionWindow):
    title = 'Linear Regression'

    def handler(self):
        VariableSelector = wrappers.VariableSelector

        self.custom_variables = {'independent':VariableSelector(self,label='Indepenent Variable',maximum=1),
                                                'dependent':VariableSelector(self,label='Dependent Variable(s)')}

    @require_vars
    @handle_errors
    def plot_fit(self,event,image=None):

        if not self.variables_are_set():
            error('Required variables are not set.')
            return

        ilab,idata = self.custom_variables['independent'].get_first()
        dlab,ddata = self.custom_variables['dependent'].get_first()

        x = self.active_r_object[ilab]
        y = self.active_r_object[dlab]
        fit = rsession.r('lm(%s ~ %s,data=%s)' % (y,x,self.active_r_object.label))
        self.result = fit

        data={'x':idata,'y':ddata}
        args={'xlab':ilab,'ylab':dlab}

        plotwindow = rsession.RPlotThread(data=data,
                                        args=args,
                                        type='scatter',
                                        export=image,
                                        par_mode=(1,1))

        plotwindow.add_cmd(rsession.r['abline'],fit,col='red')

        plotwindow.start()
        self.active_threads.append(plotwindow)

    @require_vars
    @handle_errors
    def plot_summary(self,event,image=None):

        if not self.variables_are_set():
            error('Required variables are not set.')
            return

        #rsession.r('par(mfrow=c(2,2))')

        ilab,idata = self.custom_variables['independent'].get_first()
        dlab,ddata = self.custom_variables['dependent'].get_first()

        x = self.active_r_object[ilab]
        y = self.active_r_object[dlab]
        fit = rsession.r('lm(%s ~ %s,data=%s)' % (x,y,self.active_r_object.label))
        self.result = fit

        plotwindow = rsession.RPlotThread(data=fit,
                                        type='general',
                                        export=image,
                                        par_mode=(2,2))

        plotwindow.start()
        self.active_threads.append(plotwindow)

#-----------------------------
# Local Regression
#-----------------------------

class local_regression(RegressionWindow):
    title = 'Local Regression'

    def handler(self):
        VariableSelector = wrappers.VariableSelector

        self.custom_variables = {'independent':VariableSelector(self,label='Indepenent Variable',maximum=1),
                                 'dependent':VariableSelector(self,label='Dependent Variable(s)')}

    @require_vars
    @handle_errors
    def plot_fit(self,event,image=None):

        if not self.variables_are_set():
            error('Required variables are not set.')
            return

        rsession.r('par(mfrow=c(1,1))')

        ilab,idata = self.custom_variables['independent'].get_first()
        dlab,ddata = self.custom_variables['dependent'].get_first()

        #fit = rsession.r['loess'](idata,ddata).object

        data={'x':idata,'y':ddata}
        args={'xlab':ilab,'ylab':dlab}

        plotwindow = rsession.RPlotThread(data=data,
                                          args=args,
                                          type='scatter.smooth')

        plotwindow.start()
        self.active_threads.append(plotwindow)

    @require_vars
    @handle_errors
    def plot_summary(self,event,image=None):

        if not self.variables_are_set():
            error('Required variables are not set.')
            return

        rsession.r('par(mfrow=c(2,2))')

        ilab,idata = self.custom_variables['independent'].get_first()
        dlab,ddata = self.custom_variables['dependent'].get_first()

        x = self.active_r_object[ilab]
        y = self.active_r_object[dlab]
        fit = rsession.r('lm(%s ~ %s,data=%s)' % (x,y,self.active_r_object.label))
        self.result = fit

        plotwindow = rsession.RPlotThread(data=fit,
                                          type='general',
                                          par_mode=True)


        plotwindow.start()
        self.active_threads.append(plotwindow)

#-----------------------------
# Polynomial Regression
#-----------------------------

class polynomial_regression(RegressionWindow):
    title = 'Polynomial Regression'

    show_degree_slider = True

    def handler(self):
        VariableSelector = wrappers.VariableSelector

        self.custom_variables = {'independent':VariableSelector(self,label='Indepenent Variable',maximum=1),
                                 'dependent':VariableSelector(self,label='Dependent Variable(s)')}

    @require_vars
    @handle_errors
    def plot_summary(self,event,image=None):

        ilab,idata = self.custom_variables['independent'].get_first()
        dlab,ddata = self.custom_variables['dependent'].get_first()

        #These return the parent$column strings
        x = self.active_r_object[ilab]
        y = self.active_r_object[dlab]

        fit = rsession.r('lm(%s~poly(%s,%i))' % (y,x,self.degree.get_value()))
        self.result = fit

        plotwindow = rsession.RPlotThread(data=fit,
                                        type='general',
                                        par_mode=(2,2),
                                        export=image)

        plotwindow.start()

        self.active_threads.append(plotwindow)

    @require_vars
    @handle_errors
    def plot_fit(self,event,image=None):

        ilab,idata = self.custom_variables['independent'].get_first()
        dlab,ddata = self.custom_variables['dependent'].get_first()

        #These return the parent$column strings
        x = self.active_r_object[ilab]
        y = self.active_r_object[dlab]

        fit = rsession.r('lm(%s~poly(%s,%i))' % (y,x,self.degree.get_value()))
        self.result = fit

        data={'x':idata,'y':ddata}
        args={'xlab':ilab,'ylab':dlab}

        plotwindow = rsession.RPlotThread(data=data,
                                        args=args,
                                        par_mode=(1,1),
                                        export=image,
                                        type='scatter')

        plotwindow.start()

        seq=rsession.r['seq']
        min=rsession.r['min']
        max=rsession.r['max']

        object = rsession.env[self.active_r_object.label]
        range = seq(min(object), max(object), length_out = 100)
        predicted = rsession.r['predict'](fit,data_frame=range)
        plotwindow.add_cmd(rsession.ro.r.lines,idata,predicted,col='red')
        self.active_threads.append(plotwindow)
