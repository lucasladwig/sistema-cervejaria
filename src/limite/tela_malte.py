from limite.tela import Tela
import PySimpleGUI as sg


class TelaMalte(Tela):
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
            [sg.Text('----- Módulo Maltes -----')],
            [sg.Text('Escolha a ação desejada:')],
            [sg.Radio('Incluir Malte', "RD1", key='1')],
            [sg.Radio('Alterar Malte', "RD1", key='2')],
            [sg.Radio('Excluir Malte', "RD1", key='3')],
            [sg.Radio('Listar Maltes', "RD1", key='4')],
            [sg.Radio('Listar Maltes por Marca', "RD1", key='5')],
            [sg.Radio('Listar Maltes por Variedade', "RD1", key='6')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]
        self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

    # PEGAR DADOS
    def pegar_dados_malte(self):
        layout = [
            [sg.Text('----- Dados do Malte -----')],
            [sg.Text('Insira os dados do malte:')],
            [sg.Text('Variedade:', size=(20, 1)),
             sg.InputText('', key='variedade')],
            [sg.Text('Marca:', size=(20, 1)), sg.InputText('', key='marca')],
            [sg.Text('Cor (EBC):', size=(20, 1)),
             sg.InputText('', key='cor_ebc')],
            [sg.Text('Extrato (%):', size=(20, 1)),
             sg.InputText('', key='extrato')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

            event, values = self.abrir_tela()
            variedade = values['variedade'].title()
            marca = values['marca'].title()
            cor_ebc = int(values['cor_ebc'])
            extrato = int(values['extrato'])

            if (variedade.isnumeric()
                    or marca.isnumeric()
                    or 0 > extrato > 100
                    or cor_ebc < 0):
                raise ValueError

            self.fechar_tela()

            return {"variedade": variedade,
                    "marca": marca,
                    "cor_ebc": cor_ebc,
                    "extrato": extrato}

        except ValueError:
            self.mostrar_mensagem(
                ("Por favor insira os parâmetros de forma correta!\n"
                    + "Marca: texto\n"
                    + "Variedade: texto\n"
                    + "Cor (EBC): número inteiro\n"
                    + "Extrato potencial (%): número inteiro de 0 a 100\n"))
            self.fechar_tela()

    # MOSTRAR DADOS
    def mostrar_malte(self, dados_malte):
        string_maltes = "----- MALTES -----\n\n"
        for dado in dados_malte:
            string_maltes += f"ID {dado['id']}: {dado['marca']} - {dado['variedade']}\n"
            string_maltes += f"- Cor EBC: {dado['cor_ebc']}\n"
            string_maltes += f"- Extrato: {dado['extrato']}%\n\n"

        string_maltes = string_maltes[:-1]
        self.mostrar_mensagem(string_maltes, titulo="Lista de Maltes")

    def selecionar_malte_por_id(self):
        layout = [
            [sg.Text('----- ID do Malte -----')],
            [sg.Text('Insira o ID do malte que deseja selecionar:')],
            [sg.Text('ID:', size=(15, 1)), sg.InputText('', key='id')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window('Selecionar Malte por ID').Layout(layout)
            event, values = self.abrir_tela()
            id = int(values['id'])
            self.fechar_tela()
            return id

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um número inteiro.")
            self.fechar_tela()

    def selecionar_malte_por_marca(self):
        layout = [
            [sg.Text('----- Marca do Malte -----')],
            [sg.Text('Insira a marca do malte que deseja selecionar:')],
            [sg.Text('Marca:', size=(15, 1)), sg.InputText('', key='marca')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Malte por Marca').Layout(layout)
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

    def selecionar_malte_por_variedade(self):
        layout = [
            [sg.Text('----- Variedade do Malte -----')],
            [sg.Text('Insira a variedade do malte que deseja selecionar:')],
            [sg.Text('Variedade:', size=(15, 1)),
             sg.InputText('', key='variedade')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Malte por Variedade').Layout(layout)
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
