#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Kuarup - Festival de jogos na aprendizagem de Python
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2012/03/17  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2010, `GPL <http://is.gd/3Udt>__. 
"""
__author__ = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "1.1 $Revision$"[10:-1]
__date__ = "2011/02/19 $Date$"

# import time
# from threading import Event, Thread
from .kuarupfest import Mapas
'''
try:
    from .tkinter_factory import GUI, CANVASW, CANVASH
except ImportError:
    from .svg_factory import GUI, CANVASW, CANVASH
'''
HS = 48
HX, HY = 1, 2
STEPX, STEPY = 32, 32
DX, DY = 0, 0
HDX, HDY = DX - 8, DY - 14
TWO1DR = range(-2, 3)
TWO2DR = [(x, y) for x in TWO1DR for y in TWO1DR]
FABRICA, ARGUMENTOS = 0, 1
GLIFO, NOME, IMAGEM, GRADE = 0, 1, 2, 3
CANVASW, CANVASH = 800, 600

'''
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
'''


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

# def enum(*sequential, **named):
#    enums = dict(zip(sequential, range(len(sequential))), **named)
#    return type('Enum', (), enums)
#
# TECLA = enum(ACIMA=111,ABAIXO=116,DIREITA=114,ESQUERDA=113,
#             BRANCO=65,ENTER=36,SOBE=112,DESCE=117,EMPURRA=97,PUXA=103)


class Elemento:
    TEMPO = 0

    def __init__(self, x=0, y=0, imgxy=int(HS * 0.7), imagem=None):
        """ Um elemento básico do Jogo.
        """
        self.x, self.y = x, y
        self.imgxy = imgxy
        self.image = self.cenario = self
        self.glifo_imagem = imagem
        self.cardinames = self.cardinals = self.heroImages = self.numHero = self.nextHead = 0
        self.curHero = self.vaiX = self.vaiY = 0
        self.acoes = self.terreno = self.implemento = self.canvas = self.curDirection = None

    def atravessa(self, movimento):
        movimento()

    def remove(self):
        pass

    def abandona(self, movimento, x=0, y=0):
        movimento()

    def empurrando(self, x, y, dx, dy, movement, canvas):
        pass

    def mover(self, x, y, glif, canvas=None):
        self.image = canvas.image(glif, x, y, HS*0.7, HS*0.7) if canvas else None
        pass

    def move(self, x, y, movimento, canvas):
        self.x, self.y = x, y
        self.pinta(canvas)
        movimento()

    def entra(self, cenario, x=0, y=0):
        self.cenario = cenario
        self.x, self.y = x, y
        # self.pinta(cenario.canvas)
        return self

    def sai(self, movimento, x=0, y=0):
        pass

    def olha(self, x=0, y=0):
        return self.glifo_imagem.split('.')[0]

    def pega(self, movimento, x=0, y=0):
        pass

    def larga(self, movimento, x=0, y=0):
        pass

    def fabricar(self, construtor, *argumento):
        pass

    def criar(self, canvas, fabrica, x, y, glifo='', nome='', imagem='', *args):
        instancia = fabrica(x=x, y=y)
        if imagem:
            instancia.glifo_imagem = imagem
            instancia.image = canvas.image(
                instancia.glifo_imagem, instancia.x * STEPX + DX,
                instancia.y * STEPY + DY, instancia.imgxy, instancia.imgxy)
        return instancia

    def pinta(self, canvas):
        imgxy = self.imgxy
        # print("self.x, self.y, self.glifo_imagem", self.x, self.y, self.glifo_imagem)
        self.image.mover(self.x * STEPX + DX, self.y * STEPY + DY, self.glifo_imagem, canvas=canvas)


class Empty(Elemento):
    """ um local vazio no cenário
    """

    def empurrando(self, x, y, dx, dy, movement, canvas=None):
        """ Empurra um item
        """
        movement()

    def pinta(self, canvas):
        pass

    def olha(self, x=0, y=0):
        return 'livre'


class Ar(Elemento):
    def fabricar(self, construtor, *argumento):
        global DX, DY, HDX, HDY
        HDX = DX = -HS//2
        HDY = DY = 2*HS//1.4
        HDX, HDY = DX - 8, DY - 7
        pass

    def _fabricar(self, construtor, *argumento):
        global DX, DY, HDX, HDY
        gx, gy = argumento[GRADE]
        DX = CANVASW // 2 - gx * 16
        DY = CANVASH // 2 - gy * 16
        HDX, HDY = DX - 8, DY - 7


class Animado(Elemento):
    def entra(self, terreno, x, y):
        """ o personagem avança para um novo terreno"""
        self.terreno = self.implemento = terreno
        return Empty()

    def remove(self):
        """ método inócuo para usar o personagem como uma imagem nula"""
        pass

    def criar(self, canvas, fabrica, x, y, glifo='', nome='', imagem=''):
        self.canvas, self.image = canvas, self
        self.cria_vetor_de_imagens(imagem)
        self.x, self.y = self.vaiX, self.vaiY = x, y
        self.pinta(canvas, x, y)
        self.acoes = {TECLA.ABAIXO: self.somos_da_patria_amada,
                      TECLA.ACIMA: self.em_frente_marche,
                      TECLA.DIREITA: self.direita_volver,
                      TECLA.ESQUERDA: self.esquerda_volver,
                      TECLA.SOBE: self.apresentar_armas,
                      TECLA.DESCE: self.des_can_saar,
                      TECLA.ENTER: self.luzes_camera_acao,
                      TECLA.BRANCO: self.somos_da_patria_amada,
                      TECLA.EMPURRA: self.empurrar,
                      TECLA.PUXA: self.empurrar}
        return self

    def define_comportamento(self):
        pass

    def cria_vetor_de_imagens(self, imagem):
        self.cardinames = [c for c in 'nesw']
        cardinals = [(0, 1), (1, 0), (0, -1), (-1, 0), ]
        self.cardinals = dict(zip(self.cardinames, cardinals))
        self.heroImages = [imagem % (direction, "%d") for direction in self.cardinames]
        self.numHero = 3
        self.nextHead = 0
        self.curHero = 0
        himage = self.heroImages[0] % self.curHero
        self.image = canvas.image(himage, 0, 0, HS, HS)

    def pinta(self, canvas, x=0, y=0, posicao_heroi=0):
        self.curHero = posicao_heroi or self.curHero + 1
        self.curDirection = self.nextHead
        self.x, self.y = self.vaiX, self.vaiY
        self.curHero = self.curHero % self.numHero
        nx, ny = self.x * STEPX + HDX, self.y * STEPY + HDY
        himage = self.heroImages[self.curDirection] % self.curHero
        self.image.mover(nx, ny, himage, canvas)

    def movimenta(self, direcao=None, x=10, y=10):
        """ Move um heroi
        """
        self.nextHead = direcao
        dx, dy = self.cardinals[self.cardinames[self.nextHead]]
        self.vaiX, self.vaiY = self.x + dx, self.y - dy
        self.terreno.move(
            self.vaiX, self.vaiY, self.vai_e_move, self.canvas)
        self.implemento.move(self.vaiX, self.vaiY, self.remove, self.canvas)

    def acao(self, evento):
        """ Age como um heroi
        """
        self.acoes[evento]()

    def em_frente_marche(self):
        self.terreno.avanca_tempo()
        self.terreno.abandona(
            lambda self=self, head=self.nextHead: self.movimenta(self.nextHead),
            self.x, self.y)

    def direita_volver(self):
        self.terreno.avanca_tempo()
        self.nextHead = abs((self.nextHead + 1) % 4)
        self.vaiX, self.vaiY = self.x, self.y
        self.pinta(self.canvas, posicao_heroi=1)

    def esquerda_volver(self):
        self.terreno.avanca_tempo()
        self.nextHead = (self.nextHead - 1) % 4
        self.vaiX, self.vaiY = self.x, self.y
        self.pinta(self.canvas, posicao_heroi=1)

    def aa_pon_tar(self):
        dx, dy = self.cardinals[self.cardinames[self.nextHead]]
        vaix, vaiy = self.vaiX, self.vaiY = self.x + dx, self.y - dy
        return self.terreno.olha(vaix, vaiy)

    def somos_da_patria_amada(self, texto=None):
        # self.r = self.canvas.rect(100, 66, 700, 128, color='forestgreen')
        if texto:
            self.canvas.text(400, 96, texto)
        else:
            self.canvas.text(400, 96, self.aa_pon_tar())

    def des_can_saar(self):
        self.terreno.avanca_tempo()
        dx, dy = self.cardinals[self.cardinames[self.nextHead]]
        vaix, vaiy = self.vaiX, self.vaiY = self.x + dx, self.y - dy
        self.implemento.empurrando(self.x, self.y, dx, dy, self.larga_o_implemento, self.canvas)
        # self.implemento.larga(self.larga_o_implemento,vaix, vaiy)

    def empurrando(self, x, y, dx, dy, movement, canvas=None):
        """ Empurra um item
        """
        movement()

    def empurrar(self):
        self.terreno.avanca_tempo()
        dx, dy = self.cardinals[self.cardinames[self.nextHead]]
        self.vaiX, self.vaiY = self.x + dx, self.y - dy
        self.terreno.empurrando(self.vaiX, self.vaiY, dx, dy,
                                self.em_frente_marche, self.canvas)

    def apresentar_armas(self):
        self.terreno.avanca_tempo()
        dx, dy = self.cardinals[self.cardinames[self.nextHead]]
        self.vaiX, self.vaiY = self.x + dx, self.y - dy
        self.terreno.pega(self.pega_o_implemento, self.vaiX, self.vaiY)

    def pega_o_implemento(self, implemento, sai):
        if self.implemento != self.terreno:
            return False
        sai()
        self.implemento = implemento
        self.implemento.move(self.x, self.y, self.remove, self.canvas)
        return True

    def larga_o_implemento(self):
        # self.implemento.move(
        #    self.vaiX, self.vaiY, self.remove, self.canvas)
        # self.terreno.adentra(self.implemento,self.vaiX,self.vaiY)
        self.implemento = self.terreno

    def inicia_comportamento(self):
        self.canvas.registra_executante(self.define_comportamento)
        self.inicia_comportamento = self.remove

    def luzes_camera_acao(self):
        self.inicia_comportamento()
        self.canvas.continua()

    def _avanca_tempo(self):
        self.canvas.espera()

    def executa_passo(self, comando, *arg):
        self._avanca_tempo()
        return comando(*arg)

    def vai_e_move(self):
        """ Move um heroi
        """
        self.pinta(self.canvas)


class Personagem(Animado):
    """ O personagem controlado pelo jogador conectado 
    """

    def olha(self):
        """ Retorna uma sring com o nome do objeto que o ator está encarando
        """
        return self.executa_passo(self.aa_pon_tar)

    def fala(self, *arg):
        """ Escreve na tela uma string passada como argumento
        """
        return self.executa_passo(self.somos_da_patria_amada, *arg)

    def anda(self):
        """ Move o ator na direção que ele está encarando
        """
        return self.executa_passo(self.em_frente_marche)

    def direita(self):
        """ O ator faz uma volta de 90 graus à direita
        """
        return self.executa_passo(self.direita_volver)

    def pega(self):
        """ Pega (n)um objeto adiante do ator
        """
        return self.executa_passo(self.apresentar_armas)

    def empurra(self):
        """ Empurra um objeto adiante do ator
        """
        return self.executa_passo(self.empurrar)

    def larga(self):
        """ Larga (d)um objeto adiante do ator
        """
        return self.executa_passo(self.des_can_saar)

    def esquerda(self):
        """ O ator faz uma volta de 90 graus à esquerda
        """
        return self.executa_passo(self.esquerda_volver)


class Fixo(Elemento):
    """ Um elemento que não se move e não se pode atravessar
    """

    def atravessa(self, movement):
        pass


class Borda(Elemento):
    """ A borda do cenário que não se move e não se pode atravessar
    """

    def atravessa(self, movement):
        pass

    def pinta(self, canvas):
        pass

    def olha(self, x=0, y=0):
        return 'floresta'


class Passante(Fixo):
    """ Um elemento que se move e se pode atravessar
    """

    def atravessa(self, movement):
        movement()

    def empurrando(self, x, y, dx, dy, movement, canvas=None):
        """ Empurra um item
        """
        movement()

    def pinta(self, canvas):
        pass


class Grudante(Fixo):
    """ Um elemento que se não move e que não deixa sair se entrar
    """

    def criar(self, canvas, fabrica, x, y, glifo='', nome='',
              imagem='', *args):
        instancia = fabrica(x=x, y=y)
        instancia.texto = args and args[0] or 'Você ficou grudado para sempre!'
        instancia.canvas = canvas
        if imagem:
            instancia.glifo_imagem = imagem
            instancia.pinta(canvas)
        return instancia

    def atravessa(self, movement):
        # self.r = self.canvas.rect(100, 66, 700, 128, color='forest green')
        self.canvas.text(400, 96, self.texto)
        movement()

    def abandona(self, movement, x=0, y=0):
        pass

    def empurrando(self, x, y, dx, dy, movement, canvas=None):
        """ Empurra um item
        """
        movement()


class Saida(Fixo):
    """ Um elemento que se não move e que é a porta de saída de um cenário
    """

    def criar(self, canvas, fabrica, x, y, glifo='', nome='',
              imagem='', *args):
        instancia = fabrica(x=x, y=y)
        instancia.texto = args and args[0] or 'Você achou a saída!'
        instancia.canvas = canvas
        if imagem:
            instancia.glifo_imagem = imagem
            instancia.image = canvas.image(
                instancia.glifo_imagem, instancia.x * STEPX + DX,
                instancia.y * STEPY + DY, instancia.imgxy, instancia.imgxy)
            instancia.image.img.onclick = lambda *_: canvas.do_reload()
        return instancia

    def atravessa(self, movement):
        # self.r = self.canvas.rect(100, 66, 700, 128, color='forest green')
        self.canvas.text(400, 96, 'Você achou a saída!')
        self.canvas.reload()

        movement()

    def abandona(self, movement, x=0, y=0):
        pass

    def empurrando(self, x, y, dx, dy, movement, canvas=None):
        """ Empurra um item
        """
        movement()


def variar(tipo, canvas, fabrica, x, y, glifo='', nome='',
           imagem='', alternativo=Empty, *args):
    if tipo.VAZIO == []:
        tipo.VAZIO = [canvas.escolha([True, False])]
        tipo.VAZIO += [not tipo.VAZIO[0]]
    if tipo.VAZIO.pop():
        instancia = alternativo()  # Passante(x,y, int(HS*0.2), imagem = 'livre.png')
        if instancia.glifo_imagem:
            instancia.pinta(canvas)
    else:
        instancia = fabrica(x=x, y=y)
        instancia.texto = args and args[0] or 'Você ficou grudado para sempre!'
        if imagem:
            instancia.glifo_imagem = imagem
            instancia.pinta(canvas)
    instancia.canvas = canvas
    return instancia


class Grande(Elemento):
    """ Um elemento que se pode pegar ou empurrar
    """

    def atravessa(self, movement):
        pass

    def pega(self, movimento, x=0, y=0):
        # self.cenario.sai(self,self.x,self.y)

        movimento(self, lambda: self.cenario.sai(self, self.x, self.y))

    def larga(self, movimento, x=0, y=0):
        self.cenario.move(x, y, movimento)

    def sai(self, movimento, x, y):
        self.cenario.sai(self, x, y)
        self.x, self.y = x, y
        movimento(self)

    def move(self, x, y, movimento, canvas):
        self.cenario.move(
            x, y, lambda self=self: self.vai_e_move(x, y, movimento, canvas))

    def vai_e_move(self, x, y, movimento, canvas):
        self.x, self.y = x, y
        self.pinta(canvas)
        movimento()

    def empurrando(self, x, y, dx, dy, movimento, canvas):
        nx, ny = self.x + dx, self.y - dy
        self.cenario.empurrando(nx, ny, dx, dy,
                                lambda self=self, x=nx, y=ny, m=movimento, c=canvas:
                                self.vai_e_empurra(x, y, m, c),
                                canvas)

    def vai_e_empurra(self, nx, ny, movimento, canvas):
        self.cenario.sai(self, self.x, self.y)
        self.cenario.adentra(self, nx, ny)
        self.x, self.y = nx, ny
        self.pinta(canvas)
        movimento()


class Pesado(Grande):
    """ Um elemento que se não se pode pegar mas se pode empurrar
    """

    def pega(self, movimento, x=0, y=0):
        pass

    def larga(self, movimento, x=0, y=0):
        pass


class Fragil(Elemento):
    """ Um elemento que se não se pode pegar e é destruído quando se passa
    """

    def sai(self, implemento, x, y):
        """ Sai um implemento do cenário
        """
        self.cenario.remover(self, self.x, self.y)
        return

    def pega(self, movimento, x=0, y=0):
        self.sai(self, self.x, self.y)

    def larga(self, movimento, x=0, y=0):
        self.sai(self, self.x, self.y)

    def atravessa(self, movimento):
        self.sai(self, self.x, self.y)
        movimento()

    def empurrando(self, x, y, dx, dy, movimento, canvas):
        self.sai(self, self.x, self.y)
        movimento()


class Varigrande(Grande):
    """ Um elemento que se pode pegar ou empurrar posicionado aleatoriamente
    """
    VAZIO = []

    def criar(self, canvas, fabrica, x, y, glifo='',
              nome='', imagem='', *args):
        return variar(Varigrande, canvas, fabrica, x, y, glifo, nome, imagem, *args)


class Variante(Grudante):
    """ Um elemento aleatório que se não move e que não deixa sair se entrar
    """
    VAZIO = []

    def criar(self, canvas, fabrica, x, y, glifo='',
              nome='', imagem='', *args):
        return variar(Variante, canvas, fabrica, x, y, glifo, nome, imagem, *args)


class Varifragil(Grudante):
    """ Um elemento que alterna fragil e um que se não move e que gruda
    """
    VAZIO = []

    def criar(self, canvas, fabrica, x, y, glifo='', nome='', imagem='',
              *args):
        return variar(Varifragil, canvas, fabrica, x, y, glifo, nome, imagem,
                      alternativo=lambda: Fragil(x=x, y=y, imagem='flor.gif'), *args)


class Cenario(Elemento):
    """ O cenário corrente onde os atores e objetos estão posicionados
    """

    def fabricar(self, construtor, *argumento):
        self.instance = construtor._fabricar_instancia(DX, DY, '#')
        construtor._inventario['#'][FABRICA] = self
        cenario, separador = argumento[GRADE][1:], argumento[GRADE][0]
        self.grade = construtor._fabricar_grade(cenario.split(separador), self)

    def criar(self, canvas, fabrica, x, y, glifo='', nome='', imagem='', *args):
        global HDX, HDY, DX, DY
        instancia = fabrica(x=x, y=y)
        instancia.temporizados = []
        grade = args[0][1:].split(args[0][0])
        imgxy = int(HS * 0.7)
        nx, ny = len(grade[0]), len(grade)
        instancia.ceu = canvas.image(
            'sky.gif', 0, 0, 800, 2 * imgxy)
        c = 800
        x = c / 2
        y = (x * x / c) / 20
        instancia.sol = canvas.image(
            'sun.gif', 0, y - 10, 2 * imgxy, 2 * imgxy)
        instancia.solpos = (-c / 2, c / 10, c / 2)
        if imagem:
            instancia.glifo_imagem = imagem
        # LDX, LDY = DX + imgxy, DY + imgxy
        HDX, HDY = 400-(nx*imgxy)/2-imgxy, 250 + 3 * imgxy - (ny*imgxy)/2-imgxy
        DX, DY = HDX*1.05, HDY*1.005
        HDX, HDY = HDX*0.98, HDY*0.98
        LDX, LDY = 400-(nx*imgxy)/2, 250 + 3 * imgxy - (ny*imgxy)/2
        # LDX, LDY = 0, 3 * imgxy
        # print("LDX, LDY = DX + imgxy, DY + imgxy", LDX, LDY, nx, ny, LDX + nx * imgxy, LDY + ny * imgxy)
        canvas.rect(
            LDX, LDY, nx * imgxy, ny * imgxy, color='navajowhite')
        # canvas.rect(
        #     LDX, LDY, LDX + nx * imgxy, LDY + ny * imgxy, color='navajowhite')
        return instancia

    def registra_tempo(self, registrado):
        self.temporizados.append(registrado)

    def avanca_tempo(self):
        """ Move o astro no céu
        """
        x, y, c = self.instance.solpos
        nx, ny = x + 2, (x * x / c) / 10.0 + 40
        self.instance.solpos = nx, ny, c
        self.instance.sol.translate(nx - x, ny - y)
        Elemento.TEMPO += 1
        for elemento in self.instance.temporizados:
            elemento.avanca_tempo()

    def empurrando(self, x, y, dx, dy, movement, canvas=None):
        """ Empurra um item
        """
        self.grade[y][x].empurrando(x, y, dx, dy, movement, canvas)

    def move(self, x, y, movement, canvas=None):
        """ Move um heroi
        """
        self.grade[y][x].atravessa(movement)
        return

    def abandona(self, movimento, x=0, y=0):
        self.grade[y][x].abandona(movimento)

    def adentra(self, implemento, x, y):
        """ Entra um implemento no cenário
        """
        self.grade[y][x].image.remove()
        self.grade[y][x] = implemento
        return

    def remover(self, implemento, x, y):
        """ Sai um implemento do cenário
        """
        implemento.image.remove()
        self.grade[y][x] = Empty()
        return

    def sai(self, implemento, x, y):
        """ Sai um implemento do cenário
        """
        # implemento.image.remove()
        self.grade[y][x] = Empty()
        return

    def olha(self, x=0, y=0):
        """ Move um heroi
        """
        return self.grade[y][x].olha(x, y)

    def pega(self, acao, x, y, canvas=None):
        """ Move um heroi
        """
        self.grade[y][x].pega(acao, x, y)
        return

    def pinta(self, canvas):
        pass


INVENTARIO = {'ar': Ar, 'cenario': Cenario, 'caminho': Empty, 'variante': Variante,
              'fixo': Fixo, 'ator': Personagem, 'grande': Grande, 'saida': Saida,
              'passante': Passante, 'varigrande': Varigrande, 'grudante': Grudante,
              'fragil': Fragil, 'pesado': Pesado, 'borda': Borda,
              'varifragil': Varifragil}
""" Dicionário com todos os tipos de objetos atores e cenários disponíveis
"""
_BD = u'©'


class Kuarup(Mapas):
    pass


class Kuarup(Personagem, Mapas):
    """ O terreno onde o Festival Kuarup é apresentado
    """

    def __init__(self, mapa=Kuarup.SIMPLES, indio=None, gui=None):
        """ Standard initialiser.
        """
        mapinha = mapa[-1][-1]
        separador = ',' in mapinha and ',' or ' '
        mapinha = mapinha.split(separador)
        imgxy = int(HS * 0.7)
        self.dx, dy = imgxy * len(mapinha[0]), imgxy * len(mapinha)
        # print("imgxy * len(mapinha[0])", self.dx, imgxy, len(mapinha[0]), len(mapinha))
        # self.dx, dy = STEPX * len(mapinha[0]) + 50, STEPY * len(mapinha) + 90
        self._mapa = mapa
        self.__gui = gui
        self.canvas = self._indio = None
        self.canvas = gui
        if indio:
            INVENTARIO['ator'] = indio

    def inicia(self):
        self._constroi_inventario_de_classes(self._mapa)
        self._indio = self._inventario['a'][FABRICA]
        self.canvas.inicia(self, self.dx)
        pass

    @property
    def indio(self):
        self._indio.luzes_camera_acao()
        return self._indio

    @indio.setter
    def indio(self, value):
        INVENTARIO['ator'] = value

    # indio = property(_get_indio, None)
    # "indio: retorna o herói do Kuarup"

    def _constroi_inventario_de_classes(self, inventario):
        """ Cria a descrição das classes disponíveis no inventário
        """
        self._inventario = dict(
            [(item[GLIFO], [INVENTARIO[item[NOME]](), item])
             for item in inventario])
        BORDER = Borda()
        self._inventario.update({_BD: [BORDER, (_BD, "borda", "livre.gif")]})
        fabrica = self._inventario['^']
        fabrica[FABRICA].fabricar(self, *fabrica[ARGUMENTOS])
        for fabrica in self._inventario.values():
            fabrica[FABRICA].fabricar(self, *fabrica[ARGUMENTOS])

    def _fabricar_instancia(self, x, y, tipo_de_classe):
        classe_a_fabricar = self._inventario[tipo_de_classe]
        fabrica_criada = classe_a_fabricar[FABRICA]
        argumentos = classe_a_fabricar[ARGUMENTOS]
        classe_fabricante = INVENTARIO[argumentos[NOME]]
        instancia_fabricada = fabrica_criada.criar(
            self.canvas, classe_fabricante, x, y, *argumentos)
        return instancia_fabricada

    def _fabricar_grade(self, cenario, terreno):
        def elem(x, y, row, c=cenario):
            return x, y, row[x]

        dx, dy = len(cenario[0]) + 2, len(cenario) + 2
        tops = _BD * dx
        # cenario = [tops]
        cenario = [tops] + [_BD + row + _BD for row in cenario] + [tops]
        return [
            [self._fabricar_instancia(*elem(x, y, row)).entra(terreno, x, y)
             for x in range(len(row))]
            for y, row in enumerate(cenario)]

    def quandoDisparaTemporizador(self, timerID):
        """ Acontece toda vez que o temporizador dispara.
        """
        pass

    def quandoApertaUmaTecla(self, ev):
        self._indio.acao(ev)
        pass


#############################################################################
# MAPA = [("*","cerca","fence.gif"),
# ("+","grande","stone.gif"),("=","caminho"),("a","ator","smkp-%s0%s.gif"),
# ("#","cenario","soil.gif","**********.*++======*.*=a==*===*.**********")]
# MAPA = "00~*&cerca&fence.gif^=&caminho^a&ator&smkp-%s0%s.gif~**********.*a=======*.*========*.**********~00"
#############################################################################
if __name__ == "__main__":
    mundo = Kuarup()
    mundo.inicia()
