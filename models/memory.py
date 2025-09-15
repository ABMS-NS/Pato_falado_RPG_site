"""

Aqui é basicamente uma memória simples para armazenar o personagem na sessão sem precisar utilizar banco de dados (na execução do personagem)

"""

class Memory:
    def __init__(self):
        self.personagens = [] #na main, precisamos declarar isso como variável global para poder acessar e modificar os players e fazer o escudo do mestre
        self.lista_iniciativa = []
        self.rodada_atual = 0

    def organizar_init(self):
        # Primeiro: pega todos os personagens da memória
        todos_personagens = self.personagens
        # Segundo: filtra quem tem iniciativa > 0
        personagens_com_iniciativa = [p for p in todos_personagens if p.iniciativa > 0]
        # Terceiro: ordena do maior para o menor
        self.lista_iniciativa = sorted(personagens_com_iniciativa, key=lambda p: p.iniciativa, reverse=True)

    def passar_turno(self):
        for personagem in self.lista_iniciativa:
            for efeito in personagem.efeitos:
                efeito.reduzir_duracao()
            # Remove efeitos com duração 0
            personagem.efeitos = [e for e in personagem.efeitos if e.duracao > 0]