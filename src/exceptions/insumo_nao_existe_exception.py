class InsumoNaoExisteException(Exception):
    def __init__(self):
        self.__mensagem = "Insumo não encontrado!\n"
        super().__init__(self.__mensagem)
