#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Kuarup - Festival de jogos na aprendizagem de Python
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2012/03/16  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2010, `GPL <http://is.gd/3Udt>__. 
"""
__author__ = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "1.0 $Revision$"[10:-1]
__date__ = "2012/03/16 $Date$"

from random import choice, seed
from threading import Event, Thread

from . import svgcanvas as gi
from .svgcanvas import *

seed()
IMAGEREPO = '/image/'


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


class _GUI(gi.GUI):
    def inicia(self, mundo):
        self.mundo_Kuarup = mundo

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

    def rect(self, x, y, w, h, **kwargs):
        gi.GUI.rect(self, x, y, w - x, h - y, **kwargs)

    def image(self, href, x, y, w, h, **kwargs):
        """ Returns an Image
        x,y - position; w,h - size
        """
        parent = kwargs.pop(PARENT, self)
        return Image(IMAGEREPO + href, x=x, y=y, width=w, height=h,
                     parent=parent, **kwargs)

    def escolha(self, lista):
        return choice(lista)


class GUI(_GUI, Thread):
    """ O terreno onde o Festival Kuarup é apresentado
    """

    def __init__(self, width=CANVASW, height=CANVASH):
        Thread.__init__(self)
        _GUI.__init__(self, width=width, height=height)
        self.executante = None
        self.evento = Event()

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
