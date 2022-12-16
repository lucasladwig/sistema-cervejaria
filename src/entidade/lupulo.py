from entidade.insumo import Insumo


class Lupulo(Insumo):
    def __init__(self,
                 id: int,
                 variedade: str,
                 marca: str,
                 alfa_acidos: float,
                 oleos_totais: float):
        super().__init__(id, variedade, marca)
        self.__alfa_acidos = alfa_acidos
        self.__oleos_totais = oleos_totais

    @property
    def alfa_acidos(self):
        return self.__alfa_acidos

    @alfa_acidos.setter
    def alfa_acidos(self, alfa_acidos: float):
        self.__alfa_acidos = alfa_acidos

    @property
    def oleos_totais(self):
        return self.__oleos_totais

    @oleos_totais.setter
    def oleos_totais(self, oleos_totais: float):
        self.__oleos_totais = oleos_totais
