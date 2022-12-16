from controle.controlador_insumos import ControladorInsumos
from controle.controlador_receitas import ControladorReceitas
from controle.controlador_producoes import ControladorProducoes
from limite.tela_sistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.__controlador_insumos = ControladorInsumos(self)
        self.__controlador_receitas = ControladorReceitas(self)
        self.__controlador_producoes = ControladorProducoes(self)
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_insumos(self):
        return self.__controlador_insumos
    
    @property
    def controlador_receitas(self):
        return self.__controlador_receitas

    @property
    def controlador_producoes(self):
        return self.__controlador_producoes

    def abre_tela(self):
        lista_opcoes = {1: self.cadastrar_insumos,
                        2: self.cadastrar_receitas,
                        3: self.cadastrar_producoes,                        
                        0: self.encerrar_sistema}

        while True:
            lista_opcoes[self.__tela_sistema.tela_opcoes()]()

    def inicializar_sistema(self):
        self.abre_tela()

    def cadastrar_insumos(self):
        self.controlador_insumos.abre_tela()    

    def cadastrar_receitas(self):
        self.controlador_receitas.abre_tela()

    def cadastrar_producoes(self):
        self.controlador_producoes.abre_tela()    

    def encerrar_sistema(self):
        exit(0)
