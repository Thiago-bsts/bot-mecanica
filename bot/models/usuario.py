from enum import Enum, auto

# ESTRUTURA DE DADOS: Enum (Enumeration)
# POR QUE: Usado para mapear de forma clara, legível e segura os estados da
# máquina de estados do nosso fluxo conversacional. Previne erros de digitação.
class EstadoUsuario(Enum):
    INICIO = auto()
    MENU_PRINCIPAL = auto()
    ORCAMENTO = auto()
    DIAGNOSTICO = auto()
    AGENDAMENTO = auto()
    FINALIZADO = auto()

class Usuario:
    def __init__(self, telefone: str):
        self.telefone = telefone
        self.estado = EstadoUsuario.INICIO
        
        # ESTRUTURA DE DADOS: Lista (Atuando como simulador de Linked Behavior)
        # POR QUE: O histórico de mensagens é essencialmente uma lista encadeada temporal,
        # onde as mensagens são "apendadas" em ordem. A Lista em Python (que é um array dinâmico)
        # serve bem para essa simulação porque tem tempo O(1) amortizado para inserção no fim.
        self.historico_mensagens = []
        
        self.pedido_atual = None

    def adicionar_mensagem(self, remetente: str, texto: str):
        self.historico_mensagens.append(f"[{remetente}]: {texto}")
