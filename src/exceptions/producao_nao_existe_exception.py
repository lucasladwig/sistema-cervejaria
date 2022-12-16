class ProducaoNaoExisteException(Exception):
    def __init__(self):
        self.__mensagem = "Produção não encontrada!\n"
        super().__init__(self.__mensagem)
