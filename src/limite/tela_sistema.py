from limite.tela import Tela
import PySimpleGUI as sg


class TelaSistema(Tela):
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
        if event in (None, 'Encerrar Sistema'):
            opcao = 0

        self.fechar_tela()
        return opcao

    def iniciar_opcoes(self):
        layout = [
            [sg.Text('----- Sistema Cervejaria -----')],
            [sg.Text('Escolha o módulo desejado:')],
            [sg.Radio('Insumos', "RD1", key='1')],
            [sg.Radio('Receitas', "RD1", key='2')],
            [sg.Radio('Produções', "RD1", key='3')],
            [sg.Button('Confirmar'), sg.Exit('Encerrar Sistema')]
        ]
        self.__window = sg.Window('Sistema Cervejaria').Layout(layout)
