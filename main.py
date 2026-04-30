import sys
from bot.core.filas import GerenciadorFilas
from bot.core.gerenciador_usuarios import GerenciadorUsuarios
from bot.services.processador import ProcessadorMensagens

def modo_interativo():
    print("=== INICIANDO SISTEMA AUTOBOT OFICINA MECÂNICA ===")
    print("Modo Interativo Ativado! Converse com o bot como se fosse pelo WhatsApp.")
    print("Digite 'sair' a qualquer momento para desligar o sistema e ver o relatório final.\n")
    print("Dica: Dê um 'Oi' para começar o atendimento!\n")
    
    # 1. Inicializando as Estruturas de Dados
    gerenciador_filas = GerenciadorFilas()
    gerenciador_usuarios = GerenciadorUsuarios()
    processador = ProcessadorMensagens(gerenciador_usuarios, gerenciador_filas)
    
    # Simularemos que o seu terminal é um celular com este número
    telefone_usuario = "11988887777" 
    
    # 2. Loop Infinito (Simulando o servidor sempre escutando novas mensagens)
    while True:
        try:
            # Pega a mensagem digitada no terminal
            mensagem_cliente = input("\nVocê: ")
            
            if mensagem_cliente.strip().lower() == 'sair':
                print("\nEncerrando a simulação interativa...")
                break
                
            if not mensagem_cliente.strip():
                continue
                
            # Enfileira a mensagem que chegou (Fila FIFO)
            gerenciador_filas.enfileirar_mensagem_entrada(telefone_usuario, mensagem_cliente)
            
            # O processador retira da fila e processa o texto imediatamente
            telefone, mensagem_na_fila = gerenciador_filas.desenfileirar_mensagem_entrada()
            processador.processar(telefone, mensagem_na_fila)
            
        except KeyboardInterrupt:
            # Caso o usuário aperte Ctrl+C
            print("\nEncerrando forçadamente...")
            break
            
    # 3. Finalização: Mostra os bastidores das estruturas de dados
    gerenciador_filas.relatorio_filas()
    
    print("\n=== HISTÓRICO COMPLETO DA SESSÃO (Linked Behavior) ===")
    user = gerenciador_usuarios.obter_ou_criar_usuario(telefone_usuario)
    for msg in user.historico_mensagens:
        print(msg)
    print("======================================================")

if __name__ == "__main__":
    modo_interativo()
