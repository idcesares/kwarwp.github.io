#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Kwarwp
# Copyright 2010-2019 Carlo Oliveira <carlo@nce.ufrj.br>,
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

"""Kwarwp tutorial using a book metaphor.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from vitollino import main as vitollino_main

DICT = {}
COLA_NO_CADERNO = "Você acha uma folha e cola no caderno"
ENIGMA1 = "á?ido,#desoxirribonuc?eico,#t?po,#???ÂÂÂ possui,#armaze??r,#" \
          "in?ormação,#genét?ca,#?rande,#moléc?la,#fo?m??aÂÂÂ p?r,#nu?leotídeos,#" \
          "ap?esenta,#f?r?a,#?rgani?mo?,#eucariótic?s,#?it?côndrias".split("#")

DNA = "https://i.imgur.com/tEtZk2X.jpg"

TEXTO = [
    """<div style="width:100%; text-align: center;">
    <H2>KWARWP, UM RITUAL INDÍGENA</H2>
    <br>
    <img src="/image/abertura_kwarwpp.jpg" width=250 />
    </div>
    <br/><br/>
    A ganância do homem branco. Nenhum entendimento 
    do valor sagrado da terra. Nenhum entendimento do valor sagrado da vida.<br/>
    O valoroso curumim da tribo Guarani-Kaiowá observa
    aterrorizado o que sobrou de sua adeia. Tchuk enxuga suas lágrimas e segue seu caminho.
    """,
    """<div style="width:100%; text-align: center;">
    <H2>TERRA XAKRIABÁ</H2>
    <br>
    <img src="https://i.imgur.com/aHl1xfa.jpg" width=300 />
    </div>
    <br/><br/>Chamas e sange tingiram de vermelho
    o chão, o céu e o branco dos seus olhos, magoados de tanto chorar.
    A fome aperta, hora de buscar comida.
    """,
    """<div style="width:100%; text-align: center;">
    <H2>2 Os Cromossomos</H2>
    <br>
    <img src="https://i.imgur.com/mdHOJ9y.jpg" width=200 onclick="clica_elemento()"/>
    </div>
    <br/>
    Cromossomos são estruturas compostas de DNA que,
    por sua vez, carregam os genes de um ser vivo,
    responsáveis por definir as características físicas
    particulares de cada indivíduo.
    <br/>
    Os cromossomos estão localizados no núcleo das
    células do ser vivo. Os seres humanos
    possuem 46 cromossomos, divididos em 23 pares,
    sendo 44 autossomos e 2 sexuais.
    <br/><br/><span style="color:#FF0000;">
    Decifre o enigma para obter uma pista:</span><br/><br/>
    {}

    """,
    """<div style="width:100%; text-align: center;">
    <H2>Página 3 Os Genes</H2>
    <br>
    <img src="https://i.imgur.com/EXNWAPb.png" width=200 />
    </div>
    <br/><br/>
    Um gene é o menor fragmento de uma molécula de ADN (DNA) que possui
    informação completa para um caráter determinado.    <br/>
    Cada gene codifica uma determinada sequência de uma cadeia
    polipeptídica (união de aminoácidos que formam a proteína).
    O gene é formado por uma sequência de DNA
    (ácido desoxirribonucleico) e RNA (ácido ribonucleico),
    sendo este último responsável pela síntese de proteínas da célula.
    <br/>
    Um gene é constituído por vários fragmentos de ADN separados
    por sequências sem sentido.
    As parte com sentido servem para fabricar a proteína são denominadas
    Exons e as partes sem sentido intercaladas no gene, Introns.
    """

]
TEXTO[2] = TEXTO[2].format(" ".join(
    '<span style="color:#FF0000;">{}</span>'.format(w) for w in ENIGMA1))


class Livro:
    jogo = None

    def __init__(self, jogo):
        self.pagina_atual = 0
        self.pagina_final = 0
        self.jogo = jogo
        self.cena_livro_aberto = None
        self.clica_livro = self.abre_livro = lambda: None
        self.cena_onde_estou_no_jogo = None
        self.texto_da_pagina_do_livro = self.jogo.codigo(
            codigo="", topo=TEXTO[0],
            style=dict(left=60, top=0, width=380, margin="10px 0px"))
        jogo.i.inicia()
        self.cria_o_livro()
        self.index_itens()
        # cromo = self.cria_pagina(vai=lambda: self.cria_pagina(
        #     quadro=self.jogo.sala.A.sul, tit="pagina2", left=310, top=340))
        # jogo.clica_elemento = cromo.chave_cromossomo
        # cromo.chave_cromossomo(cena=self.jogo.sala.A.norte)

    def abre(self, *_):
        self.cena_livro_aberto.vai()

    def cria_o_livro(self):

        class PaginaAnterior:
            def __init__(self, livro_):
                self.livro = livro_

            def vai(self, *_):
                print("PaginaAnterior", self.livro.pagina_atual)
                if self.livro.pagina_atual == 0:
                    return False
                self.livro.pagina_atual -= 1
                self.livro.texto_da_pagina_do_livro.topo.html = TEXTO[self.livro.pagina_atual]

        _livro_fechado = "https://i.imgur.com/ty2fWuE.gif"
        _livro_aberto = "https://i.imgur.com/sI177hV.jpg"
        self.cena_livro_aberto = cena_livro = self.jogo.c(_livro_aberto, PaginaAnterior(self), self)
        self.texto_da_pagina_do_livro.entra(cena_livro)

        def abre_livro(*_):
            self.clica_livro = lambda: self.fecha_livro()
            self.cena_onde_estou_no_jogo = self.jogo.i.cena
            cena_livro.vai()

        self.abre_livro = abre_livro

    def clica_elemento(self):
        pass

    def cria_aviso(self, cena=None, msg="Esta Porta Está Trancada", tit="", foi=lambda: None):
        cena = cena if cena else self.jogo.i.cena

        class Aviso:
            def __init__(self, cena_=cena, tit_=tit, msg_=msg, jogo=self.jogo, foi_=foi):
                self.aviso = jogo.n(cena_, tit_, msg_, foi=foi_)
                cena_.meio = self

            def vai(self, *_):
                self.aviso.vai()

        return Aviso(cena)

    def cria_pagina(self, **kwargs):

        class Pagina:
            def __init__(self, quadro=None, tit="pagina1", left=160, top=530,
                         width=16, height="60px", aviso=COLA_NO_CADERNO, vai=lambda: object(), livro=self):
                self.livro, self.jogo, self.tit, self.agora_vai = livro, livro.jogo, tit, vai
                self.height, self.left, self.top, self.width = height, left, top, width
                self.quadro, self.tit, self.papel = quadro, tit, None
                self.aviso = self.jogo.n(quadro, aviso)  # , foi=livro)

            def vai(self, event=None):
                self.aviso.vai()
                self.jogo.i.bota(self.papel)
                self.jogo.i.tira(self.tit)
                self.livro.pagina_final += 1
                self.livro.pagina_atual += 1
                self.agora_vai()
                # self.nova.pagina_atual = 1
                event.stopPropagation() if event else None

        return Pagina(**kwargs) if kwargs else Pagina

    def nova_pagina(self, event=None):
        self.pagina_atual += 1
        self.pagina_final += 1
        event.stopPropagation() if event else None

    def index_itens(self):
        def xk(*_):
            Xakriaba(self.jogo).abre()
        ca = self.cena_livro_aberto
        param = dict(cena=ca, w=40, h=40)
        forest = self.jogo.a("/image/forest.jpg", x=480, y=80, w=300, h=500, tipo="cover")
        forest.entra(self.cena_livro_aberto)
        self.jogo.a("/image/saida.gif", tit="terra pataxó", x=662, y=145, **param)
        self.jogo.a("/image/saida.gif", tit="terra pataxó", x=560, y=240, **param)
        self.jogo.a("/image/saida.gif", tit="terra terena", x=663, y=240, **param)
        self.jogo.a("/image/saida.gif", tit="terra mundukuru", x=560, y=340, **param)
        self.jogo.a("/image/saida.gif", tit="terra pataxó", x=665, y=340, **param)
        self.jogo.a("/image/saida.gif", tit="terra pataxó", x=661, y=440, **param)
        self.jogo.a("/image/saida.gif", tit="terra pataxó", x=562, y=440, **param)
        mist = self.jogo.a("/image/mist.png", x=400, y=180, w=460, h=540, tipo="100% 100%", style=dict(opacity=0.7))
        mist.entra(self.cena_livro_aberto)
        mist = self.jogo.a("/image/mist.png", x=540, y=40, w=290, h=240, tipo="100% 100%", style=dict(opacity=0.7))
        mist.entra(self.cena_livro_aberto)
        self.jogo.a("/image/saida.gif", tit="terra xakriabá", x=510, y=140, vai=xk, **param)

    def fecha_livro(self, *_):
        self.clica_livro = self.abre_livro
        self.cena_onde_estou_no_jogo.vai()

    def _vai(self, *_):
        if self.pagina_atual == self.pagina_final:
            self.fecha_livro()
            return False
        self.pagina_atual += 1
        self.texto_da_pagina_do_livro.topo.html = TEXTO[self.pagina_atual]


class Xakriaba(Livro):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.cena = jogo.c()
        self.texto_da_pagina_do_livro.topo.html = TEXTO[1]
        self.texto_da_pagina_do_livro.code = '''print("xexéu")
if x or y: return True'''

    def index_itens(self):
        pass


class Main:

    def __init__(self, **kwargs):
        _ = kwargs
        self.j = j = vitollino_main()
        self.livro = Livro(j)

    def paint_scenes(self):
        self.livro.abre()


def main(**kwargs):
    return Main(**kwargs)


if __name__ == '__main__':
    main(**{})
