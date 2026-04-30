from bot.models.usuario import Usuario

# ESTRUTURA DE DADOS: HashMap (Dicionário / dict)
# POR QUE: Armazenar os usuários ativos num dicionário indexado pelo telefone (chave)
# permite recuperar todo o contexto da conversa em tempo O(1).
class GerenciadorUsuarios:
    def __init__(self):
        self._usuarios = {}

    def obter_ou_criar_usuario(self, telefone: str) -> Usuario:
        if telefone not in self._usuarios:
            self._usuarios[telefone] = Usuario(telefone)
        return self._usuarios[telefone]
        
    def remover_usuario(self, telefone: str):
        if telefone in self._usuarios:
            del self._usuarios[telefone]

    def listar_usuarios_ativos(self):
        return list(self._usuarios.values())
