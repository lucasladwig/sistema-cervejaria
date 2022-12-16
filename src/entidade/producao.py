from entidade.receita import Receita
from datetime import date


class Producao():
    def __init__(self,
                 id: int,
                 receita: Receita,
                 volume: int,
                 data: date):
        self.__id = id
        self.__receita = receita
        self.__volume = volume
        self.__data = data

    # ATRIBUTOS
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def receita(self):
        return self.__receita

    @receita.setter
    def receita(self, receita: Receita):
        self.__receita = receita

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, volume: int):
        self.__volume = volume

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def ano(self):
        return self.data.year

    @property
    def mes(self):
        return self.data.month

    @property
    def dia(self):
        return self.data.day

    # METODOS
    def calcular_ingredientes(self):
        ingredientes = self.receita.listar_ingredientes()
        for ingr in ingredientes:
            ingredientes[ingr] *= self.volume

        return ingredientes
