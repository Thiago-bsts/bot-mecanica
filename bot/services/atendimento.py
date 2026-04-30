from bot.models.usuario import Usuario, EstadoUsuario
from bot.models.pedido import PedidoAtendimento
from bot.models.servico import Servico
from bot.data.base_conhecimento import SERVICOS_PRECOS
from bot.services.diagnostico import DiagnosticoService

class AtendimentoService:
    def __init__(self, gerenciador_filas):
        self.filas = gerenciador_filas
        self.diagnostico_service = DiagnosticoService()

    def iniciar_atendimento(self, usuario: Usuario) -> str:
        usuario.pedido_atual = PedidoAtendimento(usuario)
        usuario.estado = EstadoUsuario.MENU_PRINCIPAL
        return (
            "Olá! Bem-vindo à Oficina Mecânica AutoBot.\n"
            "Como podemos te ajudar hoje?\n"
            "1 - Fazer um Orçamento (Ver Serviços e Preços)\n"
            "2 - Fazer Diagnóstico de Problema\n"
            "3 - Agendar um Serviço\n"
            "4 - Falar com Atendente Humano"
        )

    def processar_menu_principal(self, usuario: Usuario, mensagem: str) -> str:
        escolha = mensagem.strip()
        if escolha == '1':
            usuario.pedido_atual.tipo_atendimento = "ORCAMENTO"
            usuario.estado = EstadoUsuario.ORCAMENTO
            
            menu_orcamento = "Nossa tabela de serviços:\n"
            for k, v in SERVICOS_PRECOS.items():
                menu_orcamento += f"{k} - {v['nome']} (R$ {v['preco']:.2f})\n"
            menu_orcamento += "\nDigite o número do serviço para incluir no orçamento, ou 'F' para finalizar e enviar à equipe."
            return menu_orcamento
            
        elif escolha == '2':
            usuario.pedido_atual.tipo_atendimento = "DIAGNOSTICO"
            return self.diagnostico_service.iniciar_diagnostico(usuario)
            
        elif escolha == '3':
            usuario.pedido_atual.tipo_atendimento = "AGENDAMENTO"
            usuario.estado = EstadoUsuario.AGENDAMENTO
            return "Para agendamento, por favor digite o dia e horário de preferência (Ex: Quinta-feira às 14h)."
            
        elif escolha == '4':
            usuario.pedido_atual.tipo_atendimento = "ATENDENTE"
            usuario.estado = EstadoUsuario.FINALIZADO
            self.encaminhar_para_fila(usuario.pedido_atual)
            return "Entendido. Você foi direcionado para a fila de atendimento humano. Aguarde, por favor."
            
        return "Opção inválida. Digite 1, 2, 3 ou 4."

    def processar_orcamento(self, usuario: Usuario, mensagem: str) -> str:
        escolha = mensagem.strip().upper()
        
        if escolha == 'F':
            total = usuario.pedido_atual.calcular_total()
            usuario.estado = EstadoUsuario.FINALIZADO
            self.encaminhar_para_fila(usuario.pedido_atual)
            return f"Orçamento salvo! Total prévio: R$ {total:.2f}. Encaminhando para um consultor finalizar o orçamento."
            
        if escolha in SERVICOS_PRECOS:
            dados = SERVICOS_PRECOS[escolha]
            servico = Servico(escolha, dados['nome'], dados['preco'])
            usuario.pedido_atual.adicionar_servico(servico)
            return f"[{servico.nome}] adicionado ao orçamento. Digite outro número para adicionar mais ou 'F' para finalizar."
            
        return "Opção não reconhecida. Digite o número do serviço ou 'F' para finalizar."

    def processar_agendamento(self, usuario: Usuario, mensagem: str) -> str:
        usuario.pedido_atual.data_agendamento = mensagem
        usuario.estado = EstadoUsuario.FINALIZADO
        self.encaminhar_para_fila(usuario.pedido_atual)
        return f"Sua preferência ({mensagem}) foi registrada! Encaminhando para confirmação com a equipe."

    def encaminhar_para_fila(self, pedido: PedidoAtendimento):
        """Implementa o SPLIT de atendimento enviando o pedido para a Fila Correta (deque)"""
        if pedido.urgente:
            self.filas.fila_urgente.append(pedido)
            print(f"[SPLIT DE FILAS] Pedido #{pedido.id} ({pedido.usuario.telefone}) direcionado para -> FILA URGENTE")
        elif pedido.tipo_atendimento == "ORCAMENTO":
            self.filas.fila_orcamento.append(pedido)
            print(f"[SPLIT DE FILAS] Pedido #{pedido.id} ({pedido.usuario.telefone}) direcionado para -> FILA DE ORÇAMENTOS")
        elif pedido.tipo_atendimento == "DIAGNOSTICO":
            self.filas.fila_diagnostico.append(pedido)
            print(f"[SPLIT DE FILAS] Pedido #{pedido.id} ({pedido.usuario.telefone}) direcionado para -> FILA DE DIAGNÓSTICOS")
        else:
            self.filas.fila_atendente_geral.append(pedido)
            print(f"[SPLIT DE FILAS] Pedido #{pedido.id} ({pedido.usuario.telefone}) direcionado para -> FILA GERAL")
