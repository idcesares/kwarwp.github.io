#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Canvas Factory : Gui interface to Html Canvas
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2012/03/04  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2012, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (carlo@ufrj.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2012/03/04 $Date$"

# The following is provided for the convenience of end users.
import re
from os.path import join as join_path

# variable that start with "_" are not displayed in Crunchy's "help";
# we use this feature to only expose a small number of them to the user.
import random as _random
try:
    from src.interface import plugin as _plugin
    _exec = _plugin['exec_js']
    _page = _plugin['get_pageid']
    _uid = _plugin['get_uid']
except:
    pass

#
#logger = logging.getLogger('myapp')
#logger.addHandler(logging.StreamHandler())
#logger.setLevel(logging.CRITICAL)
#logger.setLevel(logging.INFO)

CANVASW, CANVASH = 400, 480
COLOR={'forest green':'#228B22' , 'navajo white':'#FFDFB0', 'white':'#FFFFFF'
        ,'darksalmon':'#E9967A', 'peachpuff':'#FFDAB9', 'maroon':'#800000'
        ,'lightsalmon':'#FFA07A', 'saddlebrown':'#8B4513'
        ,'darkbrown':'#462813','linen':'#FAF0E6'}

_REF ='document.getElementById("%s").'
_CTX =_REF + 'getContext("2d").'

class _Document(object): 
    def __init__(self): # tested indirectly
        self.__next_free = 0
        self.__uids = []
    def get_uid(self):
        uid = _uid()
        if not uid in self.__uids:
            self.__uids.append(uid)
        return uid
    def _get_uids(self):
        return self.__uids
    def _freevar(self):
        """returns a variable name guaranteed to be free"""
        self.__next_free += 1
        return 'a' + str(self.__next_free)
    def exec_jscript(self, code):
        """ code = javascript code to be executed"""
        #print code
        _exec(_page(), code + ";")
    
    def _get_body(self):
        return _Element(self, "document.body")
    body = property(_get_body, None)
    "body: returns the BODY node of the document"
    
    def create_element(self, tagName, idf = None):
        "Creates an element with the specified tag name"
        v = idf or self._freevar()
        return _Script('var %s = document.createElement("%s")',tagName)
        self.exec_jscript('var %s = document.createElement("%s")' % (v, tagName))
        return _Element(v, self)
    
    def getElementById(self, idf):
        "Returns an object reference to the identifed element"
        v = self._freevar()
        self.exec_jscript('var %s = document.getElementById("%s")' % (v, idf))
        return _Element(idf, self)

    def create_child(self, tagName, parent, idf = None):
        v = idf or self._freevar()
        element = _DOC.create_element(tagName, v)
        parent.appendChild(element)
        return element
    uids = property(_get_uids, None)

_DOC = _Document()
        
class _Element(object):
    def __init__(self, var = None, document = _DOC):
        self.document = document
        self._var = var or _DOC._freevar()
    def exec_jscript(self, code, *args):
        arguments = (self._var,) + args
        _exec(_page(), code%arguments + ";")
    
    def appendChild(self,child):
        self.exec_jscript(_REF+'appendChild(%s)',_REF[:-1]%child.var)
        
    def _set_innerHTML(self, val):
        self.exec_jscript(_REF+'innerHTML= "%s"' % val)
    def set_attr(self, name, val):
        self.exec_jscript(_REF+'setAttribute("%s", "%s")'  ,name, val)
    def attr(self, name, val):
        self.exec_jscript(_REF+'%s = "%s"'  ,name, val)
    def attrs(self, **kwargs):
        for name, val in kwargs.items():
            self.exec_jscript(_REF+'%s= "%s"',name, val)
    innerHTML = property(None, _set_innerHTML)
    def _set_var(self, var):
        self.set_attr("id",var)
        self._var = var
    def _get_var(self): return self._var
    var = property(_get_var, _set_var)
    def move(self, x, y):
        self.attrs(x=x,y=y)
        
class _Script(_Element):
    def __init__(self,code, *args):
        self.document = _DOC
        self._var = _DOC._freevar()
        code += '; %s.setAttribute("id", "%s"); '
        arguments = (self.var,) + args +(self.var,self.var)
        _exec(_page(), code%arguments)
    
    

class GUI(object):
    _UIDS = []
    def __init__(self, width=CANVASW, height=CANVASH, idf = None): # tested
        '''dynamically creates a graphics canvas, with the origin at the top
        left cornder by default.  Use origin=bottom to have the origin at the
        bottom left corner, like in mathematics.
        '''
        idf = idf or _DOC._freevar()
        uid = _uid()
        uids = self._UIDS
        self.idf = 'canvas_%s'%uid
        if uid not in uids: # dynamically create a canvas
            uids.append(uid)
            #parent = _DOC.getElementById("div_%s"%uid)
            #self.canvas = _DOC.create_child("canvas",parent)
            #self.canvas.var = "canvas_%s"%uid
            
            _exec(_page(),
                """var divCanvas = document.getElementById("div_%s");
                   var newCanvas = document.createElement("canvas");
                   newCanvas.setAttribute("id", "canvas_%s");
                   divCanvas.appendChild(newCanvas);
                """%(uid, uid))
        self.canvas = _DOC.getElementById("canvas_%s"%uid)
        self.canvas.attrs(width = width, height = height)
        self.canvas.attr("style.display", "block")
        #self.ctx = _Script('var %s = '+_REF+'getContext("2d")', self.idf)
        self._paint("clearRect(%d,%d,%d,%d)", 0, 0, width, height)
        self.set_fill_colour('black')
        self.set_line_colour('black')
    def _paint(self,drawing, *args):
        command = "var %s = "+_CTX+ drawing
        arguments = (self.canvas.var,)+ args
        return _Script(command,*arguments)
    def _script(self,command, *args):
        command = _CTX + command
        arguments = (self.canvas.var,)+ args
        _DOC.exec_jscript(command%arguments)
        
    def text(self,x,y,texto,color='navajo white', hexcolor=None):
        label = self.font.render(texto, 1,  hexcolor and CL(hexcolor) or COLOR[color])
        self.buffer.blit(label, (x,y))
        return label
    def rect(self,x,y,w,h,color='navajo white', hexcolor=None, buff=None):
        return self._paint("fillRect(%d,%d,%d,%d)", x, y, w, h)

    def image(self,source,x,y,w,h):
        image_id = _DOC._freevar()
        _DOC.exec_jscript(
            """
            var pix = new Image();
            pix.src = "%s";
            var im = %sdrawImage(pix,%d,%d,%d,%d);
            im.setAttribute("id",%s)
            """ % (source,_CTX%self.canvas.var,x,y,w,h, image_id ))
        return _Element(image_id)
    def _image(self,source,x,y,w,h):
        pix = _Script("var %s = new Image()")
        pix.attrs(src = source)
        img = self._paint("drawImage(%s,%d,%d,%d,%d)", _REF[:-1]%pix.var, x,y,w,h)
        return img
    def set_line_colour(self ,col): # tested
        '''Sets the default line colour using a valid value given as a string.'''
        col =  validate_colour(col) or "DeepPink" # make it stand out for now
        self._script("strokeStyle = %r",col)
    set_line_color = set_line_colour # American spelling == British/Canadian spelling
    
    def set_fill_colour(self ,col): # tested
        '''Sets the default fill colour using a valid value given as a string.'''
        col =  validate_colour(col) or "DeepPink" # make it stand out for now
        self._script("fillStyle = %r",col)

named_colour = re.compile('^[a-zA-Z]*[a-zA-Z]$') 
hex_code = re.compile('^#[a-fA-F0-9]{5,5}[a-fA-F0-9]$') 

def validate_colour(colour): # tested
    '''verifies that the colour given follows an acceptable pattern'''
    named_colour = re.compile('^[a-zA-Z]*[a-zA-Z]$') 
    hex_code = re.compile('^#[a-fA-F0-9]{5,5}[a-fA-F0-9]$') 
    colour = colour.strip()
    if hex_code.match(colour):
        return colour
    elif named_colour.match(colour): # ; assume valid as colour name;
        return colour           # javascript would treat it as black otherwise.
    else: return False

try:
    from mock import Mock
except: pass
import unittest
CALL = 'ex'

class _TestPaintWithGui(unittest.TestCase):
    """can paint with gui"""
    def _find(self, call, reset = False, anything= False):
        self._callings = [called for called in self.js.method_calls
                 if anything or call == called[0]]
        reset and self.js.reset_mock()
        return self._callings
    def _count(self, call, reset = False, anything= False):
        self._counting = len(self._find(call,reset = reset, anything = anything))
        return self._counting
    def _assert_count(self, count, call= CALL, reset = False, anything= False):
        calls = self._find(call,reset = reset, anything = anything)
        assert count == len(calls)\
            , "instead call count was %d at: %s"%(len(calls),calls)
        
    def setUp(self):
        global _exec,_page,_uid
        self.js = Mock()
        _exec = lambda *a: self.js.ex(*a)
        _page = lambda *a: 0
        _uid = lambda *a: 0 #self.js.ui(*a)
        self.app = GUI()
        self.js.reset_mock()
   
    def tearDown(self):
        self.js.reset_mock()
        self.app = None
        GUI._UIDS = []

    def test_create_Gui(self):
        "testa se cria a GUI"
        self.js.reset_mock()
        GUI._UIDS = []
        self.app = GUI()
        self._assert_count(8)
    def test_create_Gui_second_time(self):
        "testa se cria a GUI na segunda vez"
        self.js.reset_mock()
        GUI._UIDS = []
        self.app = GUI()
        self._assert_count(8, reset= True)
        self.app = GUI()
        self._assert_count(7)
    def test_create_image(self):
        "testa se cria uma imagem"
        img = self.app.image("t.png",1,2,3,4)
        self._assert_count(30)
    def test_create_rect(self):
        "testa se cria um retangulo"
        rect = self.app.rect(1,2,3,4)
        self._assert_count(1)

if __name__ == '__main__':
    unittest.main()