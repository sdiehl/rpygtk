# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

import os
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

import ConfigParser
from ui import window

def get_pref(key):
    '''Fetch a config key by name, if the config file doesn't exist create it'''
    
    config = ConfigParser.ConfigParser()
    dir = os.environ['HOME']+'/.rpygtk/'
    config_file = dir + 'config'
    
    #If the config directory doesn't exist, create it
    if not os.path.isdir(dir):
        os.mkdir(dir)
    
    #If the config file doesn't exist, create it
    if not os.path.isfile(config_file):
        fd = open(config_file,'w')
        config.add_section('general')
        config.add_section('plotting')
        config.set("general", "auto_switch", True)
        config.set("general", "font", 'Sans 12')
        config.set("plotting", "single_plot", True)
        config.set("plotting", "close_plots", False)
        config.write(fd)
        fd.close()
        
    config.read(config_file)
    
    auto_switch =  config.getboolean("general", "auto_switch")
    font = config.get("general", "font")
    single_plot =  config.getboolean("plotting", "single_plot") 
    close_plots = config.getboolean("plotting", "close_plots")
    
    values = {'auto_switch':auto_switch,
              'font':font,
              'single_plot':single_plot,
              'close_plots':close_plots}
    
    if key in values:
        return values[key]
    else:
        return None

class Preferences(window.Window):
    '''Handles reading and writing the config file'''
    
    builder_file = "./ui/prefs.builder"
    builder = gtk.Builder()
    builder.add_from_file(builder_file)
    
    def __init__(self):
        self.construct('preferences')
        self.get_config()
        self.builder.connect_signals(self)
    
    #This handle fetching prferences from the widget
    def __get_pref(self,key):
        widget =  self.builder.get_object(key)
        if not widget:
            print 'Could not lookup preference key:', key
        if type(widget) is gtk.CheckButton:
            return widget.get_active()
        if type(widget) is gtk.FontButton:
            return gtk.FontButton().get_font_name()
            
    def get_config(self):
        config = ConfigParser.ConfigParser()
        dir = os.environ['HOME']+'/.rpygtk/'
        config.read(dir+'config')
        
        auto_switch =  config.getboolean("general", "auto_switch")
        font = config.get("general", "font")
        single_plot =  config.getboolean("plotting", "single_plot") 
        close_plots = config.getboolean("plotting", "close_plots")
        
        self.builder.get_object('auto_switch').set_active(auto_switch)
        self.builder.get_object('font').set_font_name(font)
        self.builder.get_object('single_plot').set_active(single_plot)
        self.builder.get_object('close_plots').set_active(close_plots)
    
    def write_config(self):
        dir = os.environ['HOME']+'/.rpygtk/'
        if not os.path.isdir(dir):
            os.mkdir(dir)
        config_file = dir + 'config'
        fd = open(config_file,'w')
        config = ConfigParser.ConfigParser()
        
        #Fetch from the Window
        auto_switch = self.__get_pref('auto_switch')
        font = self.__get_pref('font')
        single_plot = self.__get_pref('single_plot')
        close_plots = self.__get_pref('close_plots')

        config.add_section("general")
        config.set("general", "auto_switch", auto_switch)
        config.set("general", "font", font)
        config.add_section("plotting")
        config.set("plotting", "single_plot", single_plot)
        config.set("plotting", "close_plots", close_plots)
        
        config.write(fd)
        fd.close()
        
    def hide(self,*event):
        self.window.hide()
        return True
    
    def apply(self,*event):
        self.write_config()
        self.window.hide()