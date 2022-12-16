class ProducaoJaExisteException(Exception):
    def __init__(self, producao):
        self.__mensagem = f"A produção de {producao.mes} de {producao.ano} já está cadastrada!\n"
        super().__init__(self.__mensagem)
