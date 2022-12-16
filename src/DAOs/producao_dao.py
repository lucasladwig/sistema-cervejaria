from DAOs.dao import DAO
from entidade.producao import Producao
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class ProducaoDao(DAO):
    def __init__(self):
        super().__init__('producaos.pkl')

    def add(self, producao: Producao):
        if ((producao is not None) and isinstance(producao, Producao) and isinstance(producao.id, int)):
            super().add(producao.id, producao)

    def update(self, producao: Producao):
        if ((producao is not None) and isinstance(producao, Producao) and isinstance(producao.id, int)):
            super().update(producao.id, producao, InsumoNaoExisteException)

    def get(self, id: int):
        if isinstance(id, int):
            return super().get(id, InsumoNaoExisteException)

    def remove(self, id: int):
        if isinstance(id, int):
            return super().remove(id, InsumoNaoExisteException)
