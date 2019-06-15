#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Kuarup - Festival de jogos na aprendizagem de Python
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/02/19  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2010, `GPL <http://is.gd/3Udt>__. 
"""
__author__ = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "1.0 $Revision$"[10:-1]
__date__ = "2011/02/19 $Date$"

# import Tkinter
# from threading import Event, Thread
# from kuarup import MundoKuarup, TECLA
# from random import choice, seed
# seed()
# IMAGEREPO = 'public/image/'


#############################################################################
MAPA = [
    ("^", "ar", "sky.gif", (10, 4)),
    ("*", "fixo", "cercado.gif"),
    ("+", "grande", "pedra.gif"),
    ("@", "variante", "piche.gif"),  # "voce ficou grudado"),
    ("O", "pesado", "tronco.gif"),
    ("&", "fragil", "flor.gif"),
    ("%", "varigrande", "onca.gif"),
    ("x", "saida", "saida.gif"),
    ("=", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
    ("#", "cenario", "soil.gif", ".**********.*@+O&&%%@*.*@a==*=@=x.**********")]
IMAPA = [
    ("^", "ar", "sky.gif", (10, 4)),
    ("=", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
    ("#", "cenario", "soil.gif", ".a=")]


class Mapas:
    MAPA = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("*", "fixo", "cercado.gif"),
        ("+", "grande", "pedra.gif"),
        ("@", "variante", "piche.gif"),  # "voce ficou grudado"),
        ("O", "pesado", "tronco.gif"),
        ("&", "fragil", "flor.gif"),
        ("%", "varigrande", "onca.gif"),
        ("x", "saida", "saida.gif"),
        ("=", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", ".**********.*@+O&&%%@*.*@a==*=@=x.**********")]
    SIMPLES = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("=", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", ".a=")]
    INICIO = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("o", "fixo", "cercado.gif"),
        ("r", "grande", "pedra.gif"),
        ("w", "grudante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", ''',oooooo,ow...x,o....o,o....o,o.a.ro,oooooo''')

    ]
    ROCHAS = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("o", "fixo", "cercado.gif"),
        ("r", "grande", "pedra.gif"),
        ("w", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
ooooooo
o..o..x
o..r..o
oa.o..o
ooooooo''')
    ]
    CORREDOR = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("o", "fixo", "cercado.gif"),
        ("r", "grande", "pedra.gif"),
        ("w", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
oooooooooooooo
oa...........x
oooooooooooooo''')
    ]
    CORREDOR_ROCHOSO = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("o", "fixo", "cercado.gif"),
        ("r", "grande", "pedra.gif"),
        ("w", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
oooooooooooooo
oa.rrrrrrrrr.x
oooooooooooooo''')
    ]
    E_PAU_E_PEDRA = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("o", "fixo", "cercado.gif"),
        ("r", "pesado", "pedra.gif"),
        ("t", "grande", "tronco.gif"),
        ("w", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
oo.ooooo
oxratr.o
ootoo.oo
oo.ootoo
o.rt.roo
ooooo.oo
oooooooo''')
    ]
    E_O_FIM = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("o", "fixo", "cercado.gif"),
        ("r", "pesado", "pedra.gif"),
        ("t", "grande", "tronco.gif"),
        ("w", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
oo.oooooo
oor.xoooo
ootoooooo
ootoatr.o
ootoootoo
ootoootoo
o.rtttroo
oooooo.oo
ooooooooo''')
    ]
    E_O_RESTO = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("o", "fixo", "cercado.gif"),
        ("r", "pesado", "pedra.gif"),
        ("t", "grande", "tronco.gif"),
        ("w", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
ooooo.ooooo.ooo
a.r.or.tr.or.tx
oo.ootoo.ootooo
ootoo.ootoo.ooo
oor.tr.or.tr.o.
oo.ooooo.oooooo
ooooooooooooooo''')
    ]
    DO_CAMINHO = [
        ("^", "ar", "sky.gif", (10, 4)),
        ("o", "fixo", "cercado.gif"),
        ("r", "pesado", "pedra.gif"),
        ("t", "grande", "tronco.gif"),
        ("w", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
ooooo.ooooo.ooo
a.r.or.tr.or.tx
oo.ootoo.ootooo
ootoo.ootoo.ooo
oor.tr.or.tr.o.
oo.ooooo.oooooo
ooooooooooooooo''')
    ]
    ZIGZAG = [
        ("^", "ar", "sky.gif", (15, 10)),
        ("o", "fixo", "cercado.gif"),
        ("r", "grande", "pedra.gif"),
        ("w", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
oooooooooooooo
o............x
o.oooooooooooo
o.o...........
o.oooooooooooo
o............o
oooooooooooo.o
...........o.o
oooooooooooo.o
oa...........o
oooooooooooooo''')
    ]
    BETUMES = [
        ("^", "ar", "sky.gif", (15, 10)),
        ("o", "fixo", "cercado.gif"),
        ("r", "grande", "pedra.gif"),
        ("W", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
ooxoo
o...o
oWoWo
o.a.o
ooooo''')
    ]
    BETUMES_ROCHAS = [
        ("^", "ar", "sky.gif", (15, 10)),
        ("o", "fixo", "cercado.gif"),
        ("R", "varigrande", "pedra.gif"),
        ("W", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
ooxoo
o...o
oRoRo
o.o.o
o.o.o
oWoWo
o.a.o
ooooo''')
    ]
    CARACOL = [
        ("^", "ar", "sky.gif", (15, 13)),
        ("o", "fixo", "cercado.gif"),
        ("R", "varigrande", "pedra.gif"),
        ("W", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
oooooooooooooo
o............o
o.oooooooooo.o
o.o........o.o
o.o.oooooo.o.o
o.o.o....o.o.o
o.o.o.oo.o.o.o
o.o.o.xo.o.o.o
o.o.oooo.o.o.o
o.o......o.o.o
o.oooooooo.o.o
o..........o.o
oooooooooooo.o
oa...........o
oooooooooooooo''')
    ]
    POR_ONDE = [
        ("^", "ar", "sky.gif", (15, 13)),
        ("o", "fixo", "cercado.gif"),
        ("R", "varigrande", "pedra.gif"),
        ("W", "variante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
.oooooooooooo
.o.......o..x
.o.o.o.o.o.oo
.o.o.o.o.o.o.
.oWoWoWoWoWo.
.o.o.o.o.o.o.
oo.o.o.o.o.o.
oa...oR..R.o.
oooooooooooo.''')
    ]
    RECORDAR_E_VIVER = [
        ("^", "ar", "sky.gif", (24, 7)),
        ("o", "fixo", "cercado.gif"),
        ("*", "fragil", "flor.gif"),
        ("r", "grande", "pedra.gif"),
        ("t", "pesado", "tronco.gif"),
        ("w", "grudante", "piche.gif"),
        ("W", "grudante", "livre.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
oxoooooooooooooooooooo
owrt.................o
o.oooooooooooooooooo.o
o...*.W.......*.W....o
oo.o.oWo.oWoWo.oWo.oWo
oa*W....*.W.......*..o
oooooooooooooooooooooo.''')
    ]
    PISA_NA_FULO = [
        ("^", "ar", "sky.gif", (15, 13)),
        ("o", "fixo", "cercado.gif"),
        ("&", "fragil", "flor.gif"),
        ("r", "grande", "pedra.gif"),
        ("t", "pesado", "tronco.gif"),
        ("m", "grudante", "livre.gif"),
        ("w", "grudante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
.oooooooooooo
.om.om.o...mo
.om&&&&m.m.oo
.om&mm&m&&&o.
.om&&m&&&m&o.
.o.m&m.m.mto.
oo.m&mmmmmro.
oam.&&&&&awx.
oooooooooooo.''')
    ]
    MIRAFLOR = [
        ("^", "ar", "sky.gif", (6, 14)),
        ("o", "fixo", "cercado.gif"),
        ("&", "fragil", "flor.gif"),
        ("*", "varifragil", "flor.gif"),
        ("r", "grande", "pedra.gif"),
        ("t", "pesado", "tronco.gif"),
        ("m", "varifragil", "livre.gif"),
        ("w", "grudante", "piche.gif"),
        ("x", "saida", "saida.gif"),
        (".", "caminho"), ("a", "ator", "smkp-%s0%s.gif"),
        ("#", "cenario", "soil.gif", '''
oooooo
o&&&&o
ommo&o
o&&o&o
ommo&o
o&&o&o
ommo&o
o&&o&o
ommo&o
o&&o&o
ommo&o
o&&oto
ommoro
o&&awx
oooooo''')
    ]


'''
class Tchuk(Kuarup):
    """ O personagem controlado pelo jogador conectado
    """

    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
        self.anda()
        self.pega()
        self.esquerda()
        self.esquerda()
        self.larga()
        self.direita()
        self.direita()
        self.anda()
        self.pega()
        self.esquerda()
        self.esquerda()
        self.larga()
        self.direita()
        self.direita()
        self.anda()
        self.pega()
        self.esquerda()
        self.esquerda()
        self.larga()
        self.direita()
        self.direita()
        self.anda()
        self.pega()
        self.esquerda()
        self.esquerda()
        self.larga()
        self.direita()
        self.direita()
        self.anda()
        self.pega()
        self.anda()
        self.anda()
        self.direita()
        self.anda()
    '''
