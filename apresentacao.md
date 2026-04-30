# AutoBot Oficina Mecânica - Apresentação do Projeto

## 🎯 Objetivo
Este projeto consiste em um **Bot de Atendimento Autônomo para Oficina Mecânica**, desenvolvido em Python. O grande diferencial deste sistema não é apenas sua interface interativa, mas sim a sua **arquitetura fundamentada em Estruturas de Dados Clássicas**, ideal para fins acadêmicos e educacionais.

O bot é capaz de guiar o usuário em processos de orçamento, triagem de diagnósticos e agendamentos, encaminhando internamente cada atendimento para a fila correta (Split de Filas) baseando-se no contexto da conversa e urgência.

---

## 🏗️ Arquitetura do Sistema (Separação de Preocupações)
O sistema foi construído em camadas para garantir organização e baixo acoplamento:

* **`models/`**: Onde definimos as "entidades" puras (Usuário, Serviços e o Pedido/Ordem de Serviço). 
* **`data/`**: Funciona como um "banco de dados em memória" (Base de conhecimento estática em dicionários).
* **`core/`**: Onde residem os motores do sistema (As Estruturas de Dados complexas: Filas e HashMaps de sessão).
* **`services/`**: A inteligência (Regras de Negócio). Aqui o texto digitado vira comandos lógicos com base no contexto.
* **`main.py`**: A porta de entrada que integra as camadas e cria a interface interativa (o terminal simulando o WhatsApp).

---

## 🧠 Estruturas de Dados Utilizadas

Para resolver os problemas reais de roteamento e gestão de estado em alta performance, aplicamos as seguintes estruturas em nosso código (você pode encontrá-las facilmente usando a busca por "ESTRUTURA DE DADOS" nos comentários do código):

### 1. Fila (Queue / `collections.deque`)
* **Onde foi usada:** `bot/core/filas.py`
* **Como e Por quê:** Usamos a estrutura Double-Ended Queue (`deque`) nativa do Python, que garante inserções (`append`) e remoções (`popleft`) no tempo constante **O(1)**.
    * **Fila de Entrada (FIFO):** Cada mensagem enviada pelo usuário cai no fim desta fila. O bot consome sempre a mais antiga (início da fila) primeiro, garantindo que nada se perca em um pico de uso simultâneo.
    * **Split de Filas de Atendimento:** Após o bot concluir a conversa, ele não "solta" o pedido ao acaso. Ele usa Múltiplas Filas separadas (Orçamento, Diagnóstico, Urgente) para encaminhar o serviço à equipe técnica correta nos bastidores.

### 2. HashMap / Tabela de Espalhamento (Dicionário / `dict`)
* **Onde foi usada:** `bot/core/gerenciador_usuarios.py` e `bot/data/base_conhecimento.py`.
* **Como e Por quê:** O dicionário resolve a complexidade de busca através de *hashing*, retornando dados em tempo **O(1)** na média.
    * **Gerenciador de Usuários:** Mapeia `Telefone -> Objeto Usuario`. Num bot real, milhões de pessoas mandam mensagens juntas. Não podemos percorrer uma lista linear O(N) para saber de quem é aquela mensagem. O HashMap acha a sessão ativa de forma instantânea através do ID do celular.
    * **Base de Conhecimento:** Usado para buscar de forma super otimizada os detalhes de um Diagnóstico ou Serviço a partir da opção (1, 2, 3...) digitada pelo cliente.

### 3. Enum (Enumeração)
* **Onde foi usada:** `bot/models/usuario.py` (`EstadoUsuario`).
* **Como e Por quê:** Impede "strings mágicas" e erros de digitação. O Enum é uma estrutura restrita que formaliza a **Máquina de Estados** do bot. Se o usuário está em `ESCOLHENDO_SERVICO`, o bot sabe exatamente qual regra de negócio isolada aplicar a ele, nunca se confundindo com o menu principal.

### 4. Arrays Dinâmicos / Listas (`list`) - *Linked Behavior*
* **Onde foi usada:** `bot/models/usuario.py` (Histórico) e `bot/models/pedido.py` (Itens).
* **Como e Por quê:** Listas no Python são arrays dinâmicos super otimizados.
    * **Histórico de Mensagens:** Elas atuam de forma semelhante a uma estrutura *Linked*, onde novos nós de texto vão sendo apensados sequencialmente ao longo do tempo (inserção amortizada O(1) no final), formando o diário completo do usuário que o professor poderá comprovar no final da execução.

---

## 🔄 Fluxo de Estruturas de Dados (Passo a Passo)

Use a lógica abaixo para criar ou explicar seu diagrama/slides:

1. **[Terminal]** -> Cliente digita uma mensagem.
2. **[Fila/Deque]** -> A mensagem vai para o final da **Fila de Entrada**.
3. **[Fila/Deque]** -> O Maestro (`Processador`) retira a primeira mensagem do topo (FIFO).
4. **[HashMap/Dict]** -> O Maestro consulta o **Dicionário de Usuários O(1)** pelo telefone para carregar o contexto da conversa e salva o texto na **[Lista]** de Histórico.
5. **[Enum]** -> O Maestro olha a **Máquina de Estados** do usuário e roteia para o Serviço correto (Orçamento, Diagnóstico, etc).
6. Se o usuário pedir Serviço, busca no **[HashMap]** da Tabela de Preços.
7. Se for finalizado, passa pela Regra de Triagem e entra em uma das **[Filas Setoriais]** (Split: Diagnóstico, Urgente ou Orçamento).

---

## 🚀 Como Explicar o "Split" na Apresentação (Ponto de Ouro)

O Ponto alto da apresentação é o conceito de **Split de Atendimento**. 
Mostre à sua banca/professor que o bot não é apenas um "respondedor de mensagens vazio". Ele atua como um roteador logístico inteligente:

1. O cliente chega informando na opção de diagnóstico que a luz do óleo acendeu ou que o *"Carro não liga"*.
2. O bot detecta essa anomalia grave através da base de conhecimento (HashMap).
3. O bot avisa o cliente.
4. Internamente, o sistema altera a flag de Urgência (`urgente = True`).
5. No momento de fechar a sessão, **em vez de enviar o pedido para a `Fila Geral` de consertos**, ele encaminha esse nó de dados diretamente para a `Fila de Urgência` (um deque completamente separado).

**Resumo para a banca:** Isso comprova a aplicação direta e elegante de estruturas de dados clássicas (Filas FIFO e Maps) resolvendo triagem e gargalos logísticos do mundo real de uma mecânica!
