class ReceitaNaoExisteException(Exception):
    def __init__(self):
        self.__mensagem = "Receita não encontrada!\n"
        super().__init__(self.__mensagem)
