from entidade.receita import TipoInsumo, Receita
from limite.tela_receita import TelaReceita
from DAOs.receita_dao import ReceitaDao
from exceptions.insumo_ja_existe_exception import InsumoJaExisteException
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException
from exceptions.receita_ja_existe_exception import ReceitaJaExisteException
from exceptions.receita_nao_existe_exception import ReceitaNaoExisteException


class ControladorReceitas():
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_receita = TelaReceita()
        self.__receita_DAO = ReceitaDao()

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_receita,
                        2: self.adicionar_insumo_receita,
                        3: self.alterar_quantidade_insumo_receita,
                        4: self.remover_insumo_receita,
                        5: self.excluir_receita,
                        6: self.listar_receitas,
                        7: self.listar_ingredientes_receita,
                        0: self.retornar}
        while True:
            lista_opcoes[self.__tela_receita.tela_opcoes()]()

    # CRUD
    def incluir_receita(self):
        dados_receita = self.__tela_receita.pegar_dados_receita()
        receita = self.pegar_receita_por_nome(dados_receita["nome"])
        try:
            if receita is not None:
                raise ReceitaJaExisteException

            # gerar id e buscar receita
            novo_id = self.gerar_id()
            receita = Receita(novo_id, dados_receita["nome"])

            # maltes
            self.__tela_receita.mostrar_mensagem(
                "Escolha um malte para sua receita:", titulo="Malte")
            self.__controlador_sistema.controlador_insumos.controlador_maltes.listar_maltes()
            dados_malte = self.__tela_receita.pegar_dados_insumo()
            malte = self.__controlador_sistema.controlador_insumos.controlador_maltes.pegar_malte_por_id(
                dados_malte["id"])
            if malte == None:
                raise InsumoNaoExisteException
            receita.incluir_insumo_na_receita(
                malte, dados_malte["quantidade"])

            # lupulo
            self.__tela_receita.mostrar_mensagem(
                "Escolha um lupulo para sua receita:", titulo="Lúpulo")
            self.__controlador_sistema.controlador_insumos.controlador_lupulos.listar_lupulos()
            dados_lupulo = self.__tela_receita.pegar_dados_insumo()
            lupulo = self.__controlador_sistema.controlador_insumos.controlador_lupulos.pegar_lupulo_por_id(
                dados_lupulo["id"])
            if lupulo == None:
                raise InsumoNaoExisteException
            receita.incluir_insumo_na_receita(
                lupulo, dados_lupulo["quantidade"])

            # levedura
            self.__tela_receita.mostrar_mensagem(
                "Escolha uma levedura para sua receita:", titulo="Levedura")
            self.__controlador_sistema.controlador_insumos.controlador_leveduras.listar_leveduras()
            dados_levedura = self.__tela_receita.pegar_dados_insumo()
            levedura = self.__controlador_sistema.controlador_insumos.controlador_leveduras.pegar_levedura_por_id(
                dados_levedura["id"])
            if levedura == None:
                raise InsumoNaoExisteException
            receita.incluir_insumo_na_receita(
                levedura, dados_levedura["quantidade"])

            # salvar e mostrar receita
            self.__receita_DAO.add(receita)
            dados_receita.clear()
            dados_receita = {"id": receita.id, "nome": receita.nome}
            dados_malte, dados_lupulo, dados_levedura = self.tratar_dados_insumos_para_receita(
                receita)
            self.__tela_receita.mostrar_ingredientes_receita(
                dados_receita, dados_malte, dados_lupulo, dados_levedura)

        except ReceitaJaExisteException as rje:
            self.__tela_receita.mostrar_mensagem(rje, titulo="Erro")
        except InsumoNaoExisteException as ine:
            self.__tela_receita.mostrar_mensagem(ine, titulo="Erro")

    def adicionar_insumo_receita(self):
        try:
            if not self.__receita_DAO.get_all():
                raise ReceitaNaoExisteException

            # listar receitas
            self.listar_receitas()
            id_receita = self.__tela_receita.selecionar_receita_por_id()
            receita = self.pegar_receita_por_id(id_receita)
            if receita == None:
                raise ReceitaNaoExisteException

            self.__tela_receita.mostrar_mensagem(
                "Adicione um insumo à receita:", titulo="Insumo")
            insumo_opcao = self.__tela_receita.selecionar_tipo_insumo()

            # malte
            if insumo_opcao == TipoInsumo.MALTE.value:
                self.__controlador_sistema.controlador_insumos.controlador_maltes.listar_maltes()
                dados_malte = self.__tela_receita.pegar_dados_insumo()
                malte = self.__controlador_sistema.controlador_insumos.controlador_maltes.pegar_malte_por_id(
                    dados_malte["id"])
                if malte == None:
                    raise InsumoNaoExisteException
                receita.incluir_insumo_na_receita(
                    malte, dados_malte["quantidade"])

            # lupulo
            elif insumo_opcao == TipoInsumo.LUPULO.value:
                self.__controlador_sistema.controlador_insumos.controlador_lupulos.listar_lupulos()
                dados_lupulo = self.__tela_receita.pegar_dados_insumo()
                lupulo = self.__controlador_sistema.controlador_insumos.controlador_lupulos.pegar_lupulo_por_id(
                    dados_lupulo["id"])
                if lupulo == None:
                    raise InsumoNaoExisteException
                receita.incluir_insumo_na_receita(
                    lupulo, dados_lupulo["quantidade"])

            # levedura
            elif insumo_opcao == TipoInsumo.LEVEDURA.value:
                if len(receita.leveduras) > 0:
                    raise InsumoJaExisteException
                self.__controlador_sistema.controlador_insumos.controlador_leveduras.listar_leveduras()
                dados_levedura = self.__tela_receita.pegar_dados_insumo()
                levedura = self.__controlador_sistema.controlador_insumos.controlador_leveduras.pegar_levedura_por_id(
                    dados_levedura["id"])
                if levedura == None:
                    raise InsumoNaoExisteException
                receita.incluir_insumo_na_receita(
                    levedura, dados_levedura["quantidade"])

            # salvar e mostrar receita
            self.__receita_DAO.add(receita)
            dados_receita = {"id": receita.id, "nome": receita.nome}
            dados_malte, dados_lupulo, dados_levedura = self.tratar_dados_insumos_para_receita(
                receita)
            self.__tela_receita.mostrar_ingredientes_receita(
                dados_receita, dados_malte, dados_lupulo, dados_levedura)

        except ReceitaNaoExisteException as rne:
            self.__tela_receita.mostrar_mensagem(rne, titulo="Erro")
        except InsumoNaoExisteException as ine:
            self.__tela_receita.mostrar_mensagem(ine, titulo="Erro")
        except InsumoJaExisteException as ije:
            self.__tela_receita.mostrar_mensagem(ije, titulo="Erro")

    def alterar_quantidade_insumo_receita(self):
        try:
            if not self.__receita_DAO.get_all():
                raise ReceitaNaoExisteException

            # listar receitas
            self.listar_receitas()
            id_receita = self.__tela_receita.selecionar_receita_por_id()
            receita = self.pegar_receita_por_id(id_receita)
            if receita == None:
                raise ReceitaNaoExisteException

            dados_receita = {"id": receita.id, "nome": receita.nome}
            dados_malte, dados_lupulo, dados_levedura = self.tratar_dados_insumos_para_receita(
                receita)
            self.__tela_receita.mostrar_ingredientes_receita(
                dados_receita, dados_malte, dados_lupulo, dados_levedura)
            self.__tela_receita.mostrar_mensagem(
                "Alterar quantidade de insumo da receita:", titulo="Quantidade Insumo")

            # selecionar tipo de insumo
            tipo_insumo = self.__tela_receita.selecionar_tipo_insumo()
            # malte
            if tipo_insumo == TipoInsumo.MALTE.value:
                dados_insumo = self.__tela_receita.pegar_dados_insumo()
                malte = self.__controlador_sistema.controlador_insumos.controlador_maltes.pegar_malte_por_id(
                    dados_insumo["id"])
                if malte == None:
                    raise InsumoNaoExisteException
                receita.alterar_quantidade_insumo_receita(
                    malte, dados_insumo["quantidade"])
            # lupulo
            elif tipo_insumo == TipoInsumo.LUPULO.value:
                dados_insumo = self.__tela_receita.pegar_dados_insumo()
                lupulo = self.__controlador_sistema.controlador_insumos.controlador_lupulos.pegar_lupulo_por_id(
                    dados_insumo["id"])
                if lupulo == None:
                    raise InsumoNaoExisteException
                receita.alterar_quantidade_insumo_receita(
                    lupulo, dados_insumo["quantidade"])
            # levedura
            elif tipo_insumo == TipoInsumo.LEVEDURA.value:
                dados_insumo = self.__tela_receita.pegar_dados_insumo()
                levedura = self.__controlador_sistema.controlador_insumos.controlador_leveduras.pegar_levedura_por_id(
                    dados_insumo["id"])
                if levedura == None:
                    raise InsumoNaoExisteException
                receita.alterar_quantidade_insumo_receita(
                    levedura, dados_insumo["quantidade"])

            # salvar e mostrar receita
            self.__receita_DAO.update(receita)
            dados_malte.clear()
            dados_lupulo.clear()
            dados_levedura.clear()
            dados_malte, dados_lupulo, dados_levedura = self.tratar_dados_insumos_para_receita(
                receita)
            self.__tela_receita.mostrar_mensagem(
                "Receita alterada com sucesso!\n", titulo="Sucesso")
            self.__tela_receita.mostrar_ingredientes_receita(
                dados_receita, dados_malte, dados_lupulo, dados_levedura)

        except ReceitaNaoExisteException as rne:
            self.__tela_receita.mostrar_mensagem(rne, titulo="Erro")
        except InsumoNaoExisteException as ine:
            self.__tela_receita.mostrar_mensagem(ine, titulo="Erro")

    def remover_insumo_receita(self):
        try:
            if not self.__receita_DAO.get_all():
                raise ReceitaNaoExisteException

            # listar receitas
            self.listar_receitas()
            id_receita = self.__tela_receita.selecionar_receita_por_id()
            receita = self.pegar_receita_por_id(id_receita)
            if receita == None:
                raise ReceitaNaoExisteException

            dados_receita = {"id": receita.id, "nome": receita.nome}
            dados_malte, dados_lupulo, dados_levedura = self.tratar_dados_insumos_para_receita(
                receita)
            self.__tela_receita.mostrar_ingredientes_receita(
                dados_receita, dados_malte, dados_lupulo, dados_levedura)
            self.__tela_receita.mostrar_mensagem(
                "Remover insumo da receita:", titulo="Remover Insumo")

            # selecionar tipo
            tipo_insumo = self.__tela_receita.selecionar_tipo_insumo()

            # malte
            if tipo_insumo == TipoInsumo.MALTE.value:
                id_insumo = self.__tela_receita.pegar_id_insumo_receita()
                insumo = self.__controlador_sistema.controlador_insumos.controlador_maltes.pegar_malte_por_id(
                    id_insumo)
                if insumo == None:
                    raise InsumoNaoExisteException
                receita.excluir_insumo_da_receita(insumo)

            # lupulo
            elif tipo_insumo == TipoInsumo.LUPULO.value:
                id_insumo = self.__tela_receita.pegar_id_insumo_receita()
                insumo = self.__controlador_sistema.controlador_insumos.controlador_lupulos.pegar_lupulo_por_id(
                    id_insumo)
                if insumo == None:
                    raise InsumoNaoExisteException
                receita.excluir_insumo_da_receita(insumo)

            # levedura
            elif tipo_insumo == TipoInsumo.LEVEDURA.value:
                id_insumo = self.__tela_receita.pegar_id_insumo_receita()
                insumo = self.__controlador_sistema.controlador_insumos.controlador_leveduras.pegar_levedura_por_id(
                    id_insumo)
                if insumo == None:
                    raise InsumoNaoExisteException
                receita.excluir_insumo_da_receita(insumo)

            # salvar e mostrar receita
            self.__receita_DAO.update(receita)
            
            dados_malte.clear()
            dados_lupulo.clear()
            dados_levedura.clear()
            dados_malte, dados_lupulo, dados_levedura = self.tratar_dados_insumos_para_receita(
                receita)
            self.__tela_receita.mostrar_mensagem(
                f"Insumo de id {insumo.id} removido da receita com sucesso!\n", titulo="Sucesso")
            self.__tela_receita.mostrar_ingredientes_receita(
                dados_receita, dados_malte, dados_lupulo, dados_levedura)

        except ReceitaNaoExisteException as rne:
            self.__tela_receita.mostrar_mensagem(rne, titulo="Erro")
        except InsumoNaoExisteException as ine:
            self.__tela_receita.mostrar_mensagem(ine, titulo="Erro")

    def listar_receitas(self):
        try:
            if not self.__receita_DAO.get_all():
                raise ReceitaNaoExisteException

            dados_receita = []
            for receita in self.__receita_DAO.get_all():
                dados_receita.append({"id": receita.id,
                                      "nome": receita.nome})

            self.__tela_receita.mostrar_receita(dados_receita)

        except ReceitaNaoExisteException as rne:
            self.__tela_receita.mostrar_mensagem(rne, titulo="Erro")

    def listar_ingredientes_receita(self):
        try:
            if not self.__receita_DAO.get_all():
                raise ReceitaNaoExisteException

            self.listar_receitas()
            id_receita = self.__tela_receita.selecionar_receita_por_id()
            receita = self.pegar_receita_por_id(id_receita)

            if receita is not None:
                dados_receita = {"id": receita.id, "nome": receita.nome}
                dados_malte, dados_lupulo, dados_levedura = self.tratar_dados_insumos_para_receita(
                    receita)

                self.__tela_receita.mostrar_ingredientes_receita(
                    dados_receita, dados_malte, dados_lupulo, dados_levedura)

            else:
                raise ReceitaNaoExisteException

        except ReceitaNaoExisteException as rne:
            self.__tela_receita.mostrar_mensagem(rne, titulo="Erro")

    def excluir_receita(self):
        try:
            if not self.__receita_DAO.get_all():
                raise ReceitaNaoExisteException

            # listar receitas
            self.listar_receitas()
            id_receita = self.__tela_receita.selecionar_receita_por_id()
            receita = self.pegar_receita_por_id(id_receita)
            if receita == None:
                raise ReceitaNaoExisteException

            dados_receita = {"id": receita.id, "nome": receita.nome}
            dados_malte, dados_lupulo, dados_levedura = self.tratar_dados_insumos_para_receita(
                receita)

            # salvar e mostrar resultado
            self.__receita_DAO.remove(receita.id)
            self.__tela_receita.mostrar_mensagem(
                f"Receita de ID {id_receita} excluída com sucesso!\n", titulo="Sucesso")
            self.__tela_receita.mostrar_receita(
                dados_receita, dados_malte, dados_lupulo, dados_levedura)

        except ReceitaNaoExisteException as rne:
            self.__tela_receita.mostrar_mensagem(rne, titulo="Erro")

    # METODOS AUXILIARES
    def gerar_id(self):
        if not self.__receita_DAO.get_all():
            receita_id = 0
        else:
            for receita in self.__receita_DAO.get_all():
                receita_id = receita.id
        return receita_id + 1

    def pegar_receita_por_id(self, id: int):
        for receita in self.__receita_DAO.get_all():
            if receita.id == id:
                return receita
        return None

    def pegar_receita_por_nome(self, nome: str):
        for receita in self.__receita_DAO.get_all():
            if receita.nome.lower() == nome.lower():
                return receita
        return None

    def tratar_dados_insumos_para_receita(self, receita: Receita):
        dados_malte = {}
        dados_lupulo = {}
        dados_levedura = {}
        maltes = receita.listar_maltes()
        lupulos = receita.listar_lupulos()
        levedura_dict = receita.levedura
        for malte in maltes.keys():
            dados_malte[malte.id] = f"{malte.variedade} {malte.marca}: {maltes[malte]}g"
        for lupulo in lupulos.keys():
            dados_lupulo[lupulo.id] = f"{lupulo.variedade} {lupulo.marca}: {lupulos[lupulo]}g"
        for levedura in levedura_dict.keys():
            dados_levedura[levedura.id] = f"{levedura.variedade} {levedura.marca}: {levedura_dict[levedura]}g"
        return dados_malte, dados_lupulo, dados_levedura
