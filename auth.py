"""
Sistema de autenticação simples para o RPG
"""

# Usuários hardcoded (login: senha)
USUARIOS = {
    "mestre": "sessão",
    "jogadores": "123"
}

class Auth:
    @staticmethod
    def validar_login(usuario, senha):
        """Valida se o login e senha estão corretos"""
        return USUARIOS.get(usuario) == senha
    
    @staticmethod
    def get_usuarios():
        """Retorna lista de usuários disponíveis"""
        return list(USUARIOS.keys())
    
    @staticmethod
    def adicionar_usuario(usuario, senha):
        """Adiciona um novo usuário (para expansão futura)"""
        USUARIOS[usuario] = senha