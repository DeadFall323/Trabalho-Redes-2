# Instruções para rodar a simulação
# Simulação de Rede com Roteamento por Estado de Enlace (Link State)

### Passos:

# Como Executar o Projeto
cd "nome_do_diretorio"
# Construa os containers:
docker-compose build
# Inicie a simulação:
docker-compose up

### repositório:

   ```bash
   git clone https://github.com/lolanl/C-digo-fonte-_Redes_II.git

   # Os containers iniciarão e os roteadores começarão a trocar pacotes de estado de enlace. Pings entre hosts serão exibidos no terminal (com sucesso ou falha).
   
# Justificativa do Protocolo Escolhido:

#1- Utilizou-se o UDP para a comunicação entre roteadores pelos seguintes motivos:

#2- Baixa sobrecarga: UDP é mais leve, ideal para troca rápida e contínua de pacotes de estado de enlace.

#3- Simulação de perda: É possível simular falhas ou pacotes perdidos sem complexidade adicional. Não exige conexão persistente, tornando a simulação mais flexível.

# Como a Topologia foi Construída:
# A rede é composta por múltiplas subredes, cada uma com:

#1 - Hosts (hostA e hostB)

#2 - 1 Roteador

#Os roteadores são interconectados de forma aleatória, garantindo que a topologia seja parcialmente conectada. Cada roteador descobre seus vizinhos dinamicamente e compartilha informações via pacotes LS (Link State).

#A topologia completa é usada para construir a LSDB (Link State Database) e calcular as rotas com Dijkstra.