#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Canvas Factory : Gui interface to Html Canvas
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2012/03/17  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2012, `GPL <http://is.gd/3Udt>`__. 
"""
__author__ = "Carlo E. T. Oliveira (carlo@ufrj.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__ = "2012/03/04 $Date$"

# The following is provided for the convenience of end users.
import re

from .colors import COLOR


# variable that start with "_" are not displayed in Crunchy's "help";
# we use this feature to only expose a small number of them to the user.
class _NOOP:
    def plugin(self, *args): return None


try:
    import src.interface as gi

    _exec = gi.plugin['exec_js']
    _page = gi.plugin['get_pageid']
    _uid = gi.plugin['get_uid']
except:

    gi = _NOOP()
    _exec = gi.plugin
    _page = lambda *a: None
    _uid = lambda *a: None
    # _exec = lambda *a : None
    # _page = lambda *a : None
    # _uid = lambda *a : None
    pass

#
# logger = logging.getLogger('myapp')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.CRITICAL)
# logger.setLevel(logging.INFO)

CANVASW, CANVASH = 400, 480
_REF = 'document.getElementById("%s").'
_CTX = _REF + 'getContext("2d").'
PARENT = 'parent'
IDF = 'idf'
SVGFONT = """font-size font-style font-weight line-height letter-spacing
word-spacing letter-spacing text-anchor text-decoration textLength
lengthAdjust font-family baseline-shift dy """
SVGSTYLE = (SVGFONT + """fill color stroke stroke-width stroke-opacity stroke-dasharray
fill-opacity stroke-linecap stroke-linejoin hexcolor""").replace('-', '_').split()


class _Base(object):
    __next_free = 0

    def __init__(self, tagname, document=None, **kwargs):
        "Creates an element with the specified tag name, parent and arguments"
        self.document = document or _DOC
        self._var = kwargs.pop(IDF, self._freevar())
        if tagname:
            elem = self._create_element(tagname, **kwargs)
            self.parent = elem.parent
        self._var = tagname and elem.var or self._var

    def _create(self, code, **kwargs):
        self._var = kwargs.pop(IDF, None) or self._freevar()
        code += '; %s.setAttribute("id", "%s"); '
        code = self.add_attrs(code, **kwargs)
        arguments = (self.var, self.var, self.var)
        _exec(_page(), code)  # %arguments)
        kwargs.pop(PARENT, None)

    def _freevar(self):
        """returns a variable name guaranteed to be free"""
        _Element.__next_free += 1
        return 'a' + str(self.__next_free)

    def exec_jscript(self, code, *args):
        arguments = (self.var,) + args
        _exec(_page(), code % arguments + ";")

    def _create_element(self, tagName, **kwargs):
        "Creates an element with the specified tag name"
        svgns = 'http://www.w3.org/2000/svg';
        create_element = 'document.createElementNS("%s", "%s")' % (svgns, tagName)
        if tagName == 'text':
            value = kwargs.pop('value', '')
            create_text = 'var textvalue = ' + \
                          'document.createTextNode("%s", true);' % value
            create_text += '%s.appendChild(textvalue);'
            create_element = 'var %s = ' + create_element
            element = _Script(create_element, _is_text_=create_text, **kwargs)
        else:
            element = _Script('var %s = ' + create_element, **kwargs)
        # element = self._create('var %s = ' + create_element, **kwargs)

        return element

    def _getElementById(self, idf):
        "Returns an object reference to the identifed element"
        v = self._freevar()
        self.exec_jscript('var %s = document.getElementById("%s")' % (v, idf))
        return _Element(None, idf=idf, document=self)

    def _appendChild(self, child):
        self.exec_jscript(_REF + 'appendChild(%s)', _REF[:-1] % child.var)

    def _set_innerHTML(self, val):
        self.exec_jscript(_REF + 'innerHTML= "%s"' % val)

    def _add_attr(self, code, name, val):
        if name is 'href':
            name = 'xlink:href'
            space = 'NS("http://www.w3.org/1999/xlink","%s", "%s");'
        else:
            space = '("%s", "%s");'
        return code + ('%s.' + 'setAttribute%s' % space) % (self.var, name, val)

    innerHTML = property(None, _set_innerHTML)

    def _set_var(self, var):
        self.set_attr("id", var)
        self._var = var

    def _get_var(self):
        return self._var

    var = property(_get_var, _set_var)


class _Element(_Base):
    def set_attr(self, name, val):
        if name is 'href':
            name = 'xlink:href'
            space = 'NS("http://www.w3.org/1999/xlink","%s", "%s")'
        else:
            space = '("%s", "%s")'
        self.exec_jscript(_REF + 'setAttribute%s' % space, name, val)

    def attr(self, name, val):
        self.exec_jscript(_REF + '%s = "%s"', name, val)

    def add_attrs(self, code, **kwargs):
        return ' '.join(self._add_attr(code, name, val) for name, val in kwargs.items())
        for name, val in kwargs.items():
            self.set_attr(name, val)

    def attrs(self, **kwargs):
        for name, val in kwargs.items():
            self.set_attr(name, val)

    def move(self, x, y):
        self.attrs(x=x, y=y)

    def remove(self):
        _exec(_page(),
              """var divCanvas = document.getElementById("%s");
              divCanvas.removeChild(document.getElementById("%s"));
              """ % (self.parent.var, self.var))

    def translate(self, x, y):
        self.exec_jscript('%s = ' + _REF + 'createSVGTransform();' +
                          '%s.setTranslate(%d,%d)', self.var, self.var, x, y)


class _Script(_Element):
    def __init__(self, code, **kwargs):
        self.document = _DOC
        self._var = kwargs.pop(IDF, None) or self._freevar()
        self.parent = kwargs.pop(PARENT, self)
        is_text = kwargs.pop('_is_text_', '')
        att = self.add_attrs('', **kwargs)
        varlist = (self.parent.var, self._var)
        varlist += is_text and (self._var,) or ()
        code += '; %s.setAttribute("id", "%s"); ' + att
        code += (' document.getElementById("%s").appendChild(%s); ' +
                 is_text) % varlist
        arguments = (self.var, self.var, self.var)
        # print '\n inicio \n%s\nfim'%code
        _exec(_page(), code % arguments)
        kwargs.pop(PARENT, None)


class _Document(_Element):
    def __init__(self):  # tested indirectly
        self.__next_free = 0
        self.__uids = []

    def get_uid(self):
        uid = _uid()
        if not uid in self.__uids:
            self.__uids.append(uid)
        return uid

    def _get_uids(self):
        return self.__uids

    def exec_jscript(self, code):
        """ code = javascript code to be executed"""
        # print code
        _exec(_page(), code + ";")

    def _get_body(self):
        return _Element(self, "document.body")

    body = property(_get_body, None)
    "body: returns the BODY node of the document"

    uids = property(_get_uids, None)


_DOC = _Document()


class Image(_Element):
    def __init__(self, href, x, y, **kwargs):
        _Element.__init__(self, 'image', href=href, x=x, y=y, **kwargs)


class Rect(_Element):
    def __init__(self, x, y, width, height, **kwargs):
        _Element.__init__(self, 'rect', x=x, y=y, width=width, height=height, **kwargs)


class Text(_Element):
    def __init__(self, x, y, value, **kwargs):
        _Element.__init__(self, 'text', x=x, y=y, value=value, **kwargs)
        # self.innerHTML = value

    def _set_value(self, value):
        self.innerHTML = value

    value = property(None, _set_value)


class Arc(_Element):
    def __init__(self, cx, cy, rx, ry, **kwargs):
        _Element.__init__(self, 'ellipse', cx=cx, cy=cy, rx=rx, ry=ry, **kwargs)


tst = """var a8 = document.createElementNS("http://www.w3.org/2000/svg", "image"); a8.setAttribute("id", "a8"); a8.setAttribute("y", "2"); a8.setAttribute("x", "100"); a8.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href", "/images/tchuk.gif"); 
document.getElementById("svg_%s").appendChild(a8);
"""

tst = """var a12 = document.createElementNS("http://www.w3.org/2000/svg", "image"); a12.setAttribute("id", "a12"); 
a12.setAttribute("y", "2");
a12.setAttribute("width", "30");
a12.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href", "/images/tchuk.gif");
a12.setAttribute("height", "40");
a12.setAttribute("x", "100");
document.getElementById("svg_%s").appendChild(a12);
"""
wtst = """var a12 = document.createElementNS("http://www.w3.org/2000/svg", "rect"); a12.setAttribute("id", "a12"); a12.setAttribute("y", "2"); a12.setAttribute("width", "3"); a12.setAttribute("style", "fill:#228B22"); a12.setAttribute("x", "1"); a12.setAttribute("height", "4"); document.getElementById("svg_%s").appendChild(a12); 
"""
wtst = 'var ux_22 = %s'


class GUI(_Element):
    _UIDS = []

    def __init__(self, width=CANVASW, height=CANVASH, idf=None):  # tested
        """dynamically creates a graphics canvas, with the origin at the top
        left cornder by default.  Use origin=bottom to have the origin at the
        bottom left corner, like in mathematics.
        """
        uid = _uid()
        uids = self._UIDS
        self._var = 'svg_%s' % uid
        self._elements = []
        if uid not in uids:  # dynamically create a canvas
            uids.append(uid)
            # parent = _DOC._getElementById("div_%s"%uid)
            # self.canvas = _DOC.create_child("canvas",parent)
            # self.canvas.var = "canvas_%s"%uid

            _exec(_page(),
                  """var divCanvas = document.getElementById("div_%s");
                  newSvg = document.createElementNS("http://www.w3.org/2000/svg","svg");
                  newSvg.setAttribute("id", "svg_%s");
                  divCanvas.appendChild(newSvg);
                  """ % (uid, uid))
        self.canvas = _DOC._getElementById("svg_%s" % uid)
        self.canvas.attrs(width=width, height=height)
        self.canvas.attr("style.display", "block")

    def _get_var(self):
        return self._var

    var = property(_get_var, None)

    def _paint(self, drawing, *args):
        command = "var %s = " + _CTX + drawing
        arguments = (self.canvas.var,) + args
        return _Script(command, *arguments)

    def _script(self, command, *args):
        command = _CTX + command
        arguments = (self.canvas.var,) + args
        _DOC.exec_jscript(command % arguments)

    def text(self, x, y, texto, color='black', hexcolor=None, **kwargs):
        """ Creates and returns a Text
        x,y - position; value - text to be written
        font_size - Font height, default(12)
        text-anchor - Relative position [start middle end]
        text-decoration - text effects [none underline overline line-through blink]
        stroke_width - border size
        fill_opacity - tranparency  0.0 .. 1.0
        stroke_opacity - border tranparency  0.0 .. 1.0
        fill = inside color, default(#000000 or COLOR.black or 'black')
        stroke - border color, default(#000000 or COLOR.black or 'black')
        """
        parent = kwargs.pop(PARENT, self)
        style = self._style(**kwargs)
        for k in SVGSTYLE: kwargs.pop(k, None)
        element = Text(x=x, y=y, value=texto, parent=parent,
                       style=style, **kwargs)
        self._elements.append(element)
        return element

    def _style(self, **kwargs):
        """
        fill = inside color, default(#000000 or COLOR.black or 'black')
        stroke - border color, default(#000000 or COLOR.black or 'black')
        """
        hexcolor = kwargs.pop('hexcolor', None)
        color = kwargs.pop('color', None)
        fill = kwargs.pop('fill', None) or color or hexcolor
        kwargs['fill'] = validate_colour(fill)
        stroke = kwargs.pop('stroke', None)
        dash = kwargs.pop('stroke_dasharray', '')
        dash = dash and ';stroke-dasharray:%d,%d' % dash
        if stroke:
            kwargs['stroke'] = validate_colour(stroke)
        return ';'.join('%s:%s' % (key.replace('_', '-'), value)
                        for key, value in kwargs.items() if key in SVGSTYLE) + dash

    def rect(self, x, y, w, h, **kwargs):
        """ Creates and returns a Rectangle
        x,y - position; w,h - size
        rx, ry - rounded rect radius 
        stroke_width - border size
        fill_opacity - tranparency  0.0 .. 1.0
        stroke_opacity - border tranparency  0.0 .. 1.0
        fill = inside color, default(#000000 or COLOR.black or 'black')
        stroke - border color, default(#000000 or COLOR.black or 'black')
        """
        parent = kwargs.pop(PARENT, self)
        style = self._style(**kwargs)
        for k in SVGSTYLE: kwargs.pop(k, None)
        element = Rect(x=x, y=y, width=w, height=h, parent=parent,
                       style=style, **kwargs)
        self._elements.append(element)
        return element

    def arc(self, x, y, rx, ry, **kwargs):
        """ Returns a Rectangle
        x,y - position
        rx, ry - radius x and y
        start, end - arc limits in radians
        open = if arc is open, default(False)
        stroke_width - border size
        fill_opacity - tranparency  0.0 .. 1.0
        stroke_opacity - border tranparency  0.0 .. 1.0
        fill = inside color, default(#000000 or COLOR.black or 'black')
        stroke - border color, default(#000000 or COLOR.black or 'black')
        """
        parent = kwargs.pop(PARENT, self)
        style = self._style(**kwargs)
        for k in SVGSTYLE: kwargs.pop(k, None)
        element = Arc(cx=x, cy=y, rx=rx, ry=ry, parent=parent,
                      style=style, **kwargs)
        self._elements.append(element)
        return element

    def clear(self):
        _exec(_page(),
              """var divCanvas = document.getElementById("svg_%s");
              il=divCanvas.getElementsByTagName('svg');
              for(i=0;i<il.length;i++)
              { divCanvas.removeChild(il[i]); };
              """ % (uid, uid))

    def image(self, href, x, y, w, h, **kwargs):
        """ Returns an Image
        x,y - position; w,h - size
        """
        parent = kwargs.pop(PARENT, self)
        return Image(href, x=x, y=y, width=w, height=h, parent=parent, **kwargs)


named_colour = re.compile('^[a-zA-Z]*[a-zA-Z]$')
hex_code = re.compile('^#[a-fA-F0-9]{5, 5}[a-fA-F0-9]$')


def validate_colour(colour):  # tested
    """verifies that the colour given follows an acceptable pattern"""
    named_colour = re.compile('^[a-zA-Z]* *[a-zA-Z]*[a-zA-Z]$')
    hex_code = re.compile('^#[a-fA-F0-9]{5,5}[a-fA-F0-9]$')
    if not colour: return COLOR.black
    if hex_code.match(colour):
        assert 0 <= int(colour[1:], 16) < 0xFFFFFF, "Cor inexistente %s" % int(colour[1:], 16)
        return colour
    elif named_colour.match(colour):
        return COLOR[colour]
    else:
        return COLOR.black


try:
    from mock import Mock
except:
    pass
import unittest

CALL = 'ex'


class _TestPaintWithGui(unittest.TestCase):
    """can paint with gui"""

    def _find(self, call, reset=False, anything=False):
        self._callings = [called for called in self.js.method_calls
                          if anything or call == called[0]]
        reset and self.js.reset_mock()
        return self._callings

    def _find_all(self, call, *items):
        # items = isinstance(items,list) and items or [items]
        anything = call or True
        self._callings = ''.join([str(called) for called in self.js.method_calls
                                  if anything or call == called[0]])
        self._items = [item in self._callings for item in items]
        return self._items

    def _count(self, call, reset=False, anything=False):
        self._counting = len(self._find(call, reset=reset, anything=anything))
        return self._counting

    def _assert_count(self, count, call=CALL, reset=False, anything=False):
        calls = self._find(call, reset=reset, anything=anything)
        assert count == len(calls) \
            , "instead call count was %d at: %s" % (len(calls), calls)

    def setUp(self):
        global _exec, _page, _uid
        self.js = Mock()
        _exec = lambda *a: self.js.ex(*a)
        _page = lambda *a: 0
        _uid = lambda *a: 0  # self.js.ui(*a)
        self.app = GUI()
        self.js.reset_mock()

    def tearDown(self):
        self.js.reset_mock()
        self.app = None
        GUI._UIDS = []

    def test_validate_color(self):
        "testa validação de cor"
        color = validate_colour('#FF0000')
        assert color == '#FF0000', 'Else color was %s' % color
        color = validate_colour('Red')
        assert color == '#FF0000', 'Else color was %s' % color
        color = validate_colour(COLOR.red)
        assert color == '#FF0000', 'Else color was %s' % color
        color = validate_colour('#FF00000')
        assert color == '#000000', 'Else color was %s' % color
        color = validate_colour('navajo white')
        assert color == '#FFDEAD', 'Else color was %s' % color

    def test_style_creation(self):
        "testa validação de cor"
        fill = dict(hexcolor='#00FF00')
        style = self.app._style(**fill)
        # assert not fill, 'Else fill was %s'%fill
        assert style == 'fill:#00FF00', 'Else green was %s' % style
        fill = dict(fill='red')
        style = self.app._style(**fill)
        # assert not fill, 'Else fill was %s'%fill
        assert style == 'fill:#FF0000', 'Else red was %s' % style

    def test_create_Gui(self):
        "testa se cria a GUI"
        self.js.reset_mock()
        GUI._UIDS = []
        self.app = GUI()
        items = self._find_all(CALL,
                               '"id", "svg_0', 'appendChild(newSvg',
                               '("width", "400"', 'getElementById("svg_0")')
        assert all(items), 'but %s' % items
        self._assert_count(5)

    def test_create_Gui_second_time(self):
        "testa se cria a GUI na segunda vez"
        self.js.reset_mock()
        GUI._UIDS = []
        self.app = GUI()
        self._assert_count(5, reset=True)
        self.app = GUI()
        self._assert_count(4)

    def test_create_image(self):
        "testa se cria uma imagem"
        img = self.app.image("/images/tchuk.gif", 1, 2, 30, 40)
        items = self._find_all(CALL,
                               'eElementNS("http://www.w3.org/2000/svg", "image")',
                               'setAttributeNS("http://www.w3.org/1999/',
                               'xlink","xlink:href", "/images/tchuk.gif"', '("x", "1")',
                               'e("width", "30")', '')
        assert all(items), 'but %s' % items
        self._assert_count(1)

    def test_create_rect(self):
        "testa se cria um retangulo"
        rect = self.app.rect(1, 2, 3, 4)
        canvas_id = 'ById("%s")' % self.app.var
        items = self._find_all(CALL, canvas_id, '"style", "fill:#000000"',
                               'eElementNS("http://www.w3.org/2000/svg", "rect"', '("y", "2")',
                               'e("width", "3")', 'e("height", "4")', '')
        assert all(items), 'but %s' % items
        self._assert_count(1)

    def test_create_red_rect(self):
        "testa se cria um retangulo vermelho"
        rect = self.app.rect(1, 2, 3, 4, fill=COLOR.red)
        canvas_id = 'ById("%s")' % self.app.var
        items = self._find_all(CALL, canvas_id, '"style", "fill:#FF0000"',
                               'eElementNS("http://www.w3.org/2000/svg", "rect"', '("y", "2")', )
        assert all(items), 'but %s' % items
        self._assert_count(1)

    def test_create_decorated_rect(self):
        "testa se cria um retangulo decorado"
        rect = self.app.rect(1, 2, 3, 4, fill='blue',
                             stroke='saddlebrown', stroke_width=2, fill_opacity=0.5,
                             stroke_dasharray=(5, 2), rx=2, ry=2)
        canvas_id = 'ById("%s")' % self.app.var
        items = self._find_all(CALL, canvas_id, '"style"', 'fill:#0000FF',
                               'eElementNS("http://www.w3.org/2000/svg", "rect"', '("ry", "2")',
                               'stroke:#8B4513;', 'stroke-dasharray:5,2"', 'stroke-width:2;')
        assert all(items), 'but %s' % items
        self._assert_count(1)

    def test_move_rect(self):
        "testa se move um retangulo"
        rect = self.app.rect(1, 2, 3, 4)
        rect.move(5, 6)
        items = self._find_all(CALL, 'setAttribute("y", "6");',
                               '.setAttribute("x", "5");', )
        assert all(items), 'but %s' % items
        self._assert_count(3)

    def test_translate_rect(self):
        "testa se translada um retangulo"
        rect = self.app.rect(1, 2, 3, 4)
        rect.translate(5, 6)
        r = rect.var
        items = self._find_all(CALL, '%s = document.getElementById("%s")' % (r, r), '.createSVGTransform()',
                               '.setTranslate(5,6);', )
        assert all(items), 'but %s' % items
        self._assert_count(2)

    def test_delete_rect(self):
        "testa se translada um retangulo"
        rect = self.app.rect(1, 2, 3, 4)
        r = rect.var
        rect.remove()
        items = self._find_all(CALL,
                               'document.getElementById("%s")' % (self.app.canvas.var),
                               ' divCanvas.removeChild(document.getElementById("%s"));' % r,
                               )
        assert all(items), 'but %s' % items
        self._assert_count(2)

    def test_create_arc(self):
        "testa se cria um circulo"
        rect = self.app.arc(1, 2, 3, 4)
        canvas_id = 'ById("%s")' % self.app.var
        items = self._find_all(CALL, canvas_id, '"style", "fill:#000000"',
                               'eElementNS("http://www.w3.org/2000/svg", "ellipse"', '("cy", "2")',
                               'setAttribute("rx", "3");', 'setAttribute("ry", "4");')
        assert all(items), 'but %s' % items
        self._assert_count(1)

    def test_create_text(self):
        "testa se cria um texto"
        text = self.app.text(1, 2, 'ola')
        canvas_id = 'ById("%s")' % self.app.var
        items = self._find_all(CALL, canvas_id, '"style", "fill:#000000"',
                               'eElementNS("http://www.w3.org/2000/svg", "text"',
                               '.setAttribute("y", "2")', '.createTextNode("ola"',
                               '%s.appendChild(textvalue);' % text.var)
        assert all(items), 'but %s' % items
        self._assert_count(1)


if __name__ == '__main__':
    unittest.main()
