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

def load_json(filename):
    with open(filename) as f:
        return json.load(f)

def load_neighbors():
    return load_json(f"config/{ROUTER_ID}/vizinhos.json")

def load_hosts():
    return load_json(f"config/{ROUTER_ID}/hosts.json")

def send_lsa(neighbor_ip, lsa_data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = json.dumps(lsa_data).encode()
        sock.sendto(message, (neighbor_ip, PORT))
        print(f"[{ROUTER_ID}] Enviou LSA para {neighbor_ip}")
    except Exception as e:
        print(f"[{ROUTER_ID}] Erro ao enviar LSA para {neighbor_ip}: {e}")

def receive_loop():
    def receive_loop():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", PORT))
        neighbors = load_neighbors()
        hosts = load_hosts()
        hosts_ips = set(hosts.values())  # conjunto dos IPs dos hosts

        while True:
            data, addr = sock.recvfrom(4096)
            ip_origem = addr[0]
            print(f"[{ROUTER_ID}] Mensagem recebida de {ip_origem}")

            try:
                lsa = json.loads(data.decode())
                # Mensagem é um LSA vindo de roteador
                print(f"[{ROUTER_ID}] Recebeu LSA de {lsa['origin']}")
                updated = processa_lsa(LSDB, lsa)
                if updated:
                    atualiza_lsdb(ROUTER_ID, LSDB)
                    tabela = calcula_tabela_roteamento(ROUTER_ID, LSDB)
                    print(f"[{ROUTER_ID}] Tabela de roteamento:")
                    for destino, proximo_salto in tabela.items():
                        print(f" - {destino} → {proximo_salto}")

            except json.JSONDecodeError:
                # Se não for JSON, trata como mensagem de host
                if ip_origem in hosts_ips:
                    mensagem = data.decode(errors="ignore")
                    print(f"[{ROUTER_ID}] Recebeu mensagem de host {ip_origem}: {mensagem}")

                    # Envia ACK de volta para o host
                    try:
                        ack = f"ACK: {ROUTER_ID} recebeu sua mensagem"
                        sock.sendto(ack.encode(), addr)
                        print(f"[{ROUTER_ID}] Enviou ACK para {ip_origem}")
                    except Exception as e:
                        print(f"[{ROUTER_ID}] Falha ao enviar ACK para host: {e}")
                else:
                    print(f"[{ROUTER_ID}] Mensagem recebida de IP desconhecido {ip_origem}: ignorando")

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
    print(f"[{ROUTER_ID}] Roteador Iniciando")
    start_router()
