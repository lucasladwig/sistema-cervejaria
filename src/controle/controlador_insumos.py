from limite.tela_insumos import TelaInsumos
from controle.controlador_maltes import ControladorMaltes
from controle.controlador_lupulos import ControladorLupulos
from controle.controlador_leveduras import ControladorLeveduras


class ControladorInsumos():

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__controlador_maltes = ControladorMaltes(self)
        self.__controlador_lupulos = ControladorLupulos(self)
        self.__controlador_leveduras = ControladorLeveduras(self)
        self.__tela_insumos = TelaInsumos()

    # ATRIBUTOS
    @property
    def controlador_maltes(self):
        return self.__controlador_maltes
    
    @property
    def controlador_lupulos(self):
        return self.__controlador_lupulos
    
    @property
    def controlador_leveduras(self):
        return self.__controlador_leveduras
    
    # NAVEGACAO
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.cadastrar_maltes,
                        2: self.cadastrar_lupulos,
                        3: self.cadastrar_leveduras,
                        0: self.retornar}
        while True:
            lista_opcoes[self.__tela_insumos.tela_opcoes()]()

    def cadastrar_maltes(self):
        self.controlador_maltes.abre_tela()

    def cadastrar_lupulos(self):
        self.controlador_lupulos.abre_tela()

    def cadastrar_leveduras(self):
        self.controlador_leveduras.abre_tela()
