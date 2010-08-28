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

import random
import numpy

from ui import window

class Distribution(object):
    def __init__(self,label,func,args):
        self.label = label
        self.func = func
        self.args = args


distributions = [
Distribution('Uniform Floats',lambda x,y: random.uniform(x,y),['Lower Bound','Upper Bound']),
Distribution('Uniform Integers',lambda x,y: random.randint(x,y),['Lower Bound','Upper Bound']),
Distribution('Gaussian Distribution',lambda x,y: random.gauss(x,y),['Mu','Sigma']),
Distribution('Triangular Distribution',lambda x,y,z: random.triangular(x,y,z),['Lower Bound','Upper Bound', 'Mode']),
Distribution('Exponential Distribution',lambda x: random.expovariate(x),['Lambda']),
Distribution('Gamma Distribution',lambda x,y: random.gammavariate(x,y),['Alpha','Beta']),
Distribution('Log normal Distribution',lambda x,y: random.gauss(x,y),['Mu','Sigma']),
Distribution('Normal Distribution',lambda x,y: random.gauss(x,y),['Mu','Sigma']),
Distribution('Von Mises Distribution',lambda x,y: random.gauss(x,y),['Mu','Kappa']),
]

class RandomGen(window.Window,gtk.Assistant):
    distribution = None
    args = None
    
    def __init__(self,parent):
        global distributions
        
        self.main = parent
        
        gtk.Assistant.__init__(self)

        self.connect('apply', self.generate)
        self.connect('cancel', self.hide)
        self.connect('delete_event', self.hide)
        self.connect('close', self.hide)

        # Construct page 0
        vbox = gtk.VBox(False, 5)
        vbox.set_border_width(5)
        vbox.show()
        self.append_page(vbox)
        self.set_page_title(vbox, 'Distributions')
        self.set_page_type(vbox, gtk.ASSISTANT_PAGE_CONTENT)
        
        #distributions = [
        #    ('Uniform Floats',lambda x,y: random.uniform(x,y),['Lower Bound','Upper Bound']),
        #    ('Uniform Integers',lambda x,y: random.randint(x,y),['Lower Bound','Upper Bound']),
        #    ('Gaussian Distribution',lambda x,y: random.gauss(x,y))
        #]
        
        group = gtk.RadioButton(None, None)

        for d in distributions:
            button = gtk.RadioButton(group, d.label)
            button.connect("toggled", self.set_func, d)
            vbox.pack_start(button, True, True, 0)
            button.set_active(False)
            vbox.pack_end(button)
            button.show()
        
        self.show()

    def set_func(self, button, d):
        self.distribution = d
        self.set_page_complete(button.get_parent(), True)
        
        hbox = gtk.HBox(False,5)
        hbox.show()
        self.append_page(hbox)
        
        self.set_page_title(hbox, 'Parameters')
        self.set_page_type(hbox, gtk.ASSISTANT_PAGE_CONFIRM)
        
        vbox1 = gtk.VBox(False, 5)
        vbox1.set_border_width(5)
        vbox1.show()
        
        vbox2 = gtk.VBox(False, 5)
        vbox2.set_border_width(5)
        vbox2.show()
        
        #Columns
        label = gtk.Label('Columns')
        label.show()
        vbox1.pack_start(label,True,True,0)
        adjustment = gtk.Adjustment(2, 1, 200, 1, 1)
        self.columns = gtk.SpinButton(adjustment)
        self.columns.show()
        vbox2.pack_start(self.columns,True,True,0)
        
        #Rows
        label = gtk.Label('Rows')
        label.show()
        vbox1.pack_start(label,True,True,0)
        adjustment = gtk.Adjustment(10, 1, 200, 1, 1)
        self.rows =  gtk.SpinButton(adjustment)
        self.rows.show()
        vbox2.pack_start(self.rows,True,True,0)
        
        inputs = []
        
        for arg in d.args:
            label = gtk.Label(arg)
            label.show()
            #self.append_page(label)
            vbox1.pack_start(label,True,True,0)
            input = gtk.Entry()
            inputs.append(input)
            input.connect('focus-out-event',self.generate_random,inputs)
            input.show()
            vbox2.pack_start(input,True,True,0)

            
        hbox.pack_start(vbox1)
        hbox.pack_start(vbox2)
        
    def generate_random(self,entry,event,inputs):
        for fields in inputs:
            if len(fields.get_text()) <= 0:
                return
        self.args = [float(input.get_text()) for input in inputs]
        self.set_page_complete(entry.get_parent().get_parent(), True)

    def handler(self):
        pass
        #close = self.builder.get_object('closebutton')
        #close.connect('clicked', self.hide)
        
    def generate(self,event):
        if len(self.args) != len(self.distribution.args):
            print "Argument length mismatch, this probably shouldn't happen."

        gen = lambda x: apply(self.distribution.func,self.args)
        
        cols = int(self.columns.get_text())
        rows = int(self.rows.get_text())
        vfunc = numpy.vectorize(gen)
        
        res = vfunc(numpy.zeros((rows,cols)))
        
        c = dict()
        for i in range(0,cols):
            c['V%s' % i] = float
        
        self.main.render_dataframe(res,c)
        
        #except TypeError,ValueError:
        #    print "Cannot match types."
        
    def hide(self,*event):
        self.window.hide()
        return True
    