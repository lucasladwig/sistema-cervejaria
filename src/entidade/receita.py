from enum import Enum
from entidade.malte import Malte
from entidade.lupulo import Lupulo
from entidade.levedura import Levedura
from entidade.insumo import Insumo
from exceptions.insumo_ja_existe_exception import InsumoJaExisteException
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class TipoInsumo(Enum):
    MALTE = 1
    LUPULO = 2
    LEVEDURA = 3


class Receita():
    def __init__(self, id: int, nome: str):
        if isinstance(id, int) and isinstance(nome, str):
            self.__id = id
            self.__nome = nome
            self.__maltes = {}
            self.__lupulos = {}
            self.__levedura = {}

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if isinstance(id, int):
            self.__id = id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    def incluir_insumo_na_receita(self, insumo: Insumo, quantidade: float):
        if isinstance(insumo, Insumo):
            if isinstance(insumo, Malte):
                if self.verificar_malte_na_receita(insumo) == None:
                    self.__maltes[insumo] = quantidade
                    return insumo
                else:
                    raise InsumoJaExisteException(insumo)
            elif isinstance(insumo, Lupulo):
                if self.verificar_lupulo_na_receita(insumo) == None:
                    self.__lupulos[insumo] = quantidade
                    return insumo
                else:
                    raise InsumoJaExisteException(insumo)
            elif isinstance(insumo, Levedura):
                if self.verificar_levedura_na_receita(insumo) == None:
                    self.__levedura[insumo] = quantidade
                    return insumo
                else:
                    raise InsumoJaExisteException(insumo)

    def excluir_insumo_da_receita(self, insumo: Insumo):
        if isinstance(insumo, Insumo):
            if isinstance(insumo, Malte):
                if self.verificar_malte_na_receita(insumo):
                    for malte in self.__maltes:
                        if insumo.id == malte.id:
                            self.__maltes.pop(malte)
                            return insumo
                else:
                    raise InsumoNaoExisteException
            elif isinstance(insumo, Lupulo):
                if self.verificar_lupulo_na_receita(insumo):
                    for lupulo in self.__lupulos:
                        if insumo.id == lupulo.id:
                            self.__lupulos.pop(lupulo)
                            return insumo
                else:
                    raise InsumoNaoExisteException
            elif isinstance(insumo, Levedura):
                if self.verificar_levedura_na_receita(insumo):
                    for levedura in self.__levedura:
                        if insumo.id == levedura.id:
                            self.__levedura.pop(levedura)
                            return insumo
                else:
                    raise InsumoNaoExisteException

    def alterar_quantidade_insumo_receita(self, insumo: Insumo, quantidade: float):
        if isinstance(insumo, Insumo):
            if isinstance(insumo, Malte):
                if self.verificar_malte_na_receita(insumo):
                    self.__maltes[insumo] = quantidade
                    return {insumo: self.__maltes[insumo]}
                else:
                    raise InsumoNaoExisteException
            elif isinstance(insumo, Lupulo):
                if self.verificar_lupulo_na_receita(insumo):
                    self.__lupulos[insumo] = quantidade
                    return {insumo: self.__lupulos[insumo]}
                else:
                    raise InsumoNaoExisteException
            elif isinstance(insumo, Levedura):
                if self.verificar_levedura_na_receita(insumo):
                    self.__levedura[insumo] = quantidade
                    return {insumo: self.__levedura[insumo]}
                else:
                    raise InsumoNaoExisteException

    def listar_maltes(self):
        return self.__maltes

    def listar_lupulos(self):
        return self.__lupulos

    @property
    def levedura(self):
        return self.__levedura

    def listar_ingredientes(self):
        ingredientes = {}
        ingredientes.update(self.__maltes)
        ingredientes.update(self.__lupulos)
        ingredientes.update(self.__levedura)
        return ingredientes

    def verificar_malte_na_receita(self, malte: Malte):
        for mlt in self.__maltes:
            if malte.id == mlt.id:
                return malte        
        return None

    def verificar_lupulo_na_receita(self, lupulo: Lupulo):
        for lup in self.__lupulos:
            if lupulo.id == lup.id:
                return lupulo        
        return None

    def verificar_levedura_na_receita(self, levedura: Levedura):
        for lev in self.__levedura:
            if levedura.id == lev.id:
                return levedura
        return None
