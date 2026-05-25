from bot.models import Usuario, EstadoUsuario, PedidoAtendimento, Servico
from bot.database import SERVICOS_PRECOS, DIAGNOSTICOS

class DiagnosticoService:
    def iniciar_diagnostico(self, usuario: Usuario) -> str:
        usuario.estado = EstadoUsuario.DIAGNOSTICO
        menu = "Certo, vamos tentar diagnosticar. Qual problema você está notando no veículo?\n"
        for k, v in DIAGNOSTICOS.items():
            menu += f"{k} - {v['problema']}\n"
        menu += "0 - Voltar ao Menu Principal\n"
        menu += "Digite o número correspondente:"
        return menu

    def processar_resposta(self, usuario: Usuario, resposta: str) -> str:
        if resposta in DIAGNOSTICOS:
            dados = DIAGNOSTICOS[resposta]
            usuario.pedido_atual.problema_relatado = dados['problema']
            
            if dados.get('urgente', False):
                usuario.pedido_atual.urgente = True
                
            causas_str = ", ".join(dados['causas'])
            servicos_str = ", ".join(dados['servicos_sugeridos'])
            
            resposta_bot = (
                f"Entendido. O problema '{dados['problema']}' geralmente pode ser causado por: {causas_str}.\n"
                f"Sugerimos os seguintes serviços: {servicos_str}.\n"
                "Seu atendimento foi encaminhado para nossa equipe técnica e um mecânico especializado avaliará em breve."
            )
            usuario.estado = EstadoUsuario.FINALIZADO
            return resposta_bot
        else:
            return "Opção inválida. Digite o número correspondente ao problema da lista."

class AtendimentoService:
    def __init__(self, gerenciador_filas):
        self.filas = gerenciador_filas
        self.diagnostico_service = DiagnosticoService()

    def obter_opcoes_menu(self) -> str:
        return (
            "1 - Fazer um Orçamento (Ver Serviços e Preços)\n"
            "2 - Fazer Diagnóstico de Problema\n"
            "3 - Agendar um Serviço\n"
            "4 - Falar com Atendente Humano"
        )

    def iniciar_atendimento(self, usuario: Usuario) -> str:
        usuario.pedido_atual = PedidoAtendimento(usuario)
        usuario.estado = EstadoUsuario.MENU_PRINCIPAL
        return (
            "Olá! Bem-vindo à Oficina Mecânica AutoBot.\n"
            "Como podemos te ajudar hoje?\n"
            f"{self.obter_opcoes_menu()}"
        )

    def retornar_menu_principal(self, usuario: Usuario) -> str:
        usuario.pedido_atual = PedidoAtendimento(usuario)
        usuario.estado = EstadoUsuario.MENU_PRINCIPAL
        return (
            "Posso ajudar em algo mais? Escolha uma das opções abaixo:\n"
            f"{self.obter_opcoes_menu()}"
        )

    def processar_menu_principal(self, usuario: Usuario, mensagem: str) -> str:
        escolha = mensagem.strip()
        if escolha == '1':
            usuario.pedido_atual.tipo_atendimento = "ORCAMENTO"
            usuario.estado = EstadoUsuario.ORCAMENTO
            
            menu_orcamento = "Nossa tabela de serviços:\n"
            for k, v in SERVICOS_PRECOS.items():
                menu_orcamento += f"{k} - {v['nome']} (R$ {v['preco']:.2f})\n"
            menu_orcamento += "0 - Voltar ao Menu Principal\n"
            menu_orcamento += "\nDigite o número do serviço para incluir no orçamento, ou 'F' para finalizar e enviar à equipe."
            return menu_orcamento
            
        elif escolha == '2':
            usuario.pedido_atual.tipo_atendimento = "DIAGNOSTICO"
            return self.diagnostico_service.iniciar_diagnostico(usuario)
            
        elif escolha == '3':
            usuario.pedido_atual.tipo_atendimento = "AGENDAMENTO"
            usuario.estado = EstadoUsuario.AGENDAMENTO
            return "Para agendamento, por favor digite o dia e horário de preferência (Ex: Quinta-feira às 14h).\nOu digite '0' para voltar ao menu principal."
            
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

class ProcessadorMensagens:
    def __init__(self, gerenciador_usuarios, gerenciador_filas):
        self.gerenciador_usuarios = gerenciador_usuarios
        self.gerenciador_filas = gerenciador_filas
        self.atendimento = AtendimentoService(gerenciador_filas)

    def processar(self, telefone: str, mensagem: str):
        # 1. Recupera contexto do usuário O(1) pelo HashMap
        usuario = self.gerenciador_usuarios.obter_ou_criar_usuario(telefone)
        
        # 2. Armazena histórico (Lista simulando encadeamento)
        usuario.adicionar_mensagem("Você", mensagem)
        
        # 3. Roteia de acordo com a máquina de estados
        resposta = self._rotear_estado(usuario, mensagem)
        
        # 4. Salva resposta do bot e exibe
        usuario.adicionar_mensagem("AutoBot", resposta)
        print(f"[AutoBot]:\n{resposta}")

    def _rotear_estado(self, usuario, mensagem: str) -> str:
        # Funcionalidade global para voltar ao menu principal
        if mensagem.strip().lower() in ['voltar', 'menu', 'inicio', 'cancelar', '0']:
            usuario.estado = EstadoUsuario.INICIO
            usuario.pedido_atual = None
            return self.atendimento.iniciar_atendimento(usuario)

        estado = usuario.estado
        resposta = ""
        
        if estado == EstadoUsuario.INICIO:
            resposta = self.atendimento.iniciar_atendimento(usuario)
            
        elif estado == EstadoUsuario.MENU_PRINCIPAL:
            resposta = self.atendimento.processar_menu_principal(usuario, mensagem)
            
        elif estado == EstadoUsuario.ORCAMENTO:
            resposta = self.atendimento.processar_orcamento(usuario, mensagem)
            
        elif estado == EstadoUsuario.DIAGNOSTICO:
            resposta = self.atendimento.diagnostico_service.processar_resposta(usuario, mensagem)
            if usuario.estado == EstadoUsuario.FINALIZADO:
                self.atendimento.encaminhar_para_fila(usuario.pedido_atual)
            
        elif estado == EstadoUsuario.AGENDAMENTO:
            resposta = self.atendimento.processar_agendamento(usuario, mensagem)
            
        elif estado == EstadoUsuario.FINALIZADO:
            return "Seu atendimento já foi encaminhado para a fila correspondente. Por favor, aguarde o contato do mecânico.\n(Digite 'voltar' ou 'menu' a qualquer momento para retornar às opções principais)"
            
        else:
            resposta = "Desculpe, não entendi o comando. Digite uma opção válida."
            
        if usuario.estado == EstadoUsuario.FINALIZADO:
            menu = self.atendimento.retornar_menu_principal(usuario)
            resposta = f"{resposta}\n\n---\n{menu}"
            
        return resposta
