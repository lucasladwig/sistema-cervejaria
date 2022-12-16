from DAOs.dao import DAO
from entidade.receita import Receita
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class ReceitaDao(DAO):
    def __init__(self):
        super().__init__('receitas.pkl')

    def add(self, receita: Receita):
        if ((receita is not None) and isinstance(receita, Receita) and isinstance(receita.id, int)):
            super().add(receita.id, receita)

    def update(self, receita: Receita):
        if ((receita is not None) and isinstance(receita, Receita) and isinstance(receita.id, int)):
            super().update(receita.id, receita, InsumoNaoExisteException)

    def get(self, id: int):
        if isinstance(id, int):
            return super().get(id, InsumoNaoExisteException)

    def remove(self, id: int):
        if isinstance(id, int):
            return super().remove(id, InsumoNaoExisteException)
