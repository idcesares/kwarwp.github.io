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

Gerador de labirintos e jogos tipo *'novel'*.
=============================================

.. module:: Vitollino
   :platform: Web
   :synopsis: Gerador de labirintos e jogos tipo *'novel'*.

.. moduleauthor:: Carlo Oliveira <carlo@ufrj.br>


Gerador de labirintos e jogos tipo *'novel'*.

.. seealso::

`Vitollino em Github <https://github.com/carlotolla/vitollino>`_

"""
import json
from browser import document, html, timer
from browser import window as win
from browser import ajax
import uuid

try:
    SUPERPYTHON = win.__SUPERPYTHON__
except Exception as _:
    SUPERPYTHON = None

CURSOR_STYLE = 'width: {}px, height: {}px, min-height: {}px, border-radius: 30px,' \
               ' left:{}px, top: {}px, position: absolute'
CURSOR_ELEMENT = 'left={}, top={}, width={}, height={}'
ABOXED = 9398
NOSCORE = dict(ponto=0, valor=0, carta=None, casa=None, move=None)
NOSC = {}
SZ = dict(W=300, H=300)
DOC_PYDIV = document["pydiv"]
ppcss = 'https://codepen.io/imprakash/pen/GgNMXO'
STYLE = {'position': "absolute", 'width': SZ['W'], 'left': 0, 'top': 0}
PSTYLE = {'position': "absolute", 'width': SZ['W'], 'left': 0, 'bottom': 0}
LIMBOSTYLE = {'position': "absolute", 'width': SZ['W'], 'left': 10000, 'bottom': 0, 'background': "white"}
ISTYLE = {'opacity': "inherited", 'height': 30, 'left': 0, 'top': 0, 'background': "white"}
ESTYLE = {'opacity': "inherited", 'width': 30, 'height': "30px", 'min-height': '30px', 'float': 'left',
          'position': 'unset'}
EIMGSTY = {"max-width": "100%", "max-height": "100%", "width": "100%", "height": "100%"}
STYLE["min-height"] = "300px"
IMAGEM = ""
NSTYLE = {'position': "absolute", 'width': "60%", 'left': "20%", 'top': 0, 'margin': "0%",
          "min-height": "20%", "cursor": "n-resize"}
SSTYLE = {'position': "absolute", 'width': "60%", 'left': "20%", 'bottom': 0, 'margin': "0%",
          "min-height": "10%", "cursor": "s-resize"}
LSTYLE = {'position': "absolute", 'width': "10%", 'left': "90%", 'top': "20%", 'margin': "0%",
          "min-height": "60%", "cursor": "e-resize"}
OSTYLE = {'position': "absolute", 'width': "10%", 'left': 0, 'top': "20%", 'margin': "0%",
          "min-height": "60%", "cursor": "w-resize"}
ZSTYLE = {'position': "absolute", 'width': "10%", 'margin': "0%",
          "min-height": "10%", "cursor": "zoom-in"}
PKEYS = ['False', 'None', 'True', ' and ', ' as ', 'assert', 'break', 'class ', 'continue', 'def ',
         'del', 'elif', 'else', 'except', 'finally', 'for ', 'from ', 'global ', 'if ', 'import ',
         ' in ', ' is ', 'lambda', 'nonlocal', ' not ', ' or ', 'pass', 'raise', 'return', 'try', 'while', 'with',
         'yield']


class _PATTERN:
    NOOP = {k.strip(): v for k, v in (tp.split(":") for tp in """""".replace("\n", "").split(";") if tp)}
    STARRY = {k.strip(): v for k, v in (tp.split(":") for tp in """background-color:black; opacity:0.4;
    background-image:
    radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
    radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
    radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px),
    radial-gradient(rgba(255,255,255,.4), rgba(255,255,255,.1) 2px, transparent 30px);
    background-size: 550px 550px, 350px 350px, 250px 250px, 150px 150px; 
    background-position: 0 0, 40px 60px, 130px 270px, 70px 100px;""".replace("\n", "").split(";") if tp)}

    NCROSS = {k.strip(): v for k, v in (tp.split(": ") for tp in """opacity: 0.7;
    background: 
    radial-gradient(circle, transparent 20%, slategray 20%, slategray 80%, transparent 80%, transparent),
    radial-gradient(circle, transparent 20%, slategray 20%, slategray 80%, transparent 80%, transparent) 30px 30px,
    linear-gradient(#A8B1BB 8px, transparent 8px) 0 -4px,
    linear-gradient(90deg, #A8B1BB 8px, transparent 8px) -4px 0;
    background-color: slategray;
    background-size: 60px 60px, 60px 60px, 30px 30px, 30px 30px;""".replace("\n", "").split(";") if tp)}

    OCROSS = {k.strip(): v for k, v in (tp.split(": ") for tp in """opacity: 0.7;
    background: 
    radial-gradient(circle, transparent 20%, slategray 20%, slategray 80%, transparent 80%, transparent),
    radial-gradient(circle, transparent 20%, slategray 20%, slategray 80%, transparent 80%, transparent) 50px 50px,
    linear-gradient(#A8B1BB 8px, transparent 8px) 0 -4px,
    linear-gradient(90deg, #A8B1BB 8px, transparent 8px) -4px 0;
    background-color: slategray;
    background-size: 100px 100px, 100px 100px, 50px 50px, 50px 50px;""".replace("\n", "").split(";") if tp)}

    BCROSS = {k.strip(): v for k, v in (tp.split(": ") for tp in """opacity: 0.7;
    background-color: slategray;
    background: 
    radial-gradient(slategray 9px, transparent 10px),        
    repeating-radial-gradient(slategray 0, slategray 4px, transparent 5px, transparent 15px,
    slategray 16px, slategray 20px, transparent 21px, transparent 30px);    
    background-size: 30px 30px, 90px 90px; 
    background-position: 0 0;""".replace("\n", "").split(";") if tp)}

    SHIPPO = {k.strip(): v for k, v in (tp.split(": ") for tp in """opacity: 0.5;background-color: #def;
    background-image: radial-gradient(closest-side, transparent 98%, rgba(0,0,0,.3) 99%),
    radial-gradient(closest-side, transparent 98%, rgba(0,0,0,.3) 99%);
    background-size: 80px 80px;
    background-position: 0 0, 40px 40px;""".replace("\n", "").split(";") if tp)}
    RADGRAD = ", ".join(["rgba({a},{a},{a},{b}) {c}%".format(
        a=200 if c % 2 else 20, b=0.6, c=c * 10) for c in range(0, 11)])

    BOKEH = {k.strip(): v for k, v in (tp.split(": ") for tp in """opacity: 0.5;
    background-size: 60px 60px, 60px 60px, 30px 30px, 30px 30px, 100% 100%;background: 
    radial-gradient({}) 0 0;""".replace("\n", "").format(RADGRAD).split(";") if tp)}


# INVENTARIO = None

from functools import WRAPPER_ASSIGNMENTS


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


def wraps_class_to_mimic_wrapped(original_cls):
    """
    Empacota uma classe decoradora para que apareça corretamente nos documentos.

    .. doctest ::

        >>> @wraps_class_to_mimic_wrapped
        ... class Exemplo:
        ...     ...
        ...
        >>> print(Exemplo.__doc__)
        Atualiza wrapper_cls para se assemelhar à classe original_cls.
        <BLANKLINE>

    :param original_cls: A Classe a ser empacotada
    :return: O empacotador da classe
    """

    def wrapper(wrapper_cls):
        """Atualiza wrapper_cls para se assemelhar à classe original_cls.
        """
        _ = [setattr(wrapper_cls, attr, getattr(original_cls, attr))
             for attr in WRAPPER_ASSIGNMENTS if hasattr(original_cls, attr)]
        return wrapper_cls

    return wrapper


def singleton(cls_to_decorate):
    """
    Decora um classe para ser um singleton e retornar sempre a mesma instância.

    >>> @singleton
    ... class Mono:
    ...     def __init__(self):
    ...             self.x = 0
    ...
    >>> Mono().x, Mono().x = 1, 2
    >>> print(Mono().x == Mono().x, Mono().x)
    True 2

    :param cls_to_decorate: A classe para ser definida como singleton
    :return: O decorador de singleton
    """
    instance = cls_to_decorate()

    @wraps_class_to_mimic_wrapped(cls_to_decorate)
    class Singletoner(cls_to_decorate):
        def __init__(self):
            super().__init__()
            self.wrapped = cls_to_decorate
            Singletoner.__doc__ = cls_to_decorate.__doc__
            Singletoner.__repr__ = cls_to_decorate.__repr__

        def __new__(cls, *args, **kwargs):
            return instance

        def __call__(self, *args, **kwargs):
            return instance

        def __repr__(self):
            return repr(cls_to_decorate)

    return Singletoner


@singleton
class NoEv:
    """ Representa um evento vazio.

    .. doctest::

        >>> print(ev.x, ev.y)
        -100 -100
    """
    x = -100
    y = -100

    def __repr__(self):
        return "<NoEvent>"

    def __init__(self):
        self.x = -100
        self.y = -100

    def stopPropagation(self):
        pass


@singleton
class SalaCenaNula:
    """
    Define uma Sala ou uma Cena vazia.

    .. doctest::

        >>> cena = Cena(SalaCenaNula())  # A próxima cena
        >>> uma_cena = Cena(SalaCenaNula(), cena)  # Cena nula à esquerda, proxima no meio
        >>> uma_cena.vai_esquerda()  # tenta navegar para a cena à esquerda
        >>> # não vai, pois a cena é nula e não deixa que se navegue para ela
        >>> print(INVENTARIO.cena == cena)
        True

    Deve ser usado quando um parâmetro requer uma cena mas não deve ter uma cena válida ali.
    """

    def __init__(self):
        self.esquerda, self.direita = [None] * 2
        self.salas = [None] * 5
        self.cenas = [self] * 4
        self.img = "_NO_IMG_"
        self.nome = "_NO_NAME_"
        self.init = self.init
        self.centro, self.norte, self.leste, self.sul, self.oeste = self.salas

    def __repr__(self):
        return "<CenaNula>"

    def init(self):
        self.init = lambda _=0, s=self: self
        self.esquerda, self.direita = [SalaCenaNula()] * 2
        self.salas = [SalaCenaNula()] * 5
        self.cenas = [SalaCenaNula()] * 4
        self.centro, self.norte, self.leste, self.sul, self.oeste = self.salas
        return self

    def vai(self):
        pass

    def portal(self, *_, **__):
        pass


NADA = SalaCenaNula().init()
NS = {}
NL = []


class Musica(object):
    def __init__(self, sound, loop=True, autoplay=True, sound_type="audio/mpeg"):
        self.sound = html.AUDIO(src=sound, autoplay=autoplay, loop=loop, type=sound_type)
        document.body <= self.sound


class Inventario:
    """
    Os objetos que estão de posse do jogador.


    :param tela: Div do HTML onde o inventário será anexado
    """
    """# Usado para definir um jogador no modo multiusuário"""
    GID = str(uuid.uuid4())[:8]  # Usado para definir um jogador no modo multiusuário

    def __init__(self, tela=DOC_PYDIV):
        self.tela = tela
        self.cena = None
        self.nome = "__INVENTARIO__"
        self.inventario = {}
        self.opacity = 0
        self.style = dict(**ISTYLE)
        self.style["min-height"] = "30px"
        self.elt = html.DIV(Id="__inv__", style=self.style)
        self.elt.onclick = self.mostra
        self.limbo = html.DIV(style=self.style)
        self.limbo.style.left = "4000px"
        self.mostra()
        tela <= self.elt

    def __repr__(self):
        return "Inventario"

    def __le__(self, other):
        if hasattr(other, 'elt'):
            self.elt <= other.elt
        else:
            self.elt <= other

    def inicia(self):
        self.elt.html = ""
        self.inventario = {}
        self.cena = None
        self.opacity = 0
        self.mostra()

    def desmonta(self, _=0):
        self.limbo <= self.elt

    def monta(self, _=0):
        self.tela <= self.elt

    def mostra(self, _=0):
        self.opacity = abs(self.opacity - 0.5)
        self.elt.style.opacity = self.opacity

    def bota(self, nome_item, item="", acao=None):
        """
        Os objetos que estão de posse do jogador.

        .. doctest::

            >>> inv.bota("uma_coisa")
            >>> "uma_coisa" in inv.inventario
            True

        :param nome_item: uma string com o nome do item, ele será criado e colocado no inventário
        :param item: URL da imagem do item nomeado por nome_item
        :param acao: ação associada com o item nomeado quando ele é clicado
        """
        if isinstance(nome_item, str):
            item_img = html.IMG(Id=nome_item, src=item, width=30, style=EIMGSTY)
            self.elt <= item_img
        else:
            nome_item.entra(self)
            item_img = nome_item.elt
            item_img.style = ESTYLE
        Dropper(item_img)
        if acao:
            item_img.onclick = lambda *_: acao()
        else:
            acao = lambda *_: None
        self.inventario[nome_item] = acao

    def tira(self, nome_item):
        item_img = document[nome_item]
        self.limbo <= item_img
        return self.inventario.pop(nome_item, None)

    def score(self, casa, carta, move, ponto, valor, _level=1):
        data = dict(doc_id=INVENTARIO.GID, carta=carta, casa=casa, move=move, ponto=ponto, valor=valor,
                    _level=_level, tempo=win.Date.now())
        SUPERPYTHON.scorer(data) if SUPERPYTHON else None
        # print('store', data)

    @staticmethod
    def send(operation, data, action=lambda t: None, method="POST"):
        def on_complete(request):
            if int(request.status) == 200 or request.status == 0:
                # print("req = ajax()== 200", request.text)
                action(request.text)
            else:
                print("error " + request.text)

        req = ajax()
        req.bind('complete', on_complete)
        # req.on_complete = on_complete
        url = "/record/" + operation
        req.open(method, url, True)
        # req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.set_header("Content-Type", "application/json; charset=utf-8")
        print("def send", data)
        data = json.dumps(data)
        req.send(data)


INVENTARIO = Inventario()


class Elemento:
    """
    Um objeto de interação que é representado por uma imagem em uma cena.

            papel = Elemento(
             img="papel.png", tit="caderno de notas",
             vai=pega_papel, style=dict(left=350, top=550, width=60))


    :param img: URL de uma imagem
    :param vai: função executada quando se clica no objeto
    :param style: dicionário com dimensões do objeto {"left": ..., "top": ..., width: ..., height: ...}
    :param tit: Texto que aparece quando se passa o mouse sobre o objeto
    :param alt: Texto para leitores de tela
    :param cena: cena alternativa onde o objeto vai ser colocado
    :param score: determina o score para este elemento
    :param kwargs: lista de parametros nome=URL que geram elementos com este nome e a dada imagem
    """
    limbo = html.DIV(style=LSTYLE)

    def __init__(self, img="", vai=None, style=NS, tit="", alt="", cena=INVENTARIO, score=NOSC, drag=False, drop='',
                 **kwargs):
        self._auto_score = self.score if score else self._auto_score
        self.img = img
        self.vai = vai if vai else lambda _=0: None
        self.cena = cena
        self.opacity = 0
        self.style = dict(**PSTYLE)
        # self.style["min-width"], self.style["min-height"] = w, h
        self.style.update(**style)
        self.elt = html.DIV(Id=tit, style=self.style)
        self.xy = (-111, -111)
        #  TODO FIX self.scorer = dict(ponto=1, valor=cena.nome, carta=tit or img, casa=self.xy, move=None)
        score = {}
        #  TODO FIX self.scorer.update(score)
        if img:
            self.img = html.IMG(src=img, title=tit, alt=alt, style=EIMGSTY)  # width=self.style["width"])
            self.elt <= self.img
        self.elt.onclick = self._click
        self.c(**kwargs)
        # _ = Dragger(self.elt) if drag else None
        # _ = Droppable(self.elt, drop, self.vai) if drop else None
        _ = self.entra(cena) if cena and (cena != INVENTARIO) else None

    def _auto_score(self, **kwargs):
        pass

    def __le__(self, other):
        if hasattr(other, 'elt'):
            self.elt <= other.elt
        else:
            self.elt <= other

    def _click(self, ev=NoEv()):
        self.xy = (ev.x, ev.y)
        ev.stopPropagation()
        return self.vai(ev)

    def entra(self, cena, style=NOSC):
        styler = dict(self.style)
        styler.update(style)
        self.elt.style = styler
        self.cena = cena
        self.scorer.update(valor=cena.nome, move=self.xy,
                           casa=(styler["left"], styler["top"] if "top" in styler else 0))
        self._auto_score(**self.scorer)
        cena <= self

    def score(self, **kwargs):
        #  TODO FIX score = {key: kwargs[key] if key in kwargs else value for key, value in self.scorer.items()}
        score = {}
        INVENTARIO.score(**score)

    @classmethod
    def c(cls, **kwargs):
        return [setattr(cls, nome, Elemento(**img) if isinstance(img, dict) else Elemento(img=img))
                for nome, img in kwargs.items()]


class Codigo(Elemento):
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

    def __init__(self, codigo="", topo="", cena=INVENTARIO, img="", vai=None, style=NS):
        self.img = img
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
        # TODO FIX  codigo = win.hljs.highlight("python", codigo)

        def rp(cod, keys=PKEYS[:], mark='<span class="hljs-keyword">{}</span>'):
            key = keys.pop()
            cod = cod.replace(key, mark.format(key))
            return rp(cod, keys, mark) if keys else cod

        # codigo = rp(codigo)
        # TODO FIX self._code.html = codigo.value
        _ = self.entra(cena) if cena and (cena != INVENTARIO) else None


class Portal:
    N = NSTYLE
    L = LSTYLE
    S = SSTYLE
    O = OSTYLE
    Z = ZSTYLE
    PORTAIS = dict(N=NSTYLE, L=LSTYLE, S=SSTYLE, O=OSTYLE, Z=ZSTYLE)

    def __init__(self, cena=None, debug_=False, **kwargs):
        self.portal, self.kwargs, self.debug = None, kwargs, debug_
        self.style = ZSTYLE
        if cena:
            self.cena = cena
            self.p(**kwargs)

    def __call__(self, cena):
        class CenaDecorada(cena):
            def __init__(self, *args, __portal=self, **kargs):
                style = ZSTYLE
                super(CenaDecorada, self).__init__(*args, **kargs)
                __portal.cena = self
                [__portal.__setup__(acena, portal, style) for portal, acena in __portal.kwargs.items()]

        return CenaDecorada

    def __setup__(self, cena, portal, style=NS):
        class Portico:
            def __init__(self, origem, destino, portal_, style_, debug=False):
                self.origem, self.destino, self.portal_, self.style_ = origem, destino, portal_, style_
                self.elt = html.DIV(style=self.style_)
                self.elt.onclick = self._onclick
                Droppable(self.elt, cursor="not-allowed")
                if isinstance(self.origem, Cena):
                    self.origem.elt <= self.elt
                    if debug:
                        Cursor(self.elt, self.origem.elt)
                    setattr(self.origem, portal, self)
                self._vai = self.do_vai

            def _onclick(self, *args):
                return self._vai(*args)

            def __call__(self, *args, **kwargs):
                return self._vai(*args, **kwargs)

            def fecha(self, *_):
                self._vai = lambda *_: None

            def abre(self, *_):
                self._vai = self.do_vai

            def do_vai(self, ev=NoEv()):
                print("vai", self.destino.nome)
                return self.destino.vai(ev)

            @property
            def vai(self):
                return self._vai

            @vai.setter
            def vai(self, value):
                self._vai = value

            @property
            def img(self):
                return self.destino.img

            """
            @property
            def x(self, value):
                self.elt.left = value

            @property
            def y(self, value):
                self.elt.top = value

            @property
            def w(self, value):
                self.elt.width = value

            @property
            def h(self, value):
                self.elt.height = value
            """

            def __eq__(self, other):
                return other == self.destino

        _ = style.update(**{"min-height": "%dpx" % style["height"]}) if "height" in style else None
        sty = Portal.PORTAIS.get(portal, ZSTYLE)
        self.style.update(sty)
        self.style.update(style)
        ptc = Portico(self.cena, cena, portal, self.style, debug=self.debug)
        self.elt = ptc.elt
        return ptc

    def p(self, **kwargs):
        style = dict(NS)
        styl = kwargs.pop("style") if "style" in kwargs else {}
        style.update(**styl)
        self.portal = [self.__setup__(cena, portal, style=style) for portal, cena in kwargs.items()
                       if (portal in "NSLO" and cena != NADA)]
        self.portal = self.portal[0] if self.portal else SalaCenaNula()
        return self.cena

    def vai(self, *_):
        self.portal.vai()


ROSA = list("NLSO")
CART = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # [(i, j) for j, i in CART]


class Labirinto:
    def __init__(self, c=NADA, n=NADA, l=NADA, s=NADA, o=NADA):
        self.salas = [sala for sala in [c, n, l, s, o]]
        self.centro, self.norte, self.leste, self.sul, self.oeste = self.salas
        self.lb()

    def lb(self):
        for indice, sala in enumerate(self.salas[1:]):
            self.centro.cenas[indice].portal(N=sala.cenas[indice]) if sala else None
            indice_oposto = (indice + 2) % 4
            sala.cenas[indice_oposto].portal(N=self.centro.cenas[indice_oposto]) if sala else None

    @staticmethod
    def m(cenas):
        def valid(cns, jj, ii, m, n):
            return 0 <= jj + m < len(cns) and 0 <= ii + n < len(cns[jj + m]) and cns[jj + m][ii + n]

        def vizinhos(jj, ii, cns=cenas):
            return [(kk, cns[jj + m][ii + n]) for kk, (m, n) in enumerate(CART) if valid(cns, jj, ii, m, n)]

        for j, linha in enumerate(cenas):
            if isinstance(linha, list):
                for i, centro in enumerate(linha):
                    if not isinstance(centro, Sala):
                        continue
                    for k, sala in vizinhos(j, i):
                        if not isinstance(sala, Sala):
                            continue
                        centro.cenas[k].meio = sala.cenas[k]
                        indice_oposto = (k + 2) % 4
                        sala.cenas[indice_oposto].meio = centro.cenas[indice_oposto]

    @staticmethod
    def n(cenas):
        def valid(cns, jj, ii, m, n):
            return 0 <= jj + m < len(cns) and 0 <= ii + n < len(cns[jj + m]) and cns[jj + m][ii + n]

        def vizinhos(jj, ii, cns=cenas):
            return [(kk, cns[jj + m][ii + n]) for kk, (m, n) in enumerate(CART) if valid(cns, jj, ii, m, n)]
            # return [(kk, cns[jj + m][ii + n]) for kk, (m, n) in enumerate(CART)
            #  if 0 <= jj + m < len(cns) and 0 <= ii + n < len(cns[jj+m])and cns[jj + m][ii + n]]

        for j, linha in enumerate(cenas):
            if isinstance(linha, list):
                for i, centro in enumerate(linha):
                    if not isinstance(centro, Sala):
                        continue
                    for k, sala in vizinhos(j, i):
                        if not isinstance(sala, Sala):
                            continue
                        centro.cenas[k].portal(**{"N": sala.cenas[k]})
                        indice_oposto = (k + 2) % 4
                        sala.cenas[indice_oposto].portal(**{"N": centro.cenas[indice_oposto]})


class Sala:
    def __init__(self, n=NADA, l=NADA, s=NADA, o=NADA, nome='', **kwargs):
        self.cenas = [Cena(img) if isinstance(img, str) else img for img in [n, l, s, o]]
        self.nome = nome
        Sala.c(**kwargs)
        self.p()

    @property
    def norte(self):
        return self.cenas[0]

    @property
    def leste(self):
        return self.cenas[1]

    @property
    def sul(self):
        return self.cenas[2]

    @property
    def oeste(self):
        return self.cenas[3]

    def p(self):
        for esquerda in range(4):
            cena_a_direita = (esquerda + 1) % 4
            self.cenas[esquerda].direita = self.cenas[cena_a_direita]
            self.cenas[cena_a_direita].esquerda = self.cenas[esquerda]

    @staticmethod
    def c(**cenas):
        for nome, cena in cenas.items():
            setattr(Sala, nome, Sala(nome=nome, **cena))


class Salao(Sala):
    def p(self):
        # [cena.sai(saida) for cena, saida in zip(self.cenas, saidasnlso)]
        for esquerda in range(4):
            cena_a_direita = (esquerda + 1) % 4
            self.cenas[esquerda].portal(L=self.cenas[cena_a_direita])
            self.cenas[cena_a_direita].portal(O=self.cenas[esquerda])

    @staticmethod
    def c(**cenas):
        for nome, cena in cenas.items():
            setattr(Salao, nome, Salao(nome=nome, **cena))


class Cena:
    """
    Use para construir uma cena.
    ::

        from _spy.vitollino import Cena

        cena_esq = Cena(img="esq.jpg")
        cena_mei = Cena(img="mei.jpg", cena_esq)
        cena_mei.vai()

    :param str img: URL da imagem
    :param Cena esquerda: Cena que está à esquerda desta
    :param Cena direita: Cena que está à direita desta
    :param Cena meio: Cena que está à frente desta
    :param vai: Função a ser chamada no lugar da self.vai nativa
    """

    def __init__(self, img=IMAGEM, esquerda=NADA, direita=NADA, meio=NADA,
                 vai=None, nome='', xy=(0, 0), score=NOSC, **kwargs):
        width = STYLE["width"]
        self.scorer = dict(ponto=1, valor="__JOGO__", carta=nome, casa=xy, move=None)
        self.scorer.update(score)
        self._auto_score = self.score if score else self._auto_score
        self.ev = NoEv()
        self.xy = xy
        self.img = img
        self.nome = nome
        self.dentro = []
        self.esquerda, self.direita, self.meio = esquerda or NADA, direita or NADA, meio or NADA
        self.N, self.O, self.L = [NADA] * 3
        self.vai = vai or self.vai
        self.elt = html.DIV(style=STYLE)
        self.img = html.IMG(src=self.img, width=width, style=STYLE, title=nome)
        self.elt <= self.img
        Cena.c(**kwargs)

        self._cria_divs(width)

    def _cria_divs(self, width):
        self.divesq = divesq = html.DIV(style=STYLE)
        divesq.style.opacity = 0
        divesq.style.width = width // 3  # 100
        Droppable(divesq, cursor="not-allowed")
        divesq.onclick = self.vai_esquerda
        self.divmeio = divmeio = html.DIV(style=STYLE)
        divmeio.style.opacity = 0
        divmeio.style.width = width // 3  # 100
        divmeio.onclick = self.vai_meio
        Droppable(divmeio, cursor="not-allowed")
        divmeio.style.left = width // 3  # 100
        self.divdir = divdir = html.DIV(style=STYLE)
        divdir.style.opacity = 0
        divdir.style.width = width // 3  # 100
        divdir.onclick = self.vai_direita
        Droppable(divdir, cursor="not-allowed")
        divdir.style.left = width * 2 // 3  # 100
        self.elt <= self.divesq
        self.elt <= self.divmeio
        self.elt <= self.divdir

    def __call__(self):
        return self.vai()

    def __le__(self, other):
        if hasattr(other, 'elt'):
            self.elt <= other.elt
        else:
            self.elt <= other
            print(other)

    def portal(self, esquerda=None, direita=None, meio=None, **kwargs):
        self.esquerda, self.direita, self.meio = esquerda or self.esquerda, direita or self.direita, meio or self.meio
        return Portal(self, **kwargs)

    @staticmethod
    def c(**cenas):
        for nome, imagem in cenas.items():
            imagem, kwargs = (imagem, {}) if isinstance(imagem, str) \
                else (imagem["img"], (imagem.pop("img") and 0) or imagem)
            setattr(Cena, nome, Cena(imagem, nome=nome, **kwargs))

    @staticmethod
    def q(n=NADA, l=NADA, s=NADA, o=NADA, nome="", **kwargs):
        return Sala(n, l, s, o, nome=nome, **kwargs)

    @staticmethod
    def s(n=NADA, l=NADA, s=NADA, o=NADA, nome="", **kwargs):
        return Salao(n, l, s, o, nome=nome, **kwargs)

    def vai_direita(self, _=0):
        if self.direita:
            self.direita.vai()

    def vai_esquerda(self, _=0):
        if self.esquerda:
            self.esquerda.vai()

    def vai_meio(self, _=0):
        if self.meio:
            self.meio.vai()

    def sai(self, saida):
        self.meio = saida

    def bota(self, nome_item):
        if isinstance(nome_item, str):
            item_img = html.IMG(Id=nome_item, src=nome_item, width=30, style=EIMGSTY)
            self.elt <= item_img
        else:
            nome_item.entra(self)
        self.dentro.append(nome_item)
        # self <= item

    def tira(self, item):
        self.dentro.pop(item)

    def vai(self, ev=NoEv()):
        self.ev = ev
        INVENTARIO.cena = self
        INVENTARIO.desmonta()
        tela = DOC_PYDIV
        tela.html = ""
        tela <= self.elt
        INVENTARIO.monta()
        INVENTARIO.cena = self
        self._auto_score(move=(ev.x, ev.y))
        return self

    def _auto_score(self, **kwargs):
        pass

    def score(self, **kwargs):
        score = {key: kwargs[key] if key in kwargs else value for key, value in self.scorer.items()}
        INVENTARIO.score(**score)


class Popup:
    POP = None

    def __init__(self, cena, tit="", txt="", vai=None, **kwargs):
        self.cena, self.tit, self.txt, = cena, tit, txt
        self.kwargs = kwargs
        self._vai = vai
        self.optar = {}
        Popup.__setup__()
        if isinstance(cena, Cena):
            self.d(cena, tit, txt)

    def vai(self):
        return self._vai() if self._vai else None

    def __call__(self, cena=None, tit="", txt="", *args, **kwargs):
        cena = cena or self.cena
        out = cena(*args, **kwargs)
        self.d(out, tit or self.tit, txt or self.txt)

        return out  # CenaPopup

    @staticmethod
    def __setup__():
        class Pop:
            def __init__(self, tela=DOC_PYDIV):
                self.tela = tela
                self.optou = ""
                self.popup = html.DIV(Id="__popup__", Class="overlay")
                self.div = div = html.DIV(Class="popup")
                self.tit = html.H2()
                a = html.A("&times;", Class="close", href="#")
                self.go = html.A(Id="txt_button", Class="button", href="#__popup__")
                self.go.onclick = self._open
                a.onclick = self._close
                self.alt = html.DIV(Class="content")
                self.popup <= div
                self.popup.style = {"visibility": "hidden", "opacity": 0}
                div <= self.tit
                div <= a
                div <= self.alt

            def __repr__(self):
                return "<Popup>"

            def _close(self, *_):
                self.popup.style = {"visibility": "hidden", "opacity": 0}
                self.esconde()

            def _open(self, *_):
                self.popup.style = {"visibility": "visible", "opacity": 0.7}

            def esconde(self, *_):
                ...

            def monta_optar(self, **kwargs):
                def opcao(letra):
                    self.optou = letra

                def opta(letra, texto):
                    div = html.DIV(Class="content")
                    optou = html.A(chr(ABOXED + ord(letra) - ord("A")), Class="option", href="#")
                    optou.onclick = lambda *_: opcao(letra) or self._close()
                    texto_opcao = html.SPAN(texto)
                    div <= optou
                    div <= texto_opcao
                    return div

                optar = [[optou, texto] for optou, texto in kwargs.items() if optou in "ABCDEFGHIJK"]
                for op in optar:
                    self.div <= opta(*op)

            def mostra(self, act, tit="", txt="", **kwargs):
                if tit or txt:
                    self.tit.text, self.alt.text = tit, txt
                self.monta_optar(**kwargs)
                # self.popup.style = {"visibility": "visible", "opacity": 0.7}
                self._open()
                act()

        Popup.POP = Pop()
        Popup.__setup__ = lambda: None

    @staticmethod
    def d(cena, tit="", txt=""):
        cena.elt <= Popup.POP.popup
        cena.elt <= Popup.POP.go
        act = cena.vai
        cena.vai = lambda *_, **__: Popup.POP.mostra(act, tit, txt)
        return cena


class Texto(Popup):
    def __init__(self, cena=NADA, tit="", txt="", foi=None, **kwargs):
        super().__init__(None, tit=tit, txt=txt, vai=None, **kwargs)
        # self.elt = Popup.POP.popup
        self.cena = cena
        self.esconde = foi if foi else self.esconde
        # cena <= self

    def esconde(self, ev=NoEv()):
        ...

    def mostra(self, tit="", txt="", **kwargs):
        self.elt = Popup.POP.popup
        self.cena.elt <= self.elt
        Popup.POP.mostra(lambda *_: None, tit=tit, txt=txt, **kwargs)

        Popup.POP.esconde = self.esconde
        pass

    def vai(self, ev=NoEv()):
        # self.elt = Popup.POP.popup
        ev.stopPropagation()
        self.cena.elt <= Popup.POP.popup
        Popup.POP.mostra(lambda *_: None, self.tit, self.txt)
        Popup.POP.esconde = self.esconde
        return False

    @staticmethod
    def texto(tit="", txt="", **kwars):
        def _texto(class_):
            def decorate(*args, **kwargs):
                def decorate_vai(*_):
                    class_instance.texto.vai()

                class_instance = class_(*args, **kwargs)
                decorated_vai, class_instance.portal.vai = class_instance.portal.vai, decorate_vai
                class_instance.texto = Texto(class_instance.cena, tit=tit, txt=txt, **kwars)
                class_instance.texto.esconde = lambda *_: decorated_vai()
                return class_instance

            return decorate

        return _texto


class Point(list):
    def __init__(self, x, y):
        super().__init__([x, y])
        self.x, self.y = x, y
        self.__iadd__, self.__isub__ = self.__radd__, self.__rsub__

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        print("__radd__(self, {other})".format(other=other))
        self.x += other.x
        self.y += other.y
        return self

    def __rsub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def px(self):
        return ["{}px".format(ordin) for ordin in (self.x, self.y)]

    def __iter__(self):
        return (ordin for ordin in (self.x, self.y))

    def __setitem__(self, key, value):
        if key:
            self.y = value
        else:
            self.x = value


class Cursor:
    def __init__(self, alvo, cena=DOC_PYDIV):
        self.alvo, self.cena, self.ponto = alvo, cena, None
        outer = self

        class Noop:
            def __init__(self, outerer=self):
                self.outer = outerer

            def change(self, ev):
                pass

            @staticmethod
            def update_style(styler, new_style, delta=None):
                cur_style = dict(outer.style)
                point = Point(outer.alvo.style.left, outer.alvo.style.top)
                delta = delta if delta else Point(outer.alvo.style.width, outer.alvo.style.minHeight)
                print("delta.x, delta.y", outer.elt.style.left, outer.elt.style.top, delta.x, delta.y)
                cur_style.update(cursor=styler, left=point.x, top=point.y, width=delta.x, height=delta.y, **new_style)
                cur_style["min-height"] = "{}px".format(delta.y)
                return cur_style

            def next(self, ev):
                ev.target.style = self.update_style("move", _PATTERN.BCROSS)
                outer.current = outer.move

            def mouse_over(self, ev):
                ev.target.style.cursor = "default"

            def mouse_down(self, ev):
                outer.ponto = Point(ev.x, ev.y)
                outer.cursor = outer.current
                pass

            def mouse_move(self, ev):
                pass

            def mouse_up(self, _):
                outer.cursor = outer.noop
                st = self.outer.elt.style
                width_, height_, left_, top_ = st.width, st.minHeight, st.left, st.top
                self.outer.elt.title = CURSOR_ELEMENT.format(left_, top_, width_, height_)

        class Move(Noop):
            def mouse_move(self, ev):
                delta = Point(int(alvo.style.left.rstrip("px")), int(alvo.style.top.rstrip("px"))) \
                        + Point(ev.x, ev.y) - outer.ponto
                alvo.style.left, alvo.style.top = delta
                outer.elt.left, outer.elt.top = delta
                outer.ponto = Point(ev.x, ev.y)

            def mouse_over(self, ev):
                ev.target.style.cursor = "move"

            def next(self, ev):
                print("next resize")
                ev.target.style = self.update_style("grab", _PATTERN.BOKEH)
                outer.current = outer.resize

        class Resize(Noop):
            def mouse_move(self, ev):
                delta = Point(int(outer.elt.style.width.rstrip("px")), int(outer.elt.style.minHeight.rstrip("px"))) \
                        + Point(ev.x, ev.y) - outer.ponto
                outer.elt.style.width, outer.elt.style.minHeight = delta.px()
                alvo.style.width, alvo.style.minHeight = delta.px()
                outer.elt.style.height = alvo.style.height = delta.px()[1]
                # alvo.style = self.update_style("default", {}, delta)
                # outer.elt.style = self.update_style("default", PATTERN.BOKEH, delta)
                # print("mouse_move", alvo.style.minHeight, delta)
                outer.ponto = Point(ev.x, ev.y)

            def mouse_over(self, ev):
                ev.target.style.cursor = "grab"

            def next(self, ev):
                print("next noop")
                ev.target.style = self.update_style("default", _PATTERN.STARRY)
                outer.current = outer.noop

        def next_state(ev):
            # self.state.append(self.state.pop(0))
            self.current.next(ev)

        def _mouse_down(ev): return self.cursor.mouse_down(ev)

        def _mouse_up(ev): return self.cursor.mouse_up(ev)

        def _mouse_move(ev): return self.cursor.mouse_move(ev)

        def _mouse_over(ev): return self.cursor.mouse_over(ev)

        def _strip_kind(dm):
            kinds = "px %".split()
            kind = [k for k in kinds if isinstance(dm, str) and (k in dm)]
            # dm = str(dm) if isinstance(dm, int) else dm if isinstance(dm, str) else "0"
            return int(dm.rstrip(kind[0])) if kind else int(dm) if dm else 0

        self.noop, self.move, self.resize = self.state = [Noop(), Move(), Resize()]
        self.cursor = self.noop
        self.current = self.move
        style = dict(**ISTYLE)
        dims = [self.alvo.style.top, self.alvo.style.minHeight, self.alvo.style.left, self.alvo.style.width]
        print("dim left, top = ", dims)
        dims = [_strip_kind(dm) for dm in dims]
        top, height, left, width = dims
        # left, top = left + width//2 - 30, top + height//2 - 30
        cstyle = CURSOR_STYLE
        cstyle = cstyle.format(width, height, height, left, top)
        print("cstyle = ", cstyle)
        cstyle = {k.strip(): v for k, v in (tp.split(":") for tp in cstyle.replace("\n", "").split(", ") if tp)}
        style.update(**cstyle)
        style.update(**_PATTERN.STARRY)
        self.style = style
        self.elt = html.DIV(Id="__cursor__", style=style, title="")
        self.cena <= self.elt
        self.elt.onclick = next_state
        self.elt.onmousedown = _mouse_down
        self.elt.onmouseup = _mouse_up
        self.elt.onmousemove = _mouse_move
        self.elt.onmouseover = _mouse_over


class Dragger:
    POINTER = ""
    ACTION = ""

    def __init__(self, dragger):
        self._mouse_over = self.pre_mouse_over
        self._mouse_down = self.pre_mouse_down
        self._mouse_up = self.pre_mouse_up
        self._mouse_move = self.pre_mouse_move

        def drag_start(ev): self.drag_start(ev)

        def mouse_over(ev): self._mouse_over(ev)

        def mouse_down(ev): self._mouse_down(ev)

        def mouse_move(ev): self._mouse_move(ev)

        def mouse_up(ev): self._mouse_up(ev)

        self.dragger = dragger
        dragger.draggable = True

        dragger.ondragstart = drag_start
        dragger.onmouseover = mouse_over
        dragger.onmousedown = mouse_down
        dragger.onmousemove = mouse_move
        dragger.onmouseup = mouse_up

    def widen(self, dx):
        self.dragger.w = self.dragger.w + dx

    def highten(self, dy):
        self.dragger.h = self.dragger.h + dy

    @staticmethod
    def pre_mouse_over(ev):
        ev.target.style.cursor = "grab"

    @staticmethod
    def mouse_over(ev):
        obj = ev.target
        dx, dy, x, y = obj.w, obj.h, ev.x - obj.offsetLeft, ev.y - obj.offsetTop
        quadrante = dy // y * 3 + dx // x
        ev.target.style.cursor = Dragger.POINTER[quadrante]

    def drag_start(self, ev):
        ev.data['text'] = ev.target.id
        ev.data.effectAllowed = 'move'
        ev.preventDefault()
        return False

    def mouse_down(self, ev):
        ev.target.style.cursor = "move"
        self._mouse_move = self.pre_mouse_move

    def pre_mouse_down(self, ev):
        ev.target.style.cursor = "move"
        self._mouse_move = self.pre_mouse_move

        pass

    def pre_mouse_up(self, _):
        self._mouse_over = self.mouse_over
        self._mouse_move = self.no_mouse_move
        self._mouse_down = self.mouse_down
        pass

    def _mouse_up_(self, _):
        self._mouse_over = self.mouse_over
        self._mouse_down = self.mouse_down
        self._mouse_up = self.mouse_up

    def mouse_up(self, _):
        self._mouse_over = self.pre_mouse_over
        self._mouse_down = self.pre_mouse_down
        self._mouse_up = self.pre_mouse_up
        pass

    def no_mouse_move(self, ev):
        pass

    def pre_mouse_move(self, ev):
        obj = ev.target
        dx, dy, x, y = obj.w, obj.h, ev.x - obj.offsetLeft, ev.y - obj.offsetTop
        self.dragger.x = ev.x - x
        self.dragger.y = ev.y - y
        pass


class Dropper:
    def __init__(self, dropper):
        dropper.draggable = True
        dropper.ondragstart = self.drag_start
        dropper.onmouseover = self.mouse_over

    def mouse_over(self, ev):
        ev.target.style.cursor = "pointer"

    def drag_start(self, ev):
        ev.data['text'] = ev.target.id
        ev.data.effectAllowed = 'move'
        ev.preventDefault()
        return False


class Droppable:
    def __init__(self, droppable, dropper_name="", action=None, cursor=None):
        # droppable.ondragover = self.drag_over
        # droppable.ondrop = self.drop
        droppable.bind("dragover", self.drag_over)
        droppable.bind("drop", self.drop)
        self.dropper_name = dropper_name
        self.cursor = cursor
        self.action = action if action else lambda *arg: None

    def drag_over(self, ev):
        ev.data.dropEffect = 'move'
        # print('drop', ev.target.id)
        src_id = ev.data['text']
        elt = document[src_id]
        elt.style.cursor = self.cursor or "auto"
        ev.preventDefault()
        return False

    def drop(self, ev):
        ev.preventDefault()
        src_id = ev.data['text']
        elt = document[src_id]
        elt.style.cursor = "auto"
        if self.dropper_name == src_id:
            self.action(elt, self)
        return False


class Folha:
    def __init__(self, texto, ht_ml, tela, left):
        style = {'position': "absolute", 'width': 80, 'height': 80, 'left': left, 'top': 10, 'background': "yellow"}
        fid = "folha%d" % left
        self.folha = ht_ml.DIV(texto, Id=fid, style=style, draggable=True)
        tela <= self.folha
        self.folha.ondragstart = self.drag_start
        self.folha.onmouseover = self.mouse_over

    def mouse_over(self, ev):
        ev.target.style.cursor = "pointer"

    def drag_start(self, ev):
        ev.data['text'] = ev.target.id
        ev.data.effectAllowed = 'move'


class Suporte:
    def __init__(self, bloco, ht_ml, tela, left, certa):
        style = {'position': "absolute", 'width': 80, 'height': 80, 'left': left, 'top': 100, 'background': "grey"}
        self.folha = ht_ml.DIV("............ ............", style=style)
        self.left = left
        self.certa = certa
        tela <= self.folha
        self.folha.ondragover = self.drag_over
        self.folha.ondrop = self.drop
        self.bloco = bloco

    def drag_over(self, ev):
        ev.data.dropEffect = 'move'
        ev.preventDefault()

    def drop(self, ev):
        ev.preventDefault()
        src_id = ev.data['text']
        elt = document[src_id]
        elt.style.left = self.left
        elt.style.top = 100
        elt.draggable = False  # don't drag any more
        elt.style.cursor = "auto"
        certa = True
        if src_id != self.certa:
            elt.style.background = "red"
            certa = False
            self.bloco.conta_peça(certa)


class Bloco:
    def __init__(self):
        self.monta = lambda *_: None
        ordem = "10 410 310 210 110".split()
        texto = "" \
                "Era uma vez|" \
                "de nós três|" \
                "por cima|" \
                "deu um salto|" \
                "um gato pedrêz|" \
                "".split("|")
        tela = document["pydiv"]
        tela.html = ""
        self.pecas_colocadas = []
        print(list(enumerate(ordem)))
        for pos, fl in enumerate(ordem):
            Suporte(self, html, tela, pos * 100 + 10, "folha" + fl)
        for pos, tx in enumerate(texto):
            Folha(tx, html, tela, pos * 100 + 10)

    def inicia_de_novo(self):
        pass

    def conta_pecas(self, valor_peca):
        self.pecas_colocadas += valor_peca
        if len(self.pecas_colocadas) == 4:
            if all(self.pecas_colocadas):
                input("O texto está certo.")
            else:
                vai = input("Tentar de novo?")
                if vai == "s":
                    self.inicia_de_novo()

    def nao_monta(self):
        pass

    def vai(self):
        self.monta()
        self.monta = self.nao_monta
        # self.centro.norte.vai()


class Jogo:
    def __init__(self, w=900, h=650, **kwargs):
        STYLE["width"], STYLE["height"] = w, f"{h}px"
        _ = kwargs
        self.c = Cena
        self.d = self.codigo = Codigo
        self.q = Sala
        self.salao = self.s = Salao
        self.a = Elemento
        self.texto = self.t = Popup
        self.n = Texto
        self.labirinto = self.l = Labirinto
        self.inventario = self.i = INVENTARIO
        self.portal = self.p = Portal
        self.dropper = self.d = Dropper
        self.droppable = self.r = Droppable
        self.musica = self.m = Musica
        self.codigo = Codigo
        self.document = document
        self.html = html
        self.window = win
        self.timer = timer
        pass

    @property
    def cena(self):
        """ Acessa a classe Cena"""
        return Cena

    @property
    def quarto(self):
        """ Acessa a classe Sala"""
        return Sala

    @property
    def sala(self):
        """ Acessa a classe Salao"""
        return Salao

    @property
    def algo(self):
        """ Acessa a classe Elemento"""
        return Elemento

    @property
    def nota(self):
        """ Acessa a classe Texto"""
        return Texto


def main(**kwargs):
    return Jogo(**kwargs)


if "__main__" in __name__:
    print("runnin tests")
    import doctest

    doctest.testmod(globs=dict(
        inv=Inventario(),
        ev=NoEv(),
        Cena=Cena,
        SalaCenaNula=SalaCenaNula,
        INVENTARIO=INVENTARIO,
        wraps_class_to_mimic_wrapped=wraps_class_to_mimic_wrapped,
        singleton=singleton
    ))
    # main()

CSS = '''
h1 {
  text-align: center;
  font-family: Tahoma, Arial, sans-serif;
  color: #06D85F;
  margin: 80px 0;
}

.box {
  width: 40%;
  margin: 0 auto;
  background: rgba(255,255,255,0.2);
  padding: 35px;
  border: 2px solid #fff;
  border-radius: 20px/50px;
  background-clip: padding-box;
  text-align: center;
}

.button {
  position: absolute;
  font-size: 1em;
  padding: 10px;
  color: #fff;
  border: 2px solid #FFF3;
  border-radius: 100px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease-out;
  left: 45%;
  top: 25%;
}
.button:hover {
  background: #777;
}

.overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 300ms;
}
.overlay:target {
  visibility: visible;
  opacity: 0.8;
}

.popup {
  top: 20%;
  margin: 70px auto;
  padding: 15px;
  background: #fff;
  border-radius: 10px;
  width: 85%;
  position: relative;
  transition: all 5s ease-in-out;
}

.popup h2 {
  margin-top: 0;
  color: #333;
  font-family: Tahoma, Arial, sans-serif;
}
.popup .close {
  position: absolute;
  top: 0px;
  right: 5px;
  transition: all 200ms;
  font-size: 30px;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}
.popup .option {
  transition: all 200ms;
  font-size: 30px;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}
.popup .close:hover {
  color: #06D85F;
}
.popup .option:hover {
  color: #06D85F;
}
.popup .content {
  max-height: 30%;
  overflow: auto;
}
'''


def __setup__():
    document.head <= html.STYLE(CSS, type="text/css", media="screen")
    Popup(Cena())


__setup__()
