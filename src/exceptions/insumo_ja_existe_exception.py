class InsumoJaExisteException(Exception):
    def __init__(self, insumo):
        self.__mensagem = f"O insumo {insumo.variedade} {insumo.marca} já está cadastrado!\n"
        super().__init__(self.__mensagem)        
