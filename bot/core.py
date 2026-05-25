from collections import deque
from bot.models import Usuario

# --- filas.py ---
class GerenciadorFilas:
    def __init__(self):
        self.fila_entrada = deque()
        self.fila_orcamento = deque()
        self.fila_diagnostico = deque()
        self.fila_urgente = deque()
        self.fila_atendente_geral = deque()

    def enfileirar_mensagem_entrada(self, telefone: str, mensagem: str):
        self.fila_entrada.append((telefone, mensagem))

    def desenfileirar_mensagem_entrada(self):
        if not self.fila_entrada:
            return None, None
        return self.fila_entrada.popleft()
        
    def relatorio_filas(self):
        print("\n=== STATUS DAS FILAS DE ATENDIMENTO INTERNO ===")
        print(f"Emergência / Urgência: {len(self.fila_urgente)} veículos")
        print(f"Diagnóstico Técnico: {len(self.fila_diagnostico)} veículos")
        print(f"Orçamento Rápido: {len(self.fila_orcamento)} veículos")
        print(f"Atendimento Geral: {len(self.fila_atendente_geral)} veículos")
        print("===============================================\n")


# --- gerenciador_usuarios.py ---
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
