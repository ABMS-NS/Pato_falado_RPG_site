"""
Module for defining the Efeito class.
"""


class Efeito:
    def __init__(self, nome: str, duracao: int, ):
        self.nome = nome
        self.duracao = duracao

    def reduzir_duracao(self):
        if self.duracao > 0:
            self.duracao -= 1