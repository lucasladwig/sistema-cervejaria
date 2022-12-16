from DAOs.dao import DAO
from entidade.levedura import Levedura
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class LeveduraDao(DAO):
    def __init__(self):
        super().__init__('leveduras.pkl')

    def add(self, levedura: Levedura):
        if ((levedura is not None) and isinstance(levedura, Levedura) and isinstance(levedura.id, int)):
            super().add(levedura.id, levedura)

    def update(self, levedura: Levedura):
        if ((levedura is not None) and isinstance(levedura, Levedura) and isinstance(levedura.id, int)):
            super().update(levedura.id, levedura, InsumoNaoExisteException)

    def get(self, id: int):
        if isinstance(id, int):
            return super().get(id, InsumoNaoExisteException)

    def remove(self, id: int):
        if isinstance(id, int):
            return super().remove(id, InsumoNaoExisteException)
