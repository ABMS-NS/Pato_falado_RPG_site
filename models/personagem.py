"""
Module for defining the Personagem class.
"""


class Personagem:
    def __init__(self, nome, imagem):
        self.nome = nome
        self.imagem = imagem
        self.barras = [] #ela vai receber dicionarios para cada barra nova que for posta
        self.iniciativa = 0
        self.efeitos = [] # só recebe objetos da classe Efeito

    def adicionar_barra(self, nome, atual, maximo):
        self.barras.append({"nome": nome, "atual": atual, "maximo": maximo})

    def alterar_barra(self, nome, novo_valor):
        for barra in self.barras:
            if barra["nome"] == nome:
                barra["atual"] = novo_valor
