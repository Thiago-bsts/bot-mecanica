from collections import deque
from typing import Tuple, Optional

# ESTRUTURA DE DADOS: Fila (Queue implementada com 'deque')
# POR QUE: 'deque' (Double-Ended Queue) é otimizado no Python para inserções
# e remoções rápidas O(1) nas extremidades. Usamos para garantir a ordem
# de chegada das mensagens e processá-las em formato FIFO (First In, First Out).
class FilaMensagens:
    def __init__(self):
        self._fila = deque()

    def enfileirar(self, telefone: str, mensagem: str):
        """Adiciona uma nova mensagem ao final da fila (O(1))."""
        self._fila.append((telefone, mensagem))

    def desenfileirar(self) -> Tuple[Optional[str], Optional[str]]:
        """Remove e retorna a mensagem mais antiga (início da fila) (O(1))."""
        if self.esta_vazia():
            return None, None
        return self._fila.popleft()

    def esta_vazia(self) -> bool:
        return len(self._fila) == 0

    def tamanho(self) -> int:
        return len(self._fila)
