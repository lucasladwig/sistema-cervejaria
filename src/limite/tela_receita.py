from limite.tela import Tela
import PySimpleGUI as sg


class TelaReceita(Tela):
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
        opcao = 0

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
        if values['7']:
            opcao = 7

        # voltar
        if event in (None, 'Retornar'):
            opcao = 0

        self.fechar_tela()
        return opcao

    def iniciar_opcoes(self):
        layout = [
            [sg.Text('----- Módulo Receitas -----')],
            [sg.Text('Escolha a ação desejada:')],
            [sg.Radio('Incluir Receita', "RD1", key='1')],
            [sg.Radio('Incluir Insumo na Receita', "RD1", key='2')],
            [sg.Radio('Alterar Quantidade de Insumo na Receita', "RD1", key='3')],
            [sg.Radio('Remover Insumo da Receita', "RD1", key='4')],
            [sg.Radio('Excluir Receita', "RD1", key='5')],
            [sg.Radio('Listar Receitas', "RD1", key='6')],
            [sg.Radio('Listar Ingredientes de Receita', "RD1", key='7')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]
        self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

    # PEGAR DADOS
    def pegar_dados_receita(self):
        layout = [
            [sg.Text('----- Dados da Receita -----')],
            [sg.Text('Insira os dados da Receita:')],
            [sg.Text('Nome da Receita:', size=(20, 1)),
             sg.InputText('', key='nome')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window('Sistema Cervejaria').Layout(layout)
            event, values = self.abrir_tela()
            nome = values['nome'].title()
            if nome.isnumeric():
                raise ValueError
            self.fechar_tela()
            return {"nome": nome}

        except ValueError:
            self.mostrar_mensagem(
                ("Por favor insira os parâmetros de forma correta!\n"
                    + "Nome: texto\n"))
            self.fechar_tela()

    def pegar_dados_insumo(self):
        layout = [
            [sg.Text('----- Dados do Insumo -----')],
            [sg.Text('Insira os dados do insumo que deseja selecionar:')],
            [sg.Text('ID do Insumo:', size=(20, 1)),
             sg.InputText('', key='id')],
            [sg.Text('Quantidade (g/L):', size=(20, 1)),
             sg.InputText('', key='quantidade')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

            event, values = self.abrir_tela()
            id = int(values['id'])
            quantidade = float(values['quantidade'])

            self.fechar_tela()

            return {"id": id,
                    "quantidade": quantidade}

        except ValueError:
            self.mostrar_mensagem(
                ("Por favor insira os parâmetros de forma correta!\n"
                    + "ID: número inteiro\n"
                    + "Quantidade: número (pode ser fracionário)\n"))

            self.fechar_tela()

    # MOSTRAR DADOS
    def mostrar_receita(self, dados_receita):
        string_receitas = "----- RECEITAS -----\n\n"
        for dado in dados_receita:
            string_receitas += f"ID {dado['id']}: {dado['nome']}" + "\n\n"

        string_receitas = string_receitas[:-1]
        self.mostrar_mensagem(string_receitas, titulo="Lista de Receitas")

    def mostrar_ingredientes_receita(self, dados_receita, dados_malte,
                                     dados_lupulo, dados_levedura):

        string_receitas = "----- RECEITA -----\n\n"
        string_receitas += f"{dados_receita['nome']} (ID {dados_receita['id']}):" + "\n\n"

        string_receitas += self.mostra_malte_receita(dados_malte)
        string_receitas += self.mostra_lupulo_receita(dados_lupulo)
        string_receitas += self.mostra_levedura_receita(dados_levedura)
        string_receitas = string_receitas[:-1]
        self.mostrar_mensagem(string_receitas, titulo="Lista de Ingredientes")

    def mostra_malte_receita(self, dados_malte_receita):
        string_malte = "Maltes:\n"
        for id in dados_malte_receita.keys():
            string_malte += f"- ID {id}: {dados_malte_receita[id]}\n"
        string_malte += "\n"
        return string_malte

    def mostra_lupulo_receita(self, dados_lupulo_receita):
        string_lupulo = "Lúpulos:\n"
        for id in dados_lupulo_receita.keys():
            string_lupulo += f"- ID {id}: {dados_lupulo_receita[id]}\n"
        string_lupulo += "\n"
        return string_lupulo

    def mostra_levedura_receita(self, dados_levedura_receita):
        string_levedura = "Levedura:\n"
        for id in dados_levedura_receita.keys():
            string_levedura += f"- ID {id}: {dados_levedura_receita[id]}\n"
        string_levedura += "\n"
        return string_levedura

    # SELEÇÃO
    def selecionar_receita_por_id(self):
        layout = [
            [sg.Text('----- ID da Receita -----')],
            [sg.Text('Insira o ID da receita que deseja selecionar:')],
            [sg.Text('ID:', size=(15, 1)), sg.InputText('', key='id')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Receita por ID').Layout(layout)
            event, values = self.abrir_tela()
            id = int(values['id'])
            self.fechar_tela()
            return id

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um número inteiro.")
            self.fechar_tela()

    def selecionar_tipo_insumo(self):
        layout = [
            [sg.Text('----- Tipo de Insumo -----')],
            [sg.Text('Selecione o tipo de insumo desejado:')],
            [sg.Radio('Malte', "RD1", key='1')],
            [sg.Radio('Lúpulo', "RD1", key='2')],
            [sg.Radio('Levedura', "RD1", key='3')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Selecionar Tipo de Insumo').Layout(layout)

        event, values = self.__window.Read()
        opcao = 0

        # escolha de tipo
        if values['1']:
            opcao = 1
        if values['2']:
            opcao = 2
        if values['3']:
            opcao = 3

        # voltar ou encerrar
        if event in (None, 'Cancelar'):
            opcao = 0

        self.fechar_tela()
        return opcao

    def pegar_id_insumo_receita(self):
        layout = [
            [sg.Text('----- ID do Insumo -----')],
            [sg.Text('Insira o ID do insumo que deseja selecionar:')],
            [sg.Text('ID:', size=(15, 1)), sg.InputText('', key='id')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Insumo por ID').Layout(layout)
            event, values = self.abrir_tela()
            id = int(values['id'])
            self.fechar_tela()
            return id

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um número inteiro.")
            self.fechar_tela()
