from entidade.insumo import Insumo


class Levedura(Insumo):
    def __init__(self,
                 id: int,
                 variedade: str,
                 marca: str,
                 atenuacao: int,
                 floculacao: str):
        super().__init__(id, variedade, marca)
        self.__atenuacao = atenuacao
        self.__floculacao = floculacao

    @property
    def atenuacao(self):
        return self.__atenuacao

    @atenuacao.setter
    def atenuacao(self, atenuacao: float):
        self.__atenuacao = atenuacao

    @property
    def floculacao(self):
        return self.__floculacao

    @floculacao.setter
    def floculacao(self, floculacao: str):
        self.__floculacao = floculacao
