from limite.tela import Tela
import PySimpleGUI as sg


class TelaLupulo(Tela):
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
            [sg.Text('----- Módulo Lúpulos -----')],
            [sg.Text('Escolha a ação desejada:')],
            [sg.Radio('Incluir Lúpulo', "RD1", key='1')],
            [sg.Radio('Alterar Lúpulo', "RD1", key='2')],
            [sg.Radio('Excluir Lúpulo', "RD1", key='3')],
            [sg.Radio('Listar Lúpulos', "RD1", key='4')],
            [sg.Radio('Listar Lúpulos por Marca', "RD1", key='5')],
            [sg.Radio('Listar Lúpulos por Variedade', "RD1", key='6')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]
        self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

    # PEGAR DADOS
    def pegar_dados_lupulo(self):
        layout = [
            [sg.Text('----- Dados do Lúpulo -----')],
            [sg.Text('Insira os dados do lúpulo:')],
            [sg.Text('Variedade:', size=(20, 1)),
             sg.InputText('', key='variedade')],
            [sg.Text('Marca:', size=(20, 1)), sg.InputText('', key='marca')],
            [sg.Text('Alfa-ácidos (%):', size=(20, 1)),
             sg.InputText('', key='alfa_acidos')],
            [sg.Text('Óleos Totais (ml/100g):', size=(20, 1)),
             sg.InputText('', key='oleos_totais')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

            event, values = self.abrir_tela()
            variedade = values['variedade'].title()
            marca = values['marca'].title()
            alfa_acidos = float(values['alfa_acidos'])
            oleos_totais = float(values['oleos_totais'])

            if (variedade.isnumeric() or marca.isnumeric() or
                    0 > alfa_acidos > 100 or oleos_totais < 0):
                raise ValueError

            self.fechar_tela()

            return {"variedade": variedade,
                    "marca": marca,
                    "alfa_acidos": alfa_acidos,
                    "oleos_totais": oleos_totais}

        except ValueError:
            self.mostrar_mensagem(
                ("Por favor insira os parâmetros de forma correta!\n"
                    + "Marca: texto\n"
                    + "Variedade: texto\n"
                    + "Alfa-ácidos (%): número fracionário de 0 a 100 \n"
                    + "Óleos Totais (ml/100g): número fracionário de 0 a 100\n"))

            self.fechar_tela()

    # MOSTRAR DADOS
    def mostrar_lupulo(self, dados_lupulo):
        string_lupulos = "----- LÚPULOS -----\n\n"
        for dado in dados_lupulo:
            string_lupulos += f"ID {dado['id']}: {dado['marca']} - {dado['variedade']}\n"
            string_lupulos += f"- Alfa-ácidos: {dado['alfa_acidos']}%\n"
            string_lupulos += f"- Óleos Totais: {dado['oleos_totais']}ml/100g\n\n"

        string_lupulos = string_lupulos[:-1]
        self.mostrar_mensagem(string_lupulos, titulo="Lista de Lúpulos")

    def selecionar_lupulo_por_id(self):
        layout = [
            [sg.Text('----- ID do Lúpulo -----')],
            [sg.Text('Insira o ID do lúpulo que deseja selecionar:')],
            [sg.Text('ID:', size=(15, 1)), sg.InputText('', key='id')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Lúpulo por ID').Layout(layout)

            event, values = self.abrir_tela()
            id = int(values['id'])

            self.fechar_tela()

            return id

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um número inteiro.")
            self.fechar_tela()

    def selecionar_lupulo_por_marca(self):
        layout = [
            [sg.Text('----- Marca do Lúpulo -----')],
            [sg.Text('Insira a marca do lúpulo que deseja selecionar:')],
            [sg.Text('Marca:', size=(15, 1)), sg.InputText('', key='marca')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Lúpulo por Marca').Layout(layout)

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

    def selecionar_lupulo_por_variedade(self):
        layout = [
            [sg.Text('----- Variedade do Lúpulo -----')],
            [sg.Text('Insira a variedade do lúpulo que deseja selecionar:')],
            [sg.Text('Variedade:', size=(15, 1)),
             sg.InputText('', key='variedade')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Lúpulo por Variedade').Layout(layout)

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
