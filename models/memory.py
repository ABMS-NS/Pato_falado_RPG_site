"""
Sistema de memória global compartilhada - todos os usuários veem as mesmas informações
Agora com suporte a personagens privados por usuário
"""

# Variáveis globais compartilhadas
_shared_data = {
    'personagens': [],  # Todos os personagens (públicos + privados)
    'lista_iniciativa': [],
    'rodada_atual': 0
}

class Memory:
    @property
    def personagens(self):
        return _shared_data['personagens']
    
    @personagens.setter
    def personagens(self, value):
        _shared_data['personagens'] = value
    
    @property
    def lista_iniciativa(self):
        return _shared_data['lista_iniciativa']
    
    @lista_iniciativa.setter
    def lista_iniciativa(self, value):
        _shared_data['lista_iniciativa'] = value
    
    @property
    def rodada_atual(self):
        return _shared_data['rodada_atual']
    
    @rodada_atual.setter
    def rodada_atual(self, value):
        _shared_data['rodada_atual'] = value

    def get_personagens_do_usuario(self, usuario):
        """Retorna apenas os personagens que o usuário pode ver (seus próprios)"""
        return [p for p in self.personagens if p.dono == usuario]
    
    def get_todos_personagens(self):
        """Retorna todos os personagens (para iniciativa)"""
        return self.personagens

    def organizar_init(self):
        # Primeiro: pega todos os personagens da memória (públicos e privados)
        todos_personagens = self.get_todos_personagens()
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

# Funções apenas para dados compartilhados dos personagens
# Navegação e estados individuais ficam no session_state de cada usuário