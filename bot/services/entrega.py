from collections import deque
import heapq
from bot.models.pedido import Pedido, TipoEntrega

class EntregaService:
    def __init__(self):
        # ESTRUTURA DE DADOS: Fila (deque)
        # POR QUE: Fila simples FIFO para pedidos que serão retirados no balcão.
        # Os clientes retiram os pedidos na ordem em que eles ficam prontos.
        self.fila_retirada = deque()
        
        # ESTRUTURA DE DADOS: HashMap de Filas (dict de deque)
        # POR QUE: Permite separar as entregas por região (Split de Entrega).
        # O acesso à fila de uma região específica é O(1) usando a string da região.
        self.filas_por_regiao = {
            "NORTE": deque(),
            "SUL": deque(),
            "LESTE": deque(),
            "OESTE": deque(),
            "CENTRO": deque()
        }
        
        # ESTRUTURA DE DADOS (OPCIONAL/DIFERENCIAL): Fila de Prioridade (Heap)
        # POR QUE: Usado para "pedidos urgentes" ou grandes pedidos. O Heap (heapq)
        # mantém sempre no topo o elemento de menor valor (maior prioridade) com inserção O(log n).
        self.fila_prioridade = []

    def identificar_regiao(self, endereco: str) -> str:
        """Identifica de forma simulada a região baseada em palavras-chave no endereço."""
        end_upper = endereco.upper()
        if "CENTRO" in end_upper: return "CENTRO"
        if "SUL" in end_upper: return "SUL"
        if "NORTE" in end_upper: return "NORTE"
        if "LESTE" in end_upper: return "LESTE"
        return "OESTE" # Região fallback

    def encaminhar_pedido(self, pedido: Pedido, usuario):
        if pedido.tipo_entrega == TipoEntrega.RETIRADA:
            self.fila_retirada.append(pedido)
            print(f"[SPLIT] Pedido #{pedido.id} ({usuario.telefone}) -> FILA RETIRADA.")
        
        elif pedido.tipo_entrega == TipoEntrega.DELIVERY:
            regiao = self.identificar_regiao(pedido.endereco)
            pedido.regiao = regiao
            
            # Condição simples para simular um pedido prioritário (> R$ 25)
            if pedido.calcular_total() > 25.00:
                # Armazena tupla (prioridade, id, pedido). Prioridade 1 é mais alta.
                heapq.heappush(self.fila_prioridade, (1, pedido.id, pedido))
                print(f"[SPLIT] Pedido #{pedido.id} ({usuario.telefone}) -> HEAP DE PRIORIDADE (Valor alto).")
            else:
                self.filas_por_regiao[regiao].append(pedido)
                print(f"[SPLIT] Pedido #{pedido.id} ({usuario.telefone}) -> FILA DELIVERY ({regiao}).")

    def relatorio_filas(self):
        print("\n=== STATUS DAS FILAS DE ENTREGA ===")
        print(f"Retirada (Balcão): {len(self.fila_retirada)} pedidos")
        print("Delivery Tradicional:")
        for reg, fila in self.filas_por_regiao.items():
            print(f"   - {reg}: {len(fila)} pedidos")
        print(f"Delivery Prioritário: {len(self.fila_prioridade)} pedidos")
        print("===================================\n")
