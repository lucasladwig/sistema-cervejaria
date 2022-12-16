from DAOs.dao import DAO
from entidade.lupulo import Lupulo
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class LupuloDao(DAO):
    def __init__(self):
        super().__init__('lupulos.pkl')

    def add(self, lupulo: Lupulo):
        if ((lupulo is not None) and isinstance(lupulo, Lupulo) and isinstance(lupulo.id, int)):
            super().add(lupulo.id, lupulo)

    def update(self, lupulo: Lupulo):
        if ((lupulo is not None) and isinstance(lupulo, Lupulo) and isinstance(lupulo.id, int)):
            super().update(lupulo.id, lupulo, InsumoNaoExisteException)

    def get(self, id: int):
        if isinstance(id, int):
            return super().get(id, InsumoNaoExisteException)

    def remove(self, id: int):
        if isinstance(id, int):
            return super().remove(id, InsumoNaoExisteException)
