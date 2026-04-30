from collections import deque

class GerenciadorFilas:
    def __init__(self):
        # ESTRUTURA DE DADOS: Fila (Queue / deque)
        # POR QUE: 'deque' (Double-Ended Queue) é ideal para processar eventos
        # de chegada em ordem First-In First-Out (FIFO) de forma super eficiente (O(1)).
        
        # Fila global por onde chegam todas as mensagens cruas dos clientes
        self.fila_entrada = deque()
        
        # --- SPLIT DE ATENDIMENTO ---
        # Filas separadas para onde os pedidos de atendimento são encaminhados 
        # depois que o bot entende a intenção do usuário.
        self.fila_orcamento = deque()
        self.fila_diagnostico = deque()
        self.fila_urgente = deque()
        self.fila_atendente_geral = deque()

    def enfileirar_mensagem_entrada(self, telefone: str, mensagem: str):
        """Adiciona mensagem à fila principal."""
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
