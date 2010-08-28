# Copyright 2009-2010 Stephen Diehl
#
# This file is part of RPyGTK and distributed under the terms
# of the GPLv3 license. See the file LICENSE in the RPyGTK
# distribution for full details.

import gtk
import pango

class FormulaAssistedEntry(gtk.Entry):
    words = []
    
    def __init__(self,*args,**kwargs):
        
        gtk.Entry.__init__(self,*args,**kwargs)
        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        
        textbuffer.connect('insert-text',self.move_to)
        
        font_desc = pango.FontDescription('sans 15')
        textview.modify_font(font_desc)
        textview.set_property('justification',gtk.JUSTIFY_CENTER)
        
        textview.show()
        
        self.widget = textview
        self.buffer = textbuffer
        
    def move_to(self,textbuffer, position, text, length):
        highlight = gtk.TextTag()
        highlight.set_property('size-points',15)
        
        if text == '(':
            textbuffer.insert(position,' ')
            position.forward_chars(1)
            textbuffer.insert(position,')')
            position.backward_chars(2)
            textbuffer.place_cursor(position)
            
        if text == '^':
            textbuffer.insert(position,'()')
            position.backward_chars(2)
            textbuffer.place_cursor(position)

        if text == '{':
            textbuffer.insert(position,' ')
            position.forward_chars(1)
            textbuffer.insert(position,'}')
            position.backward_chars(2)
            textbuffer.place_cursor(position)
            
    def set_text(self,text):
        self.buffer.set_text(text)
        
    def get_text(self):
        return self.buffer.get_text(*self.buffer.get_bounds())