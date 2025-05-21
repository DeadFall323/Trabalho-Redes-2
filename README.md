# Projeto: SImulação de Rede com Roteadores e Hosts usando Docker

# 1 - Pré-requisitos:
    Docker e Docker COmpose instalados na maquina
# 2 - Como fazer os testes
    - Clone este repositorio:
    git clone  https://github.com/DeadFall323/Trabalho-Redes-2.git
    
    Suba a rede e os containers com o Docker Compose:
    docker compose up -d

    Verifique se os containers estão rodando:
    docker ps

    Caso precise conectar manualmente hosts à rede:
    docker network connect trabalho-redes-2_rede host1
    docker network connect trabalho-redes-2_rede host2
    docker network connect trabalho-redes-2_rede host3
    docker network connect trabalho-redes-2_rede host4
    docker network connect trabalho-redes-2_rede host5

    Acesse os containers para executar comandos ou testes:
    docker exec -it router1 bash
    docker exec -it host1 bash

# 3 - Justificativa dos protocolos escolhidos:
Neste projeto, optamos por implementar o protocolo de roteamento por estado de enlace (Link-State Routing), especificamente o algoritmo de Dijkstra, pelos seguintes motivos:

* Eficiência: O algoritmo de Dijkstra calcula o caminho mais curto para todos os destinos, garantindo rotas otimizadas na topologia.
* Escalabilidade: Diferente de protocolos de vetor de distância, o protocolo de estado de enlace oferece convergência rápida e evita loops.

* Precisão na simulação: Permite a simulação detalhada do comportamento de roteadores que mantêm uma visão completa da topologia da rede, ideal para o entendimento acadêmico do funcionamento de redes IP.

* Controle e monitoramento: O protocolo facilita a visualização e controle da tabela de roteamento em cada roteador da rede simulada.

# 4 - Como a topologia foi construida:
A topologia da rede foi construída usando containers Docker para simular os dispositivos de rede:

* Roteadores: Containers nomeados router1, router2, router3, router4, router5.
* Hosts: Containers nomeados host1, host2, host3, host4, host5.
* Todos os containers estão conectados a uma rede Docker bridge chamada trabalho-redes-2_rede, configurada com a subnet 192.168.250.0/24.

* A comunicação entre roteadores e hosts ocorre por essa rede comum.
* O roteamento é feito internamente nos containers de roteador, usando scripts Python que implementam o algoritmo de Dijkstra para cálculo das rotas e atualização das tabelas de roteamento.
* Cada roteador possui uma interface virtual dentro da rede, com IPs fixos para facilitar o roteamento e a identificação.
* A topologia física e lógica foi modelada para representar um ambiente realista e didático, facilitando o aprendizado dos conceitos de roteamento e protocolos de rede.

# 5 - Diagrama de Classe

[]

* Router: Classe que representa o roteador, com métodos para receber, enviar pacotes e atualizar a tabela de roteamento usando o protocolo.

* Host: Representa um host final da rede, capaz de enviar e receber pacotes.

* Network: Representa a rede Docker virtual, responsável pela conexão e comunicação entre containers.



