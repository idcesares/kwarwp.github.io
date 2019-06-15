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
from kuarup import Kuarup
from brython_factory import GUI
# from .kuarupfest import Mapas
CENAS = [
    'INICIO', 'ROCHAS', 'CORREDOR', 'CORREDOR_ROCHOSO', 'E_PAU_E_PEDRA', 'E_O_FIM', 'DO_CAMINHO', 'E_O_RESTO', 'ZIGZAG', 'CARACOL',
    'BETUMES', 'BETUMES_ROCHAS', 'POR_ONDE', 'RECORDAR_E_VIVER', 'PISA_NA_FULO',
    'MIRAFLOR',
    ]


class Cenas:
    INICIO = '''class Tchuk(Kuarup):
    """ Tchuk tenta proteger o pajé limpando a aldeia.
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
    '''

    ROCHAS = '''class Tchuk(Kuarup):
    """ Tchuk quer chegar na oca mas tem
        uma pedra no caminho.
        Use self.empurre() quando estiver
        de frente para a pedra.
    """
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
    '''

    CORREDOR = '''class Tchuk(Kuarup):
    """ Use o comando de repetição para
        repetir o comando self.anda().
        for cada_passo in range(4):
            self.anda()
    """
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
    '''

    CORREDOR_ROCHOSO = '''class Tchuk(Kuarup):
    """ Use o comando de repetição para
        remover cada pedra e chegar na oca.
        for cada_passo in range(4):
            self.anda()
            self.pega()
            # .....
    """
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
        for cada_passo in range(4):
            self.anda()
            self.pega()
            # Coloque aqui algo que largue
            # a  pedra atrás do índio
            # e volte ao caminho para
            # pegar a próxima pedra.
    '''

    E_PAU_E_PEDRA = '''class Tchuk(Kuarup):
    """ Use o comando de repetição para
        remover cada tronco e empurrar cada pedra e chegar na oca.
        for cada_passo in range(4):
            self.pega()
            self.anda()
            # .....
    """
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
        for cada_passo in range(4):
            self.pega()
            self.anda()
            # Coloque aqui algo que libere
            # o caminho de todo tronco
            # e cada pedra até chegar na oca
    '''

    E_O_FIM = '''class Tchuk(Kuarup):
    """ Use o comando de repetição para
        remover cada tronco e empurrar cada pedra e chegar na oca.
        for cada_passo in range(4):
            self.pega()
            self.anda()
            # .....
    """
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
        for cada_passo in range(4):
            self.pega()
            self.anda()
            # Coloque aqui algo que libere
            # o caminho de todo tronco
            # e cada pedra até chegar na oca
    '''

    ZIGZAG = '''class Tchuk(Kuarup):
    """ Crie um novo comportamento que
        possa caminhar por um corredor.
    """
    def caminha_por_um_corredor(self, quantos_passos):
        # Use um comando de repetição que anda
        # por quantos_passos forem pedidos.
        pass
        
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
        self.caminha_por_um_corredor(2)  # na verdade não é dois!!
        self.esquerda()
        self.caminha_por_um_corredor(2)  # na verdade não é dois!!
        # faça mais comandos até completar o Zigue Zaqgue
    '''

    CARACOL = '''class Tchuk(Kuarup):
    """ Use o comportamento que pode caminhar por um corredor.
        Ajuste para que funcione no Caracol.
        Use o comando self.olha() para saber
         se chegou ao fim do corredor.
    """
    def caminha_por_um_corredor(self):
        # Use um comando de repetição que
        # anda enquanto está livre.
        while self.olha == 'livre':
            self.anda()
        
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
        self.caminha_por_um_corredor()
        self.esquerda()
        self.caminha_por_um_corredor()
        # faça mais comandos até completar o Caracol
        # mas o melhor seria usar um for
    '''

    BETUMES = '''class Tchuk(Kuarup):
    """ Use o comando if para saber se tem um obstáculo à frente.
        Volte e tente outro caminho
    """
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
    '''

    BETUMES_ROCHAS = '''class Tchuk(Kuarup):
    """ Use o comando if para saber se tem um obstáculo à frente.
        Volte e tente outro caminho
    """
    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
    '''

    POR_ONDE = '''class Tchuk(Kuarup):
    """ Armazene em uma lista onde estão as flores
        para poder voltar pelo mesmo caminho.
    """
    def segue_pelo_caminho(self):
        # Desenvolva um jeito de seguir pelo caminho.
        # Guarde as guinadas na lista.
        guinada = "esquerda"
        self.caminho_das_flores.append(guinada)
        
    def volta_pelo_caminho(self):
        # Recupere a última guinada do caminho
        guinada = caminho_das_flores.pop()
        # Desenvolva um jeito de voltar pelo caminho.
    
    def define_comportamento(self):
        self.caminho_das_flores = []
        self.fala('olá a todos')
        self.direita()
   '''

    RECORDAR_E_VIVER = '''class Tchuk(Kuarup):
    """ Armazene em uma lista onde estão as flores
        para poder voltar pelo mesmo caminho.
    """
    def segue_pelo_caminho(self):
        # Desenvolva um jeito de seguir pelo caminho.
        # Guarde as guinadas na lista.
        guinada = "esquerda"
        self.caminho_das_flores.append(guinada)
        
    def volta_pelo_caminho(self):
        # Recupere a última guinada do caminho
        guinada = caminho_das_flores.pop()
        # Desenvolva um jeito de voltar pelo caminho.
    
    def define_comportamento(self):
        self.caminho_das_flores = []
        self.fala('olá a todos')
        self.direita()
    '''

    PISA_NA_FULO = '''class Tchuk(Kuarup):
    """ Armazene em uma lista onde estão as flores
        para poder voltar pelo mesmo caminho.
    """
    def segue_pelo_caminho(self):
        # Desenvolva um jeito de seguir pelo caminho.
        # Guarde as guinadas na lista.
        guinada = "esquerda"
        self.caminho_das_flores.append(guinada)
        
    def volta_pelo_caminho(self):
        # Recupere a última guinada do caminho
        guinada = caminho_das_flores.pop()
        # Desenvolva um jeito de voltar pelo caminho.
    
    def define_comportamento(self):
        self.caminho_das_flores = []
        self.fala('olá a todos')
        self.direita()
    '''

    MIRAFLOR = '''class Tchuk(Kuarup):
    """ Armazene em uma lista onde estão as flores
        para poder voltar pelo mesmo caminho.
    """
    def segue_pelo_caminho(self):
        # Desenvolva um jeito de seguir pelo caminho.
        # Guarde as guinadas na lista.
        guinada = "esquerda"
        self.caminho_das_flores.append(guinada)
        
    def volta_pelo_caminho(self):
        # Recupere a última guinada do caminho
        guinada = caminho_das_flores.pop()
        # Desenvolva um jeito de voltar pelo caminho.
    
    def define_comportamento(self):
        self.caminho_das_flores = []
        self.fala('olá a todos')
        self.direita()
    '''

    def __init__(self):
        pass


