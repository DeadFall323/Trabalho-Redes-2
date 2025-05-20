# hosts/host.py

import socket
import sys
import time

def main():
    if len(sys.argv) < 2:
        print("Uso: python host.py <nome_do_host>")
        sys.exit(1)

    host_name = sys.argv[1]
    router_ip = "192.168.250.11"  # IP do roteador ao qual esse host está conectado
    router_port = 10000       # Porta padrão de roteadores

    print(f"[{host_name}] Iniciado e tentando se comunicar com o roteador em {router_ip}:{router_port}")

    # Criação do socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    # Exemplo de envio de mensagem
    mensagem = f"MENSAGEM_DE_{host_name}_PARA_host6"
    try:
        sock.sendto(mensagem.encode(), (router_ip, router_port))
        print(f"[{host_name}] Enviado: {mensagem}")

        # Aguarda resposta
        data, _ = sock.recvfrom(1024)
        print(f"[{host_name}] Recebido: {data.decode()}")

    except socket.timeout:
        print(f"[{host_name}] Sem resposta do roteador.")
    except Exception as e:
        print(f"[{host_name}] Erro: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
