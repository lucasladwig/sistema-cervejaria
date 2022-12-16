from entidade.malte import Malte
from limite.tela_malte import TelaMalte
from DAOs.malte_dao import MalteDao
from exceptions.insumo_ja_existe_exception import InsumoJaExisteException
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class ControladorMaltes():

    def __init__(self, controlador_insumos):
        self.__controlador_insumos = controlador_insumos
        self.__tela_malte = TelaMalte()
        self.__malte_DAO = MalteDao()

    # NAVEGACAO
    def retornar(self):
        self.__controlador_insumos.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_malte,
                        2: self.alterar_malte,
                        3: self.excluir_malte,
                        4: self.listar_maltes,
                        5: self.listar_maltes_por_marca,
                        6: self.listar_maltes_por_variedade,
                        0: self.retornar}
        while True:
            lista_opcoes[self.__tela_malte.tela_opcoes()]()

    # CRUD
    def incluir_malte(self):
        try:
            novos_dados_malte = self.__tela_malte.pegar_dados_malte()

            if not novos_dados_malte:
                raise ValueError

            malte = self.pegar_malte_por_marca_variedade(novos_dados_malte["marca"],
                                                         novos_dados_malte["variedade"])
            if malte is not None:
                raise InsumoJaExisteException(malte)
            else:
                novo_id = self.gerar_id()
                malte = Malte(novo_id,
                              novos_dados_malte["variedade"],
                              novos_dados_malte["marca"],
                              novos_dados_malte["cor_ebc"],
                              novos_dados_malte["extrato"])

                # salva alteração
                self.__malte_DAO.add(malte)

                # mostra resultado
                novos_dados_malte["id"] = novo_id
                dados_malte = []
                dados_malte.append(novos_dados_malte)
                self.__tela_malte.mostrar_malte(dados_malte)

        except InsumoJaExisteException as ije:
            self.__tela_malte.mostrar_mensagem(ije, titulo="Erro")

        except ValueError:
            pass

    def alterar_malte(self):
        try:
            if not self.__malte_DAO.get_all():
                raise InsumoNaoExisteException

            self.listar_maltes()
            id_malte = self.__tela_malte.selecionar_malte_por_id()
            malte = self.pegar_malte_por_id(id_malte)

            if malte is not None:
                novos_dados_malte = self.__tela_malte.pegar_dados_malte()
                novos_dados_malte["id"] = id_malte
                malte.variedade = novos_dados_malte["variedade"]
                malte.marca = novos_dados_malte["marca"]
                malte.cor_ebc = novos_dados_malte["cor_ebc"]
                malte.extrato = novos_dados_malte["extrato"]

                # salva alteração
                self.__malte_DAO.add(malte)

                # mostra resultado
                dados_malte = []
                dados_malte.append(novos_dados_malte)
                self.__tela_malte.mostrar_malte(dados_malte)

            else:
                raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_malte.mostrar_mensagem(ine, titulo="Erro")

    def listar_maltes(self):
        try:
            if not self.__malte_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                dados_malte = []
                for malte in self.__malte_DAO.get_all():
                    dados_malte.append(
                        {"id": malte.id,
                         "variedade": malte.variedade,
                         "marca": malte.marca,
                         "cor_ebc": malte.cor_ebc,
                         "extrato": malte.extrato})

                self.__tela_malte.mostrar_malte(dados_malte)

        except InsumoNaoExisteException as ine:
            self.__tela_malte.mostrar_mensagem(ine, titulo="Erro")

    def excluir_malte(self):
        try:
            if not self.__malte_DAO.get_all():
                raise InsumoNaoExisteException

            self.listar_maltes()

            id_malte = self.__tela_malte.selecionar_malte_por_id()
            malte = self.pegar_malte_por_id(id_malte)

            if malte is None:
                raise InsumoNaoExisteException
            else:
                self.__malte_DAO.remove(id_malte)
                self.__tela_malte.mostrar_mensagem(
                    f"Malte de ID {id_malte} removido com sucesso!\n", titulo="Sucesso")

        except InsumoNaoExisteException as ine:
            self.__tela_malte.mostrar_mensagem(ine, titulo="Erro")

    def listar_maltes_por_marca(self):
        try:
            if not self.__malte_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                marca = self.__tela_malte.selecionar_malte_por_marca()
                dados_malte = []

                for malte in self.__malte_DAO.get_all():
                    if marca.lower() == malte.marca.lower():
                        dados_malte.append(
                            {"id": malte.id,
                             "variedade": malte.variedade,
                             "marca": malte.marca,
                             "cor_ebc": malte.cor_ebc,
                             "extrato": malte.extrato})

                if dados_malte:
                    self.__tela_malte.mostrar_malte(dados_malte)
                else:
                    raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_malte.mostrar_mensagem(ine, titulo="Erro")

    def listar_maltes_por_variedade(self):
        try:
            if not self.__malte_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                variedade = self.__tela_malte.selecionar_malte_por_variedade()
                dados_malte = []

                for malte in self.__malte_DAO.get_all():
                    if variedade.lower() == malte.variedade.lower():
                        dados_malte.append(
                            {"id": malte.id,
                             "variedade": malte.variedade,
                             "marca": malte.marca,
                             "cor_ebc": malte.cor_ebc,
                             "extrato": malte.extrato})

                if dados_malte:
                    self.__tela_malte.mostrar_malte(dados_malte)
                else:
                    raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_malte.mostrar_mensagem(ine, titulo="Erro")

    # METODOS AUXILIARES
    def gerar_id(self):
        if not self.__malte_DAO.get_all():
            malte_id = 0
        else:
            for malte in self.__malte_DAO.get_all():
                malte_id = malte.id
        return malte_id + 1

    def pegar_malte_por_id(self, id: int):
        for malte in self.__malte_DAO.get_all():
            if malte.id == id:
                return malte
        return None

    def pegar_malte_por_marca_variedade(self, marca: str, variedade: str):
        for malte in self.__malte_DAO.get_all():
            if (malte.variedade.lower() == variedade.lower()
                    and malte.marca.lower() == marca.lower()):
                return malte
            else:
                return None
