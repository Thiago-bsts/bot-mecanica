from enum import Enum, auto

# --- servico.py ---
class Servico:
    def __init__(self, id_servico: str, nome: str, preco: float):
        self.id = id_servico
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f"{self.nome} (R$ {self.preco:.2f})"

# --- produto.py ---
class Produto:
    def __init__(self, id_produto: int, nome: str, preco: float):
        self.id = id_produto
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f"{self.nome} (R$ {self.preco:.2f})"

# --- usuario.py ---
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
        self.historico_mensagens = []
        self.pedido_atual = None

    def adicionar_mensagem(self, remetente: str, texto: str):
        self.historico_mensagens.append(f"[{remetente}]: {texto}")

# --- pedido.py ---
class PedidoAtendimento:
    _id_counter = 1

    def __init__(self, usuario):
        self.id = PedidoAtendimento._id_counter
        PedidoAtendimento._id_counter += 1
        
        self.usuario = usuario
        self.servicos = []
        self.problema_relatado = None
        self.tipo_atendimento = None # Pode ser ORCAMENTO, DIAGNOSTICO, AGENDAMENTO, ATENDENTE
        self.urgente = False
        self.data_agendamento = None

    def adicionar_servico(self, servico: Servico):
        self.servicos.append(servico)

    def calcular_total(self) -> float:
        return sum(s.preco for s in self.servicos)
