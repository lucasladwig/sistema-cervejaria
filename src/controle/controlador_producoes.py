from entidade.producao import Producao
from entidade.receita import Receita
from limite.tela_producao import TelaProducao
from DAOs.producao_dao import ProducaoDao
from exceptions.producao_nao_existe_exception import ProducaoNaoExisteException
from exceptions.receita_nao_existe_exception import ReceitaNaoExisteException
from datetime import date


class ControladorProducoes():
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_producao = TelaProducao()
        self.__producao_DAO = ProducaoDao()

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @property
    def tela_producao(self):
        return self.__tela_producao

    # NAVEGACAO
    def retornar(self):
        self.controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_producao,
                        2: self.alterar_producao,
                        3: self.excluir_producao,
                        4: self.listar_producoes,
                        5: self.calcular_volume_receita_por_mes_ano,
                        6: self.calcular_receita_mais_produzida_mes_ano,
                        0: self.retornar}
        while True:
            lista_opcoes[self.tela_producao.tela_opcoes()]()

    # CRUD
    def incluir_producao(self):
        try:
            self.chamar_controlador_receitas().listar_receitas()
            id_receita = self.tela_producao.selecionar_id_receita()
            receita = self.chamar_controlador_receitas().pegar_receita_por_id(id_receita)

            if receita is None:
                raise ReceitaNaoExisteException

            dados_producao = self.tela_producao.pegar_dados_producao()

            data = date(dados_producao["ano"],
                        dados_producao["mes"],
                        dados_producao["dia"])

            novo_id = self.gerar_id()
            producao = Producao(novo_id,
                                receita,
                                dados_producao["volume"],
                                data)

            # salva alteração e mostra resultado
            self.__producao_DAO.add(producao)
            dados_producao["id"] = novo_id
            dados_producao["receita"] = receita.nome
            dados = []
            dados.append(dados_producao)
            self.tela_producao.mostrar_producao(dados)

        except ReceitaNaoExisteException as e:
            self.tela_producao.mostrar_mensagem(e)

        except ValueError:
            self.tela_producao.mostrar_mensagem("Dados inválidos!")

    def alterar_producao(self):
        try:
            if not self.__producao_DAO.get_all():
                raise ProducaoNaoExisteException

            self.listar_producoes()
            id_producao = self.tela_producao.selecionar_producao_por_id()
            producao = self.pegar_producao_por_id(id_producao)

            if producao is not None:
                novos_dados_producao = self.tela_producao.pegar_dados_producao()
                novos_dados_producao["id"] = id_producao
                data = date(novos_dados_producao["ano"],
                            novos_dados_producao["mes"],
                            novos_dados_producao["dia"])
                producao.volume = novos_dados_producao["volume"]
                producao.data = data
                novos_dados_producao['receita'] = producao.receita.nome

                # salva alteração
                self.__producao_DAO.add(producao)

                # mostra resultado
                dados_producao = []
                dados_producao.append(novos_dados_producao)
                self.tela_producao.mostrar_producao(dados_producao)
            else:
                raise ProducaoNaoExisteException

        except ProducaoNaoExisteException as e:
            self.tela_producao.mostrar_mensagem(e)

    def listar_producoes(self):
        try:
            if not self.__producao_DAO.get_all():
                raise ProducaoNaoExisteException

            dados_producao = []
            for producao in self.__producao_DAO.get_all():
                dados_producao.append({"id": producao.id,
                                       "receita": producao.receita.nome,
                                       "volume": producao.volume,
                                       "dia": producao.dia,
                                       "mes": producao.mes,
                                       "ano": producao.ano})

            self.__tela_producao.mostrar_producao(dados_producao)

        except ProducaoNaoExisteException as e:
            self.tela_producao.mostrar_mensagem(e, titulo="Erro")

    def excluir_producao(self):
        try:
            if not self.__producao_DAO.get_all():
                raise ProducaoNaoExisteException

            self.listar_producoes()
            id_producao = self.tela_producao.selecionar_producao_por_id()
            producao = self.pegar_producao_por_id(id_producao)

            if producao is not None:
                self.__producao_DAO.remove(id_producao)
                self.tela_producao.mostrar_mensagem(
                    f"Produção de ID {id_producao} removida com sucesso!", titulo="Sucesso")
            else:
                raise ProducaoNaoExisteException

        except ProducaoNaoExisteException as e:
            self.tela_producao.mostrar_mensagem(e, titulo="Erro")

    # RELATORIOS
    def calcular_volume_receita_por_mes_ano(self):
        try:
            if not self.__producao_DAO.get_all():
                raise ProducaoNaoExisteException

            # listar receitas
            self.chamar_controlador_receitas().listar_receitas()
            id_receita = self.tela_producao.selecionar_id_receita()
            receita = self.chamar_controlador_receitas().pegar_receita_por_id(id_receita)

            # escolher mês e ano
            mes_ano = self.tela_producao.selecionar_mes_ano()
            mes = mes_ano["mes"]
            ano = mes_ano["ano"]

            # calcular volume da receita produzido no mês
            volume_produzido = 0
            for producao in self.__producao_DAO.get_all():
                if producao.receita == receita and mes == producao.mes and ano == producao.ano:
                    volume_produzido += producao.volume

            nome = receita.nome

            self.tela_producao.mostrar_mensagem(
                f"Volume produzido de {nome} em {mes}/{ano}: {volume_produzido} L")

            return volume_produzido

        except ProducaoNaoExisteException as e:
            self.tela_producao.mostrar_mensagem(e)

    def calcular_receita_mais_produzida_mes_ano(self):
        try:
            if not self.__producao_DAO.get_all():
                raise ProducaoNaoExisteException

            # escolher mês e ano
            mes_ano = self.tela_producao.selecionar_mes_ano()
            mes = mes_ano["mes"]
            ano = mes_ano["ano"]

            # percorrer producoues e montar dicionario
            vol_receitas = {}
            for producao in self.__producao_DAO.get_all():
                if (mes == producao.mes and ano == producao.ano
                        and producao.receita not in vol_receitas.keys()):
                    vol_receitas[producao.receita] = producao.volume

                elif (mes == producao.mes and ano == producao.ano
                        and producao.receita in vol_receitas.keys()):
                    vol_receitas[producao.receita] += producao.volume

            # tratamento caso não haja receitas no periodo
            if not vol_receitas:
                raise ProducaoNaoExisteException

            # retornar receita mais produzida no periodo
            mais_produzida = max(vol_receitas, key=vol_receitas.get)
            receita = mais_produzida.nome
            volume = vol_receitas[mais_produzida]

            self.tela_producao.mostrar_mensagem(
                f"Receita mais produzida em {mes}/{ano}:")
            self.tela_producao.mostrar_mensagem(f"{receita} - {volume} L")

            return mais_produzida

        except ProducaoNaoExisteException as e:
            self.tela_producao.mostrar_mensagem(e)

    # METODOS AUXILIARES
    def gerar_id(self):
        if not self.__producao_DAO.get_all():
            producao_id = 0
        else:
            for producao in self.__producao_DAO.get_all():
                producao_id = producao.id
        return producao_id + 1

    def pegar_producao_por_id(self, id: int):
        for producao in self.__producao_DAO.get_all():
            if producao.id == id:
                return producao
        return None

    def pegar_producoes_por_data(self, data: date):
        producoes_data = []
        for producao in self.__producao_DAO.get_all():
            if producao.data == data:
                producoes_data.append(producao)
        if not producoes_data:
            return None
        return producoes_data

    def pegar_producao_por_receita(self, receita: Receita):
        producoes_receita = []
        for producao in self.__producao_DAO.get_all():
            if producao.receita == receita:
                producoes_receita.append(producao)
        if not producoes_receita:
            return None
        return producoes_receita

    def chamar_controlador_receitas(self):
        return self.controlador_sistema.controlador_receitas
