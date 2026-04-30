from bot.models.usuario import EstadoUsuario
from bot.services.atendimento import AtendimentoService

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
        estado = usuario.estado
        
        if estado == EstadoUsuario.INICIO:
            return self.atendimento.iniciar_atendimento(usuario)
            
        elif estado == EstadoUsuario.MENU_PRINCIPAL:
            return self.atendimento.processar_menu_principal(usuario, mensagem)
            
        elif estado == EstadoUsuario.ORCAMENTO:
            return self.atendimento.processar_orcamento(usuario, mensagem)
            
        elif estado == EstadoUsuario.DIAGNOSTICO:
            resposta = self.atendimento.diagnostico_service.processar_resposta(usuario, mensagem)
            if usuario.estado == EstadoUsuario.FINALIZADO:
                self.atendimento.encaminhar_para_fila(usuario.pedido_atual)
            return resposta
            
        elif estado == EstadoUsuario.AGENDAMENTO:
            return self.atendimento.processar_agendamento(usuario, mensagem)
            
        elif estado == EstadoUsuario.FINALIZADO:
            return "Seu atendimento já foi encaminhado para a fila correspondente. Por favor, aguarde o contato do mecânico."
            
        return "Desculpe, não entendi o comando. Digite uma opção válida."
