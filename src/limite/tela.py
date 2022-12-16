from abc import ABC, abstractmethod
import PySimpleGUI as sg


class Tela(ABC):

    # INICIALIZAÇÃO
    @abstractmethod
    def __init__(self):
        self.__window = None
        self.iniciar_opcoes()

        # Tema padrão
        sg.ChangeLookAndFeel('DarkGrey2')
        sg.set_options(font=('Tahoma', 11))

    # CAPTURA ENTRADAS DO USUARIO
    @abstractmethod
    def tela_opcoes(self):
        pass

    # LAYOUT TELA
    @abstractmethod
    def iniciar_opcoes(self):
        pass

    # NAVEGAÇÃO
    def abrir_tela(self):
        event, values = self.__window.Read()
        return event, values

    def fechar_tela(self):
        self.__window.Close()

    # MOSTRAR MENSAGENS
    def mostrar_mensagem(self, msg, titulo=""):
        sg.popup(msg, title=titulo)
