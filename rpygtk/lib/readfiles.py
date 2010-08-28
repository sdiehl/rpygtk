# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

import os
import csv
import numpy
import rsession

from lib.utils import *

def readfile(uri):
    '''Read a files and returns a dict of {column header: column type} and data in a numpy matrix'''
    
    if uri.startswith('file:\\\\\\'): # windows
        path = uri[8:] 
    elif uri.startswith('file://'): # nautilus, rox
        path = uri[7:]
    elif uri.startswith('file:'): # xffm
        path = uri[5:]
    else:
        path = uri
    
    if not os.path.isfile(path):
        print "File cannot be opened."
        return False
    
    (filepath, filename) = os.path.split(path)
    (filename, extension) = os.path.splitext(filename)
    
    #There are a bunch of different ways to write delimite csv files, maybe we should
    #the file to find the delimeter.
    
    if extension == '.csv':
        df = rsession.r['read.csv'](rsession.r['file'](path))
        
        colnames = df.colnames()
        rownames = df.rownames()
        
        data = numpy.array(df).T
        cols = numpy.array(rownames).T
        
        columns = odict()
        
        for colname,type in zip(colnames,df):
            columns[colname] = str(rsession.typeof(type))

        col = numpy.array(rownames)
        
        return columns,data,cols
    
    elif extension == '.xls':
        if not rsession.gdata_is_available:
            error('Cannot load Excel Spreadsheets without the gdata library.')
            return
        
        try:
            df = rsession.r['read.xls'](path)
            
            colnames = df.colnames()
            rownames = df.rownames()
            
            data = numpy.array(df).T
            cols = numpy.array(rownames).T
            
            columns = odict()
            
            for colname,type in zip(colnames,df):
                columns[colname] = str(rsession.typeof(type))
    
            col = numpy.array(rownames)
            
            return columns,data,cols
        except rsession.ri.RRuntimeError,RError:
            error('''Could not import spreadsheet. Make sure the file is stored in
                  Excel 2003 format since R cannot parse files generated by Excel 2007
                  and beyond''')
    
def try_casting(datapoint):
    '''Try to cast the inputed data to a float, otherwise default to string'''
    try:
        return float(datapoint)
    except:
        return str(datapoint)