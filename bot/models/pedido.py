from bot.models.servico import Servico

class PedidoAtendimento:
    _id_counter = 1

    def __init__(self, usuario):
        self.id = PedidoAtendimento._id_counter
        PedidoAtendimento._id_counter += 1
        
        self.usuario = usuario
        
        # ESTRUTURA DE DADOS: Lista (List)
        # POR QUE: Usada para armazenar uma coleção de itens (serviços) onde a ordem
        # de adição pode ser relevante e itens podem ser adicionados dinamicamente
        # conforme o usuário navega no menu.
        self.servicos = []
        
        self.problema_relatado = None
        self.tipo_atendimento = None # Pode ser ORCAMENTO, DIAGNOSTICO, AGENDAMENTO, ATENDENTE
        self.urgente = False
        self.data_agendamento = None

    def adicionar_servico(self, servico: Servico):
        self.servicos.append(servico)

    def calcular_total(self) -> float:
        return sum(s.preco for s in self.servicos)
