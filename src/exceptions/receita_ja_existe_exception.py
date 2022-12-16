class ReceitaJaExisteException(Exception):
    def __init__(self):
        self.__mensagem = "Receita já cadastrada!\n"
        super().__init__(self.__mensagem)
