import socket
import json
import time
import threading
import os
from utils.algoritmo_de_roteamento import processa_lsa, atualiza_lsdb
from utils.algoritmo_de_roteamento import calcula_tabela_roteamento

ROUTER_ID = os.environ.get("ROUTER_ID")
PORT = int(os.environ.get("PORT", 5000))
LSDB = {}

def load_neighbors():
    with open(f"config/{ROUTER_ID}/vizinhos.json") as f:
        return json.load(f)

def send_lsa(neighbor_ip, lsa_data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = json.dumps(lsa_data).encode()
        sock.sendto(message, (neighbor_ip, PORT))
        print(f"[{ROUTER_ID}] Enviou LSA para {neighbor_ip}")
    except Exception as e:
        print(f"[{ROUTER_ID}] Erro ao enviar LSA para {neighbor_ip}: {e}")

#def receive_loop():
#    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 #   sock.bind(("", PORT))
  #  while True:
   #     data, addr = sock.recvfrom(4096)
    #    lsa = json.loads(data.decode())
     #   print(f"[{ROUTER_ID}] Recebeu LSA de {lsa['origin']}")
#
 #       updated = processa_lsa(LSDB, lsa)
  #      if updated:
   #         atualiza_lsdb(ROUTER_ID, LSDB)
#
 #           # Calcula e imprime a tabela de roteamento
  #          tabela = calcula_tabela_roteamento(ROUTER_ID, LSDB)
   #         print(f"[{ROUTER_ID}] Tabela de roteamento:")
    #        for destino, proximo_salto in tabela.items():
     #           print(f" - {destino} → {proximo_salto}")
def receive_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    while True:
        data, addr = sock.recvfrom(4096)
        try:
            lsa = json.loads(data.decode())
        except json.JSONDecodeError:
            mensagem = data.decode(errors="ignore")
            print(f"[{ROUTER_ID}] Recebeu mensagem de host de {addr}: {mensagem}")

            # Envia ACK de volta
            try:
                ack = f"ACK: {ROUTER_ID} recebeu sua mensagem"
                sock.sendto(ack.encode(), addr)
                print(f"[{ROUTER_ID}] Enviou ACK para {addr}")
            except Exception as e:
                print(f"[{ROUTER_ID}] Falha ao enviar ACK: {e}")
            continue

        print(f"[{ROUTER_ID}] Recebeu LSA de {lsa['origin']}")
        updated = processa_lsa(LSDB, lsa)
        if updated:
            atualiza_lsdb(ROUTER_ID, LSDB)

            tabela = calcula_tabela_roteamento(ROUTER_ID, LSDB)
            print(f"[{ROUTER_ID}] Tabela de roteamento:")
            for destino, proximo_salto in tabela.items():
                print(f" - {destino} → {proximo_salto}")



def start_router():
    neighbors = load_neighbors()
    threading.Thread(target=receive_loop, daemon=True).start()

    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        lsa = {
            "origin": ROUTER_ID,
            "timestamp": timestamp,
            "neighbors": neighbors
        }
        for ip in neighbors.values():
            send_lsa(ip, lsa)
        time.sleep(10)

if __name__ == "__main__":
    print(f"[{ROUTER_ID}] Roteador iniciado")
    start_router()