class Tchuk(Kuarup):
    """ O personagem controlado pelo jogador conectado
    """

    def define_comportamento(self):
        self.fala('olá a todos')
        self.direita()
        self.anda()


class Main:

    def __init__(self, **kwargs):
        self.count, self.kwargs = 0, kwargs
        self.doc, self.svg, self.cena, self.ht, self.alert, self.storage = [
            kwargs[key] for key in 'doc svg cena html alr sto'.split()]
        code = getattr(Cenas, self.cena, Cenas.CORREDOR_ROCHOSO)
        cena = getattr(Kuarup, self.cena, Kuarup.CORREDOR_ROCHOSO)
        self.scene = kwargs['cena'] = cena
        kwargs['code'] = code
        # kwargs = dict(svg=self.svg, document=self.doc, html=self.ht, win=wd, cena=cena)
        # self.panel = self.doc["svgdiv"]
        self.title = self.mundo = None
        # self.settings()

    def start(self, scene):
        def reload(slf=self, alert=False):
            slf.alert("você achou a saída") if alert else None
            slf.paint_scenes()
        code = self.storage[scene] if scene in self.storage else getattr(Cenas, scene, Cenas.CORREDOR_ROCHOSO)
        cena = getattr(Kuarup, scene, Kuarup.CORREDOR_ROCHOSO)
        self.kwargs.update(cena=cena, code=code, codename=scene)
        gui = GUI(reload, **self.kwargs)
        self.doc["pydiv"].html = ""
        self.mundo = Kuarup(cena, indio=Tchuk, gui=gui)
        self.mundo.inicia()

    def settings(self):
        # asyncio.ensure_future(process_file())
        print("self.queue.pop().__next__()")
        print("def main(doc, svg)")
        self.title = self.svg.text(
            'LOADING..', x=200, y=30,
            font_size=22, text_anchor="middle",
            style={"stroke": "yellow", "fill": "yellow"})
        self.panel <= self.title
        self.doc["svg_circle"].bind('click', self.mouseclick)
        # self.fill()

    def _fill(self, *_):
        def value(res):
            pass
        for it in range(0, 10):
            res = self.queue.get()
            print("def value(res):", res)
            # res() if hasattr(res, '__call__') else None
            res()

    # def fill(self, *_):
    #     for it in range(0, 10):
    #         self.queue.push(self.paint)

    def paint(self, *_):
        self.count += 1
        self.title.textContent = "Contagem {}".format(self.count)

    def _mouseclick(self, *_):
        print("self.queue.pop().__next__()")

    def mouseclick(self, *_):
        # nexter = self.queue.pop().__next__()
        print("self.queue.pop().__next__()", nexter)
        # nexter()

    def select_scene(self, scene):
        self.start(scene)

    def _splash_screen(self):
        """

        :return: 
        """
        ht = self.ht
        pyd = self.doc["pydiv"]
        # pyd.html = ''
        splash = ht.DIV(id='the_splash', style={'position': 'absolute', 'top': 66, 'left': 0})
        self.splash = splashimg = ht.IMG(src="/image/abertura_kwarwpp.jpg", width=800)
        splash <= splashimg
        pyd <= splash
        splash.onclick = lambda *_: self._paint_scenes()

    def _paint_scenes(self):
        """

        :return:
        """
        ht = self.ht
        pyd = self.doc["pydiv"]
        pyd.html = ''
        sky = ht.DIV(id='the_sky', style={'position': 'absolute', 'top': 0, 'left': 0})
        self.sky = skyimg = ht.IMG(src="/image/sky.gif")
        sky <= skyimg
        sun = ht.DIV(
            id='the_sun', style={'position': 'absolute', 'top': 0, 'left': 0,
                                 'animation-name': 'daylight', 'animation-duration': '300s'})
        sun <= ht.IMG(src="/image/sun.gif")
        pyd <= sky
        svg = ht.SVG(id="svgdiv", width="800", height="66")
        svg.setAttribute('height', "66")
        pyd <= svg
        pyd <= ht.DIV(id='selector', style={
            'position': 'relative', 'margin-top': '4px', 'display': 'flex',
            'max-width': '800px', 'flex-wrap': 'wrap', 'padding': '10px'})
        pyd <= sun
        self._paint_tasks()

    def paint_scenes(self):
        self._splash_screen()

    def _paint_tasks(self):
        ht = self.ht
        for scene in CENAS:
            the_scene = scene
            icon = ht.DIV(onclick=lambda *_: self.select_scene(scene))
            icon.setAttribute("style", 'flex:1;min-width: 160px; flex-wrap: wrap; margin: 10px;' +
                              'background-color: navajowhite; border-radius: 60px; padding:4px;')
            img = ht.IMG(src="/image/saida.gif", width=60, title=scene,
                         style=dict(display='block',  margin="0 auto"))
            # icon.onclick = lambda ev: self.select_scene(scene)
            img.onclick = lambda ev: self.select_scene(ev.target.title)
            div, span, legend = ht.DIV(), ht.H6(scene, style={'text-align': 'center'}), ht.LEGEND(scene)
            div <= img
            icon <= span
            icon <= div
            self.doc['selector'] <= icon


def main(**kwargs):
    Main(**kwargs)


if __name__ == '__main__':
    main(**{})
