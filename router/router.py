import threading
import socket
import time
import json
from util import get_neighbors, create_lsa_packet
from dijkstra import run_dijkstra

ROUTER_ID = "routerA"  # esse valor pode vir por argumento/env
PORT = 5000

LSDB = {}  # Link State Database

def send_lsa():
    while True:
        neighbors = get_neighbors(ROUTER_ID)
        lsa_packet = create_lsa_packet(ROUTER_ID, neighbors)
        for neighbor in neighbors:
            addr = (neighbor["ip"], PORT)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(lsa_packet.encode(), addr)
        time.sleep(5)  # intervalo entre os envios

def receive_lsa():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        packet = json.loads(data.decode())
        sender = packet["id"]
        LSDB[sender] = packet
        print(f"[{ROUTER_ID}] Recebeu LSA de {sender}")
        run_dijkstra(ROUTER_ID, LSDB)

if __name__ == "__main__":
    threading.Thread(target=send_lsa, daemon=True).start()
    threading.Thread(target=receive_lsa, daemon=True).start()

    while True:
        time.sleep(1)  # manter o processo vivo
