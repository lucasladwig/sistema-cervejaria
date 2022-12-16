from entidade.levedura import Levedura
from limite.tela_levedura import TelaLevedura
from DAOs.levedura_dao import LeveduraDao
from exceptions.insumo_ja_existe_exception import InsumoJaExisteException
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class ControladorLeveduras():

    def __init__(self, controlador_insumos):
        self.__controlador_insumos = controlador_insumos
        self.__tela_levedura = TelaLevedura()
        self.__levedura_DAO = LeveduraDao()

    # NAVEGACAO
    def retornar(self):
        self.__controlador_insumos.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_levedura,
                        2: self.alterar_levedura,
                        3: self.excluir_levedura,
                        4: self.listar_leveduras,
                        5: self.listar_leveduras_por_marca,
                        6: self.listar_leveduras_por_variedade,
                        0: self.retornar}
        while True:
            lista_opcoes[self.__tela_levedura.tela_opcoes()]()

    # CRUD
    def incluir_levedura(self):
        try:
            novos_dados_levedura = self.__tela_levedura.pegar_dados_levedura()

            if not novos_dados_levedura:
                raise ValueError

            levedura = self.pegar_levedura_por_marca_variedade(novos_dados_levedura["marca"],
                                                               novos_dados_levedura["variedade"])
            if levedura is not None:
                raise InsumoJaExisteException(levedura)
            else:
                novo_id = self.gerar_id()
                levedura = Levedura(novo_id,
                                    novos_dados_levedura["variedade"],
                                    novos_dados_levedura["marca"],
                                    novos_dados_levedura["atenuacao"],
                                    novos_dados_levedura["floculacao"])

                # salva alteração
                self.__levedura_DAO.add(levedura)

                # mostra resultado
                novos_dados_levedura["id"] = novo_id
                dados_levedura = []
                dados_levedura.append(novos_dados_levedura)
                self.__tela_levedura.mostrar_levedura(dados_levedura)

        except InsumoJaExisteException as ije:
            self.__tela_levedura.mostrar_mensagem(ije, titulo="Erro")

        except ValueError:
            pass

    def alterar_levedura(self):
        try:
            if not self.__levedura_DAO.get_all():
                raise InsumoNaoExisteException

            self.listar_leveduras()
            id_levedura = self.__tela_levedura.selecionar_levedura_por_id()
            levedura = self.pegar_levedura_por_id(id_levedura)

            if levedura is not None:
                novos_dados_levedura = self.__tela_levedura.pegar_dados_levedura()
                novos_dados_levedura["id"] = id_levedura
                levedura.variedade = novos_dados_levedura["variedade"]
                levedura.marca = novos_dados_levedura["marca"]
                levedura.atenuacao = novos_dados_levedura["atenuacao"]
                levedura.floculacao = novos_dados_levedura["floculacao"]

                # salva alteração
                self.__levedura_DAO.add(levedura)

                # mostra resultado
                dados_levedura = []
                dados_levedura.append(novos_dados_levedura)
                self.__tela_levedura.mostrar_levedura(dados_levedura)

            else:
                raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_levedura.mostrar_mensagem(ine, titulo="Erro")

    def listar_leveduras(self):
        try:
            if not self.__levedura_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                dados_levedura = []
                for levedura in self.__levedura_DAO.get_all():
                    dados_levedura.append(
                        {"id": levedura.id,
                         "variedade": levedura.variedade,
                         "marca": levedura.marca,
                         "atenuacao": levedura.atenuacao,
                         "floculacao": levedura.floculacao})

                self.__tela_levedura.mostrar_levedura(dados_levedura)

        except InsumoNaoExisteException as ine:
            self.__tela_levedura.mostrar_mensagem(ine, titulo="Erro")

    def excluir_levedura(self):
        try:
            if not self.__levedura_DAO.get_all():
                raise InsumoNaoExisteException

            self.listar_leveduras()

            id_levedura = self.__tela_levedura.selecionar_levedura_por_id()
            levedura = self.pegar_levedura_por_id(id_levedura)

            if levedura is None:
                raise InsumoNaoExisteException
            else:
                self.__levedura_DAO.remove(id_levedura)
                self.__tela_levedura.mostrar_mensagem(
                    f"Levedura de ID {id_levedura} removido com sucesso!\n", titulo="Sucesso")

        except InsumoNaoExisteException as ine:
            self.__tela_levedura.mostrar_mensagem(ine, titulo="Erro")

    def listar_leveduras_por_marca(self):
        try:
            if not self.__levedura_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                marca = self.__tela_levedura.selecionar_levedura_por_marca()
                dados_levedura = []

                for levedura in self.__levedura_DAO.get_all():
                    if marca.lower() == levedura.marca.lower():
                        dados_levedura.append(
                            {"id": levedura.id,
                             "variedade": levedura.variedade,
                             "marca": levedura.marca,
                             "atenuacao": levedura.atenuacao,
                             "floculacao": levedura.floculacao})

                if dados_levedura:
                    self.__tela_levedura.mostrar_levedura(dados_levedura)
                else:
                    raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_levedura.mostrar_mensagem(ine, titulo="Erro")

    def listar_leveduras_por_variedade(self):
        try:
            if not self.__levedura_DAO.get_all():
                raise InsumoNaoExisteException

            else:
                variedade = self.__tela_levedura.selecionar_levedura_por_variedade()
                dados_levedura = []

                for levedura in self.__levedura_DAO.get_all():
                    if variedade.lower() == levedura.variedade.lower():
                        dados_levedura.append(
                            {"id": levedura.id,
                             "variedade": levedura.variedade,
                             "marca": levedura.marca,
                             "atenuacao": levedura.atenuacao,
                             "floculacao": levedura.floculacao})

                if dados_levedura:
                    self.__tela_levedura.mostrar_levedura(dados_levedura)
                else:
                    raise InsumoNaoExisteException

        except InsumoNaoExisteException as ine:
            self.__tela_levedura.mostrar_mensagem(ine, titulo="Erro")

    # METODOS AUXILIARES
    def gerar_id(self):
        if not self.__levedura_DAO.get_all():
            levedura_id = 0
        else:
            for levedura in self.__levedura_DAO.get_all():
                levedura_id = levedura.id
        return levedura_id + 1

    def pegar_levedura_por_id(self, id: int):
        for levedura in self.__levedura_DAO.get_all():
            if levedura.id == id:
                return levedura
        return None

    def pegar_levedura_por_marca_variedade(self, marca: str, variedade: str):
        for levedura in self.__levedura_DAO.get_all():
            if (levedura.variedade.lower() == variedade.lower()
                    and levedura.marca.lower() == marca.lower()):
                return levedura
            else:
                return None
