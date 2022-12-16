from entidade.lupulo import Lupulo
from limite.tela_lupulo import TelaLupulo
from DAOs.lupulo_dao import LupuloDao
from exceptions.insumo_ja_existe_exception import InsumoJaExisteException
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class ControladorLupulos():

    def __init__(self, controlador_insumos):
        self.__controlador_insumos = controlador_insumos
        self.__tela_lupulo = TelaLupulo()
        self.__lupulo_DAO = LupuloDao()

    # NAVEGACAO
    def retornar(self):
        self.__controlador_insumos.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_lupulo,
                        2: self.alterar_lupulo,
                        3: self.excluir_lupulo,
                        4: self.listar_lupulos,
                        5: self.listar_lupulos_por_marca,
                        6: self.listar_lupulos_por_variedade,
                        0: self.retornar}
        while True:
            lista_opcoes[self.__tela_lupulo.tela_opcoes()]()

    # CRUD
    def incluir_lupulo(self):
        try:
            novos_dados_lupulo = self.__tela_lupulo.pegar_dados_lupulo()

            if not novos_dados_lupulo:
                raise ValueError

            lupulo = self.pegar_lupulo_por_marca_variedade(novos_dados_lupulo["marca"],
                                                           novos_dados_lupulo["variedade"])
            if lupulo is not None:
                raise InsumoJaExisteException(lupulo)
            else:
                novo_id = self.gerar_id()
                lupulo = Lupulo(novo_id,
                                novos_dados_lupulo["variedade"],
                                novos_dados_lupulo["marca"],
                                novos_dados_lupulo["alfa_acidos"],
                                novos_dados_lupulo["oleos_totais"])

                # salva alteração
                self.__lupulo_DAO.add(lupulo)

                # mostra resultado
                novos_dados_lupulo["id"] = novo_id
                dados_lupulo = []
                dados_lupulo.append(novos_dados_lupulo)
                self.__tela_lupulo.mostrar_lupulo(dados_lupulo)

        except InsumoJaExisteException as ije:
            self.__tela_lupulo.mostrar_mensagem(ije, titulo="Erro")

        except ValueError:
            pass

    def alterar_lupulo(self):
        try:
            if not self.__lupulo_DAO.get_all():
                raise InsumoNaoExisteException

            self.listar_lupulos()
            id_lupulo = self.__tela_lupulo.selecionar_lupulo_por_id()
            lupulo = self.pegar_lupulo_por_id(id_lupulo)

            if lupulo is not None:
                novos_dados_lupulo = self.__tela_lupulo.pegar_dados_lupulo()
                novos_dados_lupulo["id"] = id_lupulo
                lupulo.variedade = novos_dados_lupulo["variedade"]
                lupulo.marca = novos_dados_lupulo["marca"]
                lupulo.alfa_acidos = novos_dados_lupulo["alfa_acidos"]
                lupulo.oleos_totais = novos_dados_lupulo["oleos_totais"]

                # salva alteração
                self.__lupulo_DAO.add(lupulo)

                # mostra resultado
                dados_lupulo = []
                dados_lupulo.append(novos_dados_lupulo)
                self.__tela_lupulo.mostrar_lupulo(dados_lupulo)

            else:
                raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_lupulo.mostrar_mensagem(ine, titulo="Erro")

    def listar_lupulos(self):
        try:
            if not self.__lupulo_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                dados_lupulo = []
                for lupulo in self.__lupulo_DAO.get_all():
                    dados_lupulo.append(
                        {"id": lupulo.id,
                         "variedade": lupulo.variedade,
                         "marca": lupulo.marca,
                         "alfa_acidos": lupulo.alfa_acidos,
                         "oleos_totais": lupulo.oleos_totais})

                self.__tela_lupulo.mostrar_lupulo(dados_lupulo)

        except InsumoNaoExisteException as ine:
            self.__tela_lupulo.mostrar_mensagem(ine, titulo="Erro")

    def excluir_lupulo(self):
        try:
            if not self.__lupulo_DAO.get_all():
                raise InsumoNaoExisteException

            self.listar_lupulos()

            id_lupulo = self.__tela_lupulo.selecionar_lupulo_por_id()
            lupulo = self.pegar_lupulo_por_id(id_lupulo)

            if lupulo is None:
                raise InsumoNaoExisteException
            else:
                self.__lupulo_DAO.remove(id_lupulo)
                self.__tela_lupulo.mostrar_mensagem(
                    f"Lupulo de ID {id_lupulo} removido com sucesso!\n", titulo="Sucesso")

        except InsumoNaoExisteException as ine:
            self.__tela_lupulo.mostrar_mensagem(ine, titulo="Erro")

    def listar_lupulos_por_marca(self):
        try:
            if not self.__lupulo_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                marca = self.__tela_lupulo.selecionar_lupulo_por_marca()
                dados_lupulo = []

                for lupulo in self.__lupulo_DAO.get_all():
                    if marca.lower() == lupulo.marca.lower():
                        dados_lupulo.append(
                            {"id": lupulo.id,
                             "variedade": lupulo.variedade,
                             "marca": lupulo.marca,
                             "alfa_acidos": lupulo.alfa_acidos,
                             "oleos_totais": lupulo.oleos_totais})

                if dados_lupulo:
                    self.__tela_lupulo.mostrar_lupulo(dados_lupulo)
                else:
                    raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_lupulo.mostrar_mensagem(ine, titulo="Erro")

    def listar_lupulos_por_variedade(self):
        try:
            if not self.__lupulo_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                variedade = self.__tela_lupulo.selecionar_lupulo_por_variedade()
                dados_lupulo = []

                for lupulo in self.__lupulo_DAO.get_all():
                    if variedade.lower() == lupulo.variedade.lower():
                        dados_lupulo.append(
                            {"id": lupulo.id,
                             "variedade": lupulo.variedade,
                             "marca": lupulo.marca,
                             "alfa_acidos": lupulo.alfa_acidos,
                             "oleos_totais": lupulo.oleos_totais})

                if dados_lupulo:
                    self.__tela_lupulo.mostrar_lupulo(dados_lupulo)
                else:
                    raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_lupulo.mostrar_mensagem(ine, titulo="Erro")

    # METODOS AUXILIARES
    def gerar_id(self):
        if not self.__lupulo_DAO.get_all():
            lupulo_id = 0
        else:
            for lupulo in self.__lupulo_DAO.get_all():
                lupulo_id = lupulo.id
        return lupulo_id + 1

    def pegar_lupulo_por_id(self, id: int):
        for lupulo in self.__lupulo_DAO.get_all():
            if lupulo.id == id:
                return lupulo
        return None

    def pegar_lupulo_por_marca_variedade(self, marca: str, variedade: str):
        for lupulo in self.__lupulo_DAO.get_all():
            if (lupulo.variedade.lower() == variedade.lower()
                    and lupulo.marca.lower() == marca.lower()):
                return lupulo
            else:
                return None
