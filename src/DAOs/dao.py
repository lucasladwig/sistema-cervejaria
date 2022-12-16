from abc import ABC, abstractmethod
import pickle

class DAO(ABC):
    @abstractmethod
    def __init__(self, data_source: str):
        self.__data_source = data_source
        self.__cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.__cache, open(self.__data_source, 'wb'))

    def __load(self):
        self.__cache = pickle.load(open(self.__data_source, 'rb'))

    def add(self, key, obj: object):
        self.__cache[key] = obj
        self.__dump()

    def update(self, key, obj: object, exception: Exception):
        try:
            if (self.__cache[key] != None):
                self.__cache[key] = obj
                self.__dump()
        except KeyError:
            raise exception

    def get(self, key, exception: Exception):
        try:
            return self.__cache[key]
        except KeyError:
            raise exception

    def remove(self, key, exception: Exception):
        try:
            self.__cache.pop(key)
            self.__dump()
        except KeyError:
            raise exception

    def get_all(self):
        return self.__cache.values()
