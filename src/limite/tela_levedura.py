from limite.tela import Tela
import PySimpleGUI as sg


class TelaLevedura(Tela):
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
        event, values = self.abrir_tela()

        # escolha de módulo
        if values['1']:
            opcao = 1
        if values['2']:
            opcao = 2
        if values['3']:
            opcao = 3
        if values['4']:
            opcao = 4
        if values['5']:
            opcao = 5
        if values['6']:
            opcao = 6

        # voltar
        if event in (None, 'Retornar'):
            opcao = 0

        self.fechar_tela()
        return opcao

    def iniciar_opcoes(self):
        layout = [
            [sg.Text('----- Módulo Leveduras -----')],
            [sg.Text('Escolha a ação desejada:')],
            [sg.Radio('Incluir Levedura', "RD1", key='1')],
            [sg.Radio('Alterar Levedura', "RD1", key='2')],
            [sg.Radio('Excluir Levedura', "RD1", key='3')],
            [sg.Radio('Listar Leveduras', "RD1", key='4')],
            [sg.Radio('Listar Leveduras por Marca', "RD1", key='5')],
            [sg.Radio('Listar Leveduras por Variedade', "RD1", key='6')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]
        self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

    # PEGAR DADOS
    def pegar_dados_levedura(self):
        layout = [
            [sg.Text('----- Dados do Levedura -----')],
            [sg.Text('Insira os dados do levedura:')],
            [sg.Text('Variedade:', size=(25, 1)),
             sg.InputText('', key='variedade')],
            [sg.Text('Marca:', size=(25, 1)), sg.InputText('', key='marca')],
            [sg.Text('Atenuação (%):', size=(25, 1)),
             sg.InputText('', key='atenuacao')],
            [sg.Text('Floculação (alta/média/baixa):', size=(25, 1)),
             sg.InputText('', key='floculacao')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

            event, values = self.abrir_tela()
            variedade = values['variedade'].title()
            marca = values['marca'].title()
            atenuacao = int(values['atenuacao'])
            floculacao = values['floculacao'].title()

            if (variedade.isnumeric()
                    or marca.isnumeric()
                    or atenuacao < 0
                    or atenuacao > 100
                    or floculacao.isnumeric()):
                raise ValueError

            self.fechar_tela()

            return {"variedade": variedade,
                    "marca": marca,
                    "atenuacao": atenuacao,
                    "floculacao": floculacao}

        except ValueError:
            self.mostrar_mensagem(
                ("Por favor insira os parâmetros de forma correta!\n"
                    + "Marca: texto\n"
                    + "Variedade: texto\n"
                    + "Atenuação (%): número inteiro de 0 a 100\n"
                    + "Floculação: alta/média/baixa\n"))

            self.fechar_tela()

    # MOSTRAR DADOS
    def mostrar_levedura(self, dados_levedura):
        string_leveduras = "----- LEVEDURAS -----\n\n"
        for dado in dados_levedura:
            string_leveduras += f"ID {dado['id']}: {dado['marca']} - {dado['variedade']}\n"
            string_leveduras += f"- Atenuação: {dado['atenuacao']}%\n"
            string_leveduras += f"- Floculação: {dado['floculacao']}\n\n"

        string_leveduras = string_leveduras[:-1]
        self.mostrar_mensagem(string_leveduras, titulo="Lista de Leveduras")

    def selecionar_levedura_por_id(self):
        layout = [
            [sg.Text('----- ID do Levedura -----')],
            [sg.Text('Insira o ID do levedura que deseja selecionar:')],
            [sg.Text('ID:', size=(15, 1)), sg.InputText('', key='id')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Levedura por ID').Layout(layout)

            event, values = self.abrir_tela()
            id = int(values['id'])

            self.fechar_tela()

            return id

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um número inteiro.")
            self.fechar_tela()

    def selecionar_levedura_por_marca(self):
        layout = [
            [sg.Text('----- Marca do Levedura -----')],
            [sg.Text('Insira a marca do levedura que deseja selecionar:')],
            [sg.Text('Marca:', size=(15, 1)), sg.InputText('', key='marca')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Levedura por Marca').Layout(layout)

            event, values = self.abrir_tela()
            marca = values['marca'].lower()

            self.fechar_tela()

            if marca.isnumeric():
                raise ValueError

            return marca

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um texto.")
            self.fechar_tela()

    def selecionar_levedura_por_variedade(self):
        layout = [
            [sg.Text('----- Variedade do Levedura -----')],
            [sg.Text('Insira a variedade do levedura que deseja selecionar:')],
            [sg.Text('Variedade:', size=(15, 1)),
             sg.InputText('', key='variedade')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Levedura por Variedade').Layout(layout)

            event, values = self.abrir_tela()
            variedade = values['variedade'].lower()

            self.fechar_tela()

            if variedade.isnumeric():
                raise ValueError

            return variedade

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um texto.")
            self.fechar_tela()
