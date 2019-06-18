#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Vittolino
# Copyright 2011-2017 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__, `GPL <http://is.gd/3Udt>`__.
#
# Vittolino é um software livre, você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF), na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA, sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>
"""

Notebook Com Anotações Markdown.
=============================================

.. module:: notebook
   :platform: Web
   :synopsis: Notebook Com Anotações Markdown.

.. moduleauthor:: Carlo Oliveira <carlo@ufrj.br>


Notebook Com Anotações Markdown.

.. seealso::

`Vitollino em Github <https://github.com/carlotolla/vitollino>`_

"""
from vitollino import Elemento, PSTYLE, EIMGSTY, INVENTARIO
from browser import html, win
import re
ps = [re.compile(x)for x in "^(#+)( .*)$©^!(\[.*\])\(.*\)"]


class Notebook(Elemento):
    """
    Um objeto de interação que é representado por uma trecho de código em uma cena.
            exemplo = Codigo(
             codigo="from anna import main", topo="Importando um módulo",
             vai=testa_codigo, style=dict(left=350, top=550, width=60))
    :param codigo: O código de programa
    :param vai: função executada quando se clica no objeto
    :param style: dicionário com dimensões do objeto {"left": ..., "top": ..., width: ..., height: ...}
    :param topo: Texto que aparece no topo do bloco
    :param cena: cena onde o objeto vai ser colocado
    """

    def __init__(self, codigo=[], cena=INVENTARIO, img="", vai=None, style=NS):
        class Mark:
            def __init__(self, code):
                self.code = code = self.process(code)
                self.div = html.DIV(code)
                self.keys = {"#": self.header, "!": self.image}
            def process(self, code):
                code = "".join(cd for cd in re.finditer(ps, code))
                return code
            def header(self, rg):
                return "<H{l}>{c}</H{l}>".format(l=len(rg.group(0)), c=rg.group(1))
                    
        class Code(Mark):
            def __init__(self, code):
                super().__init__(code)
                self.code = code = self.process(code)
                self.div = html.DIV(code)
            def process(self, code):
                return code
        self.img = img
        self.kind = {0:Mark, 1: Code}
        self.vai = vai if vai else lambda _=0: None
        self.cena = cena
        self.opacity = 0
        self.style = dict(**PSTYLE)
        # self.style["min-width"], self.style["min-height"] = w, h
        self.style.update(backgroundColor='rgba(210, 220, 220, 0.85)', **style)
        self.elt = html.DIV(style=self.style)
        self.xy = (-111, -111)
        istyle = dict(EIMGSTY)
        istyle.update(opacity=0.3)
        self.cell = [self.kind[kind](content) for kind, content in codigo]
        if img:
            self.img = html.IMG(src=img, style=istyle)
            self.elt <= self.img
        if topo:
            self.topo = html.DIV(color="black", style=dict(padding="15px"))
            self.topo.html = topo
            self.elt <= self.topo
        self.elt.onclick = self._click
        self.scorer = dict(ponto=1, valor=cena.nome, carta=img, casa=self.xy, move=None)
        self._code = html.CODE(codigo)
        self._area = html.PRE(self._code, Class="python", style=dict(
            position='relative', top=0, left=0, backgroundColor='transparent'))
        self.elt <= self._area
        self.code = codigo
        _ = self.entra(cena) if cena and (cena != INVENTARIO) else None

    @property
    def code(self):
        return self._area.value

    @code.setter
    def code(self, value):
        self._code.html = win.hljs.highlight("python", value).value

import unittest

class MyCase(unittest.TestCase):

    def testItIsSunny(self):
        x = Notebook([(0, "## ola")]).code
        self.assertEquals(x, "<H2> ola</H2>", x)

    def testItIsHot(self):
        x = Notebook([(0, "# ola")]).code
        self.assertEquals(x, "<H1> ola</H1>", x)

if __name__ == "__main__":
    unittest.main()