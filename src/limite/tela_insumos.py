from limite.tela import Tela
import PySimpleGUI as sg


class TelaInsumos(Tela):
    def __init__(self):
        super().__init__()

    # ABRIR/FECHAR
    def abrir_tela(self):
        event, values = self.__window.Read()
        return event, values

    def fechar_tela(self):
        self.__window.Close()

    # NAVEGAÇÃO
    def tela_opcoes(self):
        self.iniciar_opcoes()
        event, values = self.__window.Read()
        opcao = 0

        # escolha de módulo
        if values['1']:
            opcao = 1
        if values['2']:
            opcao = 2
        if values['3']:
            opcao = 3

        # voltar ou encerrar
        if event in (None, 'Retornar'):
            opcao = 0

        self.fechar_tela()
        return opcao

    def iniciar_opcoes(self):
        layout = [
            [sg.Text('----- Módulo Insumos -----')],
            [sg.Text('Escolha o módulo desejado:')],
            [sg.Radio('Maltes', "RD1", key='1')],
            [sg.Radio('Lúpulos', "RD1", key='2')],
            [sg.Radio('Leveduras', "RD1", key='3')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]
        self.__window = sg.Window('Sistema Cervejaria').Layout(layout)
