# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

import sys
import pygtk
pygtk.require("2.0")
import gtk

import urllib

import config
from lib import rsession
import inspect

from UserDict import UserDict

import numpy

def error(message,developer=False):
    if developer and not config.__devel__:
        return

    error = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL,
                      type=gtk.MESSAGE_ERROR,
                      message_format=message)
    error.add_button(gtk.STOCK_OK,gtk.RESPONSE_CLOSE)
    error.set_keep_above(True)
    error.set_modal(True)
    resp = error.run()
    if resp == gtk.RESPONSE_CLOSE:
        error.destroy()

def info(message,developer=False):
    if developer and not config.__devel__:
        return

    error = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL,
                      type=gtk.MESSAGE_INFO,
                      message_format=message)
    error.add_button(gtk.STOCK_OK,gtk.RESPONSE_CLOSE)
    error.set_modal(True)
    error.set_keep_above(True)
    resp = error.run()
    if resp == gtk.RESPONSE_CLOSE:
        error.destroy()

def handle_errors(f):
    ''' A decorator to trap errors'''
    def wrapper(*args, **kwds):
            try:
                return f(*args, **kwds)
            except rsession.rinterface.RRuntimeError,RError:
                error(str(RError))
            except ValueError,e:
                error('A type error occured, most likely the data inputted is not of the type required.')
            except Exception,e:
                error(str(e) + '\n' + str(sys.exc_info()) + '\n\n Call Stack: \n\n' +
                    str(inspect.trace()[-1]))
    return wrapper

#I end up using this more than I should...
import inspect

def get_class_that_defined_method(meth):
  obj = meth.im_self
  for cls in inspect.getmro(meth.im_class):
    if meth.__name__ in cls.__dict__: return cls
  return None

def gtkColorToRColor(color):
    '''Convert a gtk color into a hex string that r's rgb function can read'''
    return rsession.r['rgb'](color.red,color.green,color.blue,max=65535)
    
def get_path_from_url(uri):
    # get the path to file
    path = ""
    if uri.startswith('file:\\\\\\'): # windows
            path = uri[8:] # 8 is len('file:///')
    elif uri.startswith('file://'): # nautilus, rox
            path = uri[7:] # 7 is len('file://')
    elif uri.startswith('file:'): # xffm
            path = uri[5:] # 5 is len('file:')

    path = urllib.url2pathname(path) # escape special chars
    path = path.strip('\r\n\x00') # remove \r\n and NULL
    return path

def toggle_visible(widget):
    if widget.get_property('visible'):
        widget.hide()
    else:
        widget.show()

#We use ordered dictionaries to keep the column names/types, that way the nth
#column of a numpy matrix actually corresponds to the nth reference in the column dict

#From David Benjamin - http://code.activestate.com/recipes/107747/
#This works out of the box without having to apply any patches and whatnot
class odict(UserDict):
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)

class rdict(dict):
    '''A dictionary type that does not permit None types or empty strings in values'''
    def __setitem__(self, key, value):
        if value != None and value != '':
            #Fetch the parent class (dict) and invoke __setitem__ just like normal but with the
            #condition that we don't allow empty values
            super(rdict, self).__setitem__(key, value)
            
def dict_replace_key(dict,old,new):
    '''Replace a old key in dictionary with new key while preserving value'''
    
    #Use odict to preserve the order
    ndict = odict()
    for key,value in dict.iteritems():
        if key == old:
            ndict[new] = value
        else:
            ndict[key] = value
    return ndict
