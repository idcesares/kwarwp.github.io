#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Kuarup - Festival de jogos na aprendizagem de Python
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2012/03/17   $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2010, `GPL <http://is.gd/3Udt>__. 
"""
__author__ = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "1.0 $Revision$"[10:-1]
__date__ = "2012/03/16 $Date$"

import tkinter as gi
from random import choice, seed
from time import time
from threading import Event, Thread

seed()
IMAGEREPO = '../../server_root/image/'
IMAGEREPO = '/home/carlo/Dropbox/Android/igames/igames/server_root/image/'
IMAGEREPO = 'server_root/image/'
CANVASW, CANVASH = 800, 600


#############################################################################

class TECLA:
    ACIMA = 111
    ABAIXO = 116
    DIREITA = 114
    ESQUERDA = 113

    BRANCO = 65
    ENTER = 36
    SOBE = 112
    DESCE = 117
    EMPURRA = 97
    PUXA = 103


class EmpacotadorDeImagem:
    def __init__(self, canvas, glyph, x, y, dx, dy):
        self.canvas = canvas  # .canvas
        self.pi = gi.PhotoImage(file=IMAGEREPO + glyph)
        self.imageinstance = self.canvas.create_image(
            x, y, image=self.pi, anchor=gi.NW)
        self.x, self.y = x, y

    def remove(self):
        self.canvas.delete(self.imageinstance)

    def translate(self, x, y):
        self.x, self.y = self.x + x, self.y + y
        self.canvas.coords(self.imageinstance, self.x, self.y)


class _GUI:
    def __init__(self, width=CANVASW, height=CANVASH, ):
        self.top = gi.Tk()
        self.canvas = gi.Canvas(
            self.top, bg="forest green", height=height, width=width)
        self.canvas.pack()
        EVENTOS = {"<Return>": self.Return, "<space>": self.space,
                   "<Right>": self.Right, "<Left>": self.Left,
                   "<Up>": self.Up, "<Down>": self.Down,
                   "<Next>": self.Next, "<Prior>": self.Prior,
                   "<Home>": self.Home, "<End>": self.End}

        for evento, lidador in EVENTOS.items():
            self.top.bind_all(evento, lidador)

    def text(self, x, y, texto, color='navajo white'):
        self.canvas.create_text(x, y, text=texto, fill=color,
                                font=("Helvectica", "16"))  # width=0)

    def rect(self, x, y, dx, dy, color):
        self.canvas.create_rectangle(x, y, dx, dy, fill=color, width=0)

    def image(self, glyph, x, y, dx, dy):
        img = EmpacotadorDeImagem(self.canvas, glyph, x, y, dx, dy)
        return img

    def inicia(self, mundo):
        self.mundo_Kuarup = mundo
        self.top.mainloop()

    def Return(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.ENTER)

    def space(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.BRANCO)

    def Right(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.DIREITA)

    def Left(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.ESQUERDA)

    def Up(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.ACIMA)

    def Down(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.ABAIXO)

    def Next(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.DESCE)

    def Prior(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.SOBE)

    def Home(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.EMPURRA)

    def End(self, ev): self.mundo_Kuarup.quandoApertaUmaTecla(TECLA.PUXA)

    def escolha(self, lista):
        seed()
        [seed(time()) for i in range(choice([2, 3, 4]))]
        lista *= 5
        return lista[int(time() * 10000) % len(lista)]
        return choice(lista)


class GUI(_GUI, Thread):
    """ O terreno onde o Festival Kuarup é apresentado
    """

    def __init__(self, width=CANVASW, height=CANVASH):
        Thread.__init__(self)
        _GUI.__init__(self, width=width, height=height)

    def run(self):
        self.executante()

    def registra_executante(self, executante):
        self.executante = executante
        self.evento = Event()
        Thread.__init__(self)
        self.start()

    def espera(self):
        self.evento.wait()
        self.evento.clear()

    def continua(self):
        self.evento.set()

if __name__ == "__main__":
    _GUI().inicia(None)
