from bot.data.base_conhecimento import DIAGNOSTICOS
from bot.models.usuario import Usuario, EstadoUsuario

class DiagnosticoService:
    def iniciar_diagnostico(self, usuario: Usuario) -> str:
        usuario.estado = EstadoUsuario.DIAGNOSTICO
        menu = "Certo, vamos tentar diagnosticar. Qual problema você está notando no veículo?\n"
        for k, v in DIAGNOSTICOS.items():
            menu += f"{k} - {v['problema']}\n"
        menu += "Digite o número correspondente:"
        return menu

    def processar_resposta(self, usuario: Usuario, resposta: str) -> str:
        if resposta in DIAGNOSTICOS:
            dados = DIAGNOSTICOS[resposta]
            
            # Atualiza o pedido com os dados do diagnóstico
            usuario.pedido_atual.problema_relatado = dados['problema']
            
            # CLASSIFICADOR DE PRIORIDADE (Função requerida pelo fluxo)
            if dados.get('urgente', False):
                usuario.pedido_atual.urgente = True
                
            causas_str = ", ".join(dados['causas'])
            servicos_str = ", ".join(dados['servicos_sugeridos'])
            
            # Prepara a mensagem baseada no dicionário de conhecimento
            resposta_bot = (
                f"Entendido. O problema '{dados['problema']}' geralmente pode ser causado por: {causas_str}.\n"
                f"Sugerimos os seguintes serviços: {servicos_str}.\n"
                "Seu atendimento foi encaminhado para nossa equipe técnica e um mecânico especializado avaliará em breve."
            )
            
            # Finaliza o fluxo automatizado
            usuario.estado = EstadoUsuario.FINALIZADO
            return resposta_bot
        else:
            return "Opção inválida. Digite o número correspondente ao problema da lista."
