#!/usr/bin/env python

import os
from distutils.core import setup

rpygtk_files = ['*.txt','*.desktop','lib/*','examples/*','ui/*.*','ui/icons/*.svg','ui/icons/*.png','bin/*']

setup(name='rpygtk',
      version='beta',
      description='A Gnome Frontend for Statistical Analysis in R',
      author='Stephen Diehl',
      author_email='sdiehl@clarku.edu',
      url='http://code.google.com/p/rpygtk/',
      packages=['rpygtk'],
      package_data = {'rpygtk' : rpygtk_files },
      requires=['numpy','rpy2'],
      data_files=[('/usr/bin/', ['./rpygtk/bin/rpygtk']),('/usr/share/applications/', ['./rpygtk/rpygtk.desktop'])]
      )
