from abc import ABC, abstractmethod


class Insumo(ABC):
    @abstractmethod
    def __init__(self, id: int, variedade: str, marca: str):
        self.__id = id
        self.__variedade = variedade
        self.__marca = marca

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        self.__id = id

    @property
    def variedade(self):
        return self.__variedade

    @variedade.setter
    def variedade(self, variedade: str):
        self.__variedade = variedade

    @property
    def marca(self):
        return self.__marca

    @marca.setter
    def marca(self, marca: str):
        self.__marca = marca
