from limite.tela import Tela
import PySimpleGUI as sg


class TelaProducao(Tela):
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

        # voltar
        if event in (None, 'Retornar'):
            opcao = 0

        self.fechar_tela()
        return opcao

    def iniciar_opcoes(self):
        layout = [
            [sg.Text('----- Módulo Produções -----')],
            [sg.Text('Escolha a ação desejada:')],
            [sg.Radio('Incluir Produção', "RD1", key='1')],
            [sg.Radio('Alterar Produção', "RD1", key='2')],
            [sg.Radio('Excluir Produção', "RD1", key='3')],
            [sg.Radio('Listar Produções', "RD1", key='4')],
            [sg.Radio('Volume Produzido em um mês', "RD1", key='5')],
            [sg.Radio('Receita mais Produzida em um mês', "RD1", key='6')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]
        self.__window = sg.Window('Sistema Cervejaria').Layout(layout)

    # MOSTRAR DADOS
    def mostrar_producao(self, dados_producao):
        string_producao = "----- PRODUÇÕES -----\n\n"
        for dado in dados_producao:
            string_producao += f"ID {dado['id']} - Data: {dado['dia']}/{dado['mes']}/{dado['ano']} " + "\n"
            string_producao += f"- Receita: {dado['receita']}" + "\n"
            string_producao += f"- Volume: {dado['volume']}L" + "\n\n"

        string_producao = string_producao[:-1]
        self.mostrar_mensagem(string_producao, titulo="Lista de Produções")

    # PEGAR DADOS
    def pegar_dados_producao(self):
        layout = [
            [sg.Text('----- Dados da Produção -----')],
            [sg.Text('Insira os dados da Produção:')],
            [sg.Text('Volume Produzido (L):', size=(20, 1)),
             sg.InputText('', key='volume')],
            [sg.Text('Ano (2000+):', size=(20, 1)),
             sg.InputText('', key='ano')],
            [sg.Text('Mês (1-12):', size=(20, 1)),
             sg.InputText('', key='mes')],
            [sg.Text('Dia (1-31):', size=(20, 1)),
             sg.InputText('', key='dia')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window('Sistema Cervejaria').Layout(layout)
            event, values = self.abrir_tela()
            volume = int(values['volume'])
            ano = int(values['ano'])
            mes = int(values['mes'])
            dia = int(values['dia'])
            self.fechar_tela()

            if (0 < volume
                    and 1 <= dia <= 31
                    and 1 <= mes <= 12
                    and 2000 <= ano):
                return {"volume": volume,
                        "dia": dia,
                        "mes": mes,
                        "ano": ano}
            else:
                raise ValueError

        except ValueError:
            self.mostrar_mensagem(
                ("Por favor insira os parâmetros de forma correta!\n"
                    + "Volume: número inteiro positivo\n"
                    + "Dia (1-31): número inteiro\n"
                    + "Mês (1-12): número inteiro\n"
                    + "Ano (2000+): número inteiro\n"
                    + "Verifique se o mês tem menos de 31 dias!\n"))
            self.fechar_tela()

    def selecionar_id_receita(self):
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

    def selecionar_producao_por_id(self):
        layout = [
            [sg.Text('----- ID da Produção -----')],
            [sg.Text('Insira o ID da produção que deseja selecionar:')],
            [sg.Text('ID:', size=(15, 1)), sg.InputText('', key='id')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Produção por ID').Layout(layout)
            event, values = self.abrir_tela()
            id = int(values['id'])
            self.fechar_tela()
            return id

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um número inteiro.")

    def selecionar_mes_ano(self):
        layout = [
            [sg.Text('----- Mês e Ano da Produção -----')],
            [sg.Text('Insira o mês e o ano que deseja selecionar:')],
            [sg.Text('Ano (2000+):', size=(20, 1)),
             sg.InputText('', key='ano')],
            [sg.Text('Mês (1-12):', size=(20, 1)),
             sg.InputText('', key='mes')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        try:
            self.__window = sg.Window(
                'Selecionar Produções por Mês e Ano').Layout(layout)
            event, values = self.abrir_tela()
            ano = int(values['ano'])
            mes = int(values['mes'])
            self.fechar_tela()

            if 1 <= mes <= 12 and 1900 <= ano:
                return {"mes": mes, "ano": ano}
            else:
                raise ValueError

        except ValueError:
            self.mostrar_mensagem(
                "Entrada inválida! Insira um número inteiro.")

        try:
            print()
            print("---- DATA DA PRODUÇÃO -----")
            mes = int(input("Mês (1 a 12): "))
            ano = int(input("Ano (1900+): "))

            if 1 <= mes <= 12 and 1900 <= ano:
                return {"mes": mes, "ano": ano}
            else:
                raise ValueError

        except ValueError:
            self.mostrar_mensagem(
                ("Por favor insira os parâmetros de forma correta!\n"
                    + "Mês (1-12): número inteiro\n"
                    + "Ano (2000+): número inteiro\n"))
            self.fechar_tela()
