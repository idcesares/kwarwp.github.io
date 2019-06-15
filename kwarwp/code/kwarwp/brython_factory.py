#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Kwarwp
# Copyright 2010-2018 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://j.mp/GNU_GPL3>`__.
#
# Kwarwp é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

"""Brython front end client.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
import sys
import traceback
from random import choice, random
from math import pi

from .kuarup import Kuarup

# seed(27356)
random()
IMAGEREPO = '/image/'
CANVASW, CANVASH = 800, 600
NODICT = {}
EDIT = "{}/{}".format(IMAGEREPO, "sun.gif")
EDTST = {'position': 'relative', 'padding': 10, 'margin': '0', 'flex': '3 1 auto',
         'width': '99%', 'resize': 'none', 'borderColor': 'darkslategrey',
         'color': 'navajowhite', 'border': 1, 'background': 'rgba(10, 10, 10, 0.5)'}
ERRST = {'position': 'relative', 'padding': 10, 'margin': '0', 'visibility': 'visible', 'flex': '1',
         'width': '99%', 'min-height': '30%', 'resize': 'none', 'borderColor': 'darkslategrey',
         'color': 'navajowhite', 'border': 1, 'background': 'rgba(200, 54, 54, 0.5)'}

#############################################################################

"""
page up 	33
page down 	34
end 	35
home 	36
left arrow 	37
up arrow 	38
right arrow 	39
down arrow 	40
insert 	45

