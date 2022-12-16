from DAOs.dao import DAO
from entidade.malte import Malte
from exceptions.insumo_nao_existe_exception import InsumoNaoExisteException


class MalteDao(DAO):
    def __init__(self):
        super().__init__('maltes.pkl')

    def add(self, malte: Malte):
        if ((malte is not None) and isinstance(malte, Malte) and isinstance(malte.id, int)):
            super().add(malte.id, malte)

    def update(self, malte: Malte):
        if ((malte is not None) and isinstance(malte, Malte) and isinstance(malte.id, int)):
            super().update(malte.id, malte, InsumoNaoExisteException)

    def get(self, id: int):
        if isinstance(id, int):
            return super().get(id, InsumoNaoExisteException)

    def remove(self, id: int):
        if isinstance(id, int):
            return super().remove(id, InsumoNaoExisteException)
