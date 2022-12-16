from entidade.insumo import Insumo


class Malte(Insumo):
    def __init__(self,
                 id: int,
                 variedade: str,
                 marca: str,
                 cor_ebc: int,
                 extrato: int):
        super().__init__(id, variedade, marca)
        self.__cor_ebc = cor_ebc
        self.__extrato = extrato

    @property
    def cor_ebc(self):
        return self.__cor_ebc

    @cor_ebc.setter
    def cor_ebc(self, cor_ebc: int):
        self.__cor_ebc = cor_ebc

    @property
    def extrato(self):
        return self.__extrato

    @extrato.setter
    def extrato(self, extrato: int):
        self.__extrato = extrato