"""


class Queue:
    def __init__(self):
        self.queue = []
        self.resolved = self.val = lambda *_: None

    def pop(self):
        if self.queue:
            yield self.queue.pop(0)
        else:
            yield lambda *_: None

    def push(self, item):
        self.queue.append(item)

    def flush(self):
        self.queue = []

    def run(self):
        while self.pop():
            pass


class TECLA:
    ACIMA = 38
    ABAIXO = 40
    DIREITA = 39
    ESQUERDA = 37

    BRANCO = 32
    ENTER = 13
    SOBE = 33
    DESCE = 34
    EMPURRA = 35
    PUXA = 36


DIALOGS = [('black', 20, 80, 760, 500), ('red', 20, 380, 760, 200)]


class Dialog:
    def __init__(self, gui, text='xxxx', act=lambda x: None, kind=0):

        divat = {'position': 'absolute', 'top': 64, 'left': 0, 'display': 'flex', 'padding': '7px',
                 'flex-direction': 'column', 'align-items': 'stretch',
                 'width': '786px', 'height': '536px', 'background': 'rgba(10, 10, 10, 0.85)'}
        background, *dimensions = DIALOGS[kind]
        self.text = text
        self.gui = gui
        self.html, self.dom = gui.html, gui.dom
        self._div = self._err = self._area = None
        self._div = self._div if self._div else self.html.DIV(style=divat)
        self.dom <= self._div
        # self._rect = gui.back(0, 66, 800, 540, background, '0.85')
        text = text if text else self.text
        self._area = self.textarea(text, style=EDTST)
        self._set_code(text)
        # self.set_err(text)
        self.edit = gui.edit
        gui.continua, self.continua = lambda *_: None, gui.continua
        gui.edit = self.action
        self.act = act

    def _set_code(self, text=None):
        self._div <= self._area
        self.__area = self.gui.window.CodeMirror.fromTextArea(
            self._area, dict(mode="python", theme="solarized", lineNumbers=True))
        self._doc = self.__area.getDoc()

    def textarea(self, text, style=EDTST):
        def dpx(d):
            return '%spx' % d
        # divat = {'position': 'absolute', 'top': dpx(y), 'left': dpx(x),
        #          'width': dpx(w), 'height': dpx(h), 'background': 'rgba(10, 10, 10, 0.85)'}
        t = self.html.TEXTAREA(text, style=style)
        return t

    def remove(self):
        self._div.remove()
        # self._area.remove()

    def hide(self):
        self.remove()
        # self._rect.style.visibility = 'hidden'
        # self._area.style.visibility = 'hidden'

    def show(self):
        # self._rect.style.visibility = 'visible'
        # self._set_code()
        # self._area.style.visibility = 'visible'
        self._div.style.visibility = 'visible'

    def _update_text(self):
        self.text = self._area.value
        return self.text

    def get_text(self):
        self.__area.save()
        self.text = ''
        return self.text if self.text else self._update_text()

    def set_err(self, text):
        self._err.remove() if self._err else None
        self._err = self.textarea(text, style=ERRST)
        self._div <= self._err
        self.text = ''
        error = text
        lines = error.split(' line ')
        if len(lines) > 1:
            try:
                line = int(lines[-1].split("\n")[0])
                error = error.split("\n")[-2]
                h = self._doc.setSelection(dict(line=line-1, ch=0), dict(line=line-1, ch=60))
            except Exception as x:
                print("Exception", x)

    def del_err(self):
        self._err.remove() if self._err else None
        self._err = None

    def set_text(self, text):
        self._area.value = text

    def action(self, event=None):
        self.text = self._area.value
        self.hide()
        self.gui.edit = self.edit
        self.gui.continua = self.continua
        self.act(self)


class EmpacotadorDeImagem:
    def __init__(self, canvas, glyph, x, y, dx, dy):
        self.canvas = canvas.svg  # .canvas
        self.render = canvas
        self.img = self.canvas.image(
            href=IMAGEREPO + glyph, x=x, y=y,
            height="{}px".format(dy), width="{}px".format(dx))
        self.x, self.y = x, y

    def __le__(self, other):
        other <= self.img

    def do_remove(self):
        self.img.remove()

    def remove(self):
        pass
        self.render.renderer(self.img, render=lambda: self.do_remove())

    def do_move(self, x, y, image=None):
        self.img.x, self.img.y = x, y
        if image:
            self.img.href.baseVal = IMAGEREPO + image

    def mover(self, x, y, image=None, *_, **__):
        self.x, self.y = x, y
        self.render.renderer(self.img, render=lambda: self.do_move(x, y, image))

    def do_translate(self, x, y):
        self.x, self.y = self.x + x, self.y + y
        self.img.x, self.img.y = self.x, self.y

    def translate(self, x, y):
        self.render.renderer(self.img, render=lambda: self.do_translate(x, y))


class _GUI:
    def __init__(self, width, height, svg=None, doc=None, html=None,
                 win=None, sto=None, cena=None, code=None,  codename=None, **kw):
        self.current_text = None
        self.wsize = dict(width=width, height=height)
        self.queue = Queue()
        self.mundo_Kuarup = self.evs = self.o_indio = None
        self.svg, self.html, self.cena, self.code, self.window = svg, html, cena, code, win
        self.storage,  self.codename = sto,  codename
        self.evs = [getattr(TECLA, at) for at in dir(TECLA) if at.isupper()]
        doc["svgdiv"].remove()
        self.svgpanel = svg.svg(id="svgdiv", width=width, height=height)
        doc["pydiv"] <= self.svgpanel
        self.panel = doc["svgdiv"]
        self.dom = doc["pydiv"]
        self.document = doc
        self.events = {}
        self.edit = self._edit
        self.dialogue = None

    def keyCode(self, ev):
        if ev.keyCode in self.evs:
            self.mundo_Kuarup.quandoApertaUmaTecla(ev.keyCode)
            ev.stopPropagation()

    def inicia(self, mundo, dx=0):
        self.wsize.update(width=dx) if dx else None
        self.current_text.remove() if self.current_text else None
        self.current_text = None
        self.panel.remove()
        # self.svgpanel = self.svg.svg(id="svgdiv", **self.wsize)
        self.dom <= self.svgpanel
        self.panel = self.document["svgdiv"]
        self.mundo_Kuarup = mundo
        self.document.bind("keypress", lambda ev: self.keyCode(ev))
        # print("def inicia(self, mundo):", self.evs, mundo)

    def do_text(self, x, y, texto, color='navajowhite'):
        self.current_text.remove() if self.current_text else None
        # x = self.wsize["width"]
        # x //= 2
        self.current_text = img = self.svg.text(
            texto, x=x, y=y,
            font_size=22, text_anchor="middle",
            style={"stroke": color, "fill": color})
        self.panel <= img

    def text(self, x, y, texto, color='navajowhite'):
        self.renderer(None, render=lambda: self.do_text(x, y, texto, color))

    def renderer(self, img, render=None):
        if False:
            self.panel <= img

    def __render(self, img):
        def do_render(img):
            self.panel <= img

        self.queue.push(lambda: do_render(img))

    def back(self, x, y, dx, dy, color, opacity="1.0"):
        rec = self.svg.rect(x=x, y=y, width=dx, height=dy, stroke=color, fill=color,
                            style=dict(fillOpacity=opacity, visibility="visible"))
        self.panel <= rec
        return rec

    def rect(self, x, y, dx, dy, color, opacity="1.0"):
        img = self.svg.rect(x=x, y=y, width=dx, height=dy, stroke=color, fill=color,
                            style={'fillOpacity': opacity})
        # img.setAttribute('class', 'arena')
        self.renderer(img)
        return img

    def executa_acao(self, dialog):
        pass

    def _edit(self, *_):
        self.dialog("", act=self.executa_acao)

    def editor(self, glyph):
        glyph.bind('click', lambda *_: self._edit)

    def image(self, glyph, x, y, dx, dy):
        img = EmpacotadorDeImagem(self, glyph, x, y, dx, dy)
        if "sun.gif" in glyph:
            img.img.bind('click', lambda *_: self.edit())
            self.editor(img.img)
        if "sky." in glyph:
            img.img.bind('click', lambda *_: self.mundo_Kuarup.indio.luzes_camera_acao())
            self.editor(img.img)
        self.renderer(img.img)
        return img

    def escolha(self, lista):
        # seed(3456)
        random()
        return choice(lista)

    def textarea(self, text, x, y, w, h, style=EDTST):

        def dpx(d):
            return '%spx' % d

        attrs = {'position': 'relative', 'padding': 10, 'margin': "2%",
                 'width': '96%', 'height': '100%', 'resize': 'none', 'borderColor': 'darkslategrey',
                 'color': 'navajowhite', 'border': 1, 'background': 'rgba(200, 54, 54, 0.5)'}
        divat = {'position': 'absolute', 'top': 64, 'left': 0,
                 'width': '800px', 'height': '536px', 'background': 'rgba(10, 10, 10, 0.85)'}
        # divat = {'position': 'absolute', 'top': dpx(y), 'left': dpx(x),
        #          'width': dpx(w), 'height': dpx(h), 'background': 'rgba(10, 10, 10, 0.85)'}
        d = self.html.DIV(style=divat)
        t = self.html.TEXTAREA(text, style=style)
        d <= t
        self.dom <= d
        return t

    def dialog(self, text=None, img=EDIT, act=lambda x: None):
        text = text if text else self.code
        if self.dialogue:
            self.dialogue.remove()
        self.dialogue = Dialog(self, text=text, act=act)
        self.dialogue.set_text(text)
        self.dialogue.show()
        return self.dialogue

    def continua(self):
        pass


class GUI(_GUI):
    """ O terreno onde o Festival Kuarup é apresentado
    """
    def __init__(self, reloader, width=CANVASW, height=CANVASH, **kwargs):
        _GUI.__init__(self, width=width, height=height, **kwargs)
        self.executante, self.reloader = None, reloader
        self.queue = Queue()
        self.renderer = self.do_render

    def do_reload(self, alert=False):
        self.queue.flush()
        self.reloader(alert=alert)

    def reload(self):
        self.queue.push(lambda: self.do_reload(True))

    def run(self):
        self.executante()

    def do_render(self, img, render=None):
        render() if render else self.panel <= img

    def _renderer(self, render=None):
        self.queue.push(lambda: render())

    def _render(self, img, render=None):
        self.queue.push(lambda: render() if render else self.do_render(img))

    def _first_response(self, dialog, action):
        class ConsoleOutput:

            def __init__(self):
                self.value = ''

            def write(self, data):
                self.value += str(data)

            def flush(self):
                self.value = ''
                pass

        value = self.value = ConsoleOutput()
        sys_out, sys.stdout = sys.stdout, value
        sys_err, sys.stderr = sys.stderr, value
        # logger('first response %s %s %s' % (dialog, sys.stdout, sys.stderr))
        # TODO action += self.challenge[1]
        # logger('first response code %s' % action)
        try:
            action()
        except Exception as err:
            # except Exception as err:
            traceback.print_exc(file=sys.stderr)
            sys.stdout = sys_out
            sys.stderr = sys_err
            dialog = self.dialog(self.code, act=self.executa_acao)  # +str(self.value.value))
            dialog.set_err(str(self.value.value))
        else:
            self.code = dialog.get_text()
            pass
        sys.stdout = sys_out
        sys.stderr = sys_err

    def _executa_acao(self):
        self.queue.flush()
        exec(self.code, globals())
        self.o_indio = Tchuk(self.cena, indio=Tchuk, gui=self)
        self.o_indio.inicia()

    def executa_acao(self, dialog):
        self.code = dialog.get_text()
        self.storage[self.codename] = self.code
        self.renderer = self._render
        self.renderer = self.do_render
        self._first_response(dialog, self._executa_acao)

    def _registra_executante(self, executante):
        executante()

    def registra_executante(self, executante):
        self.renderer = self._render
        self.executante = executante
        self._first_response(self.dialogue, executante)

    def espera(self):
        pass

    def continua(self):
        # print("def continua(self):", len(self.queue.queue))
        self.queue.pop().__next__()()
