import socket
import sys
import time

def main():
    if len(sys.argv) < 3:
        print("Uso: python host.py <nome_do_host> <ip_do_roteador>")
        sys.exit(1)

    host_name = sys.argv[1]
    router_ip = sys.argv[2]  # Recebe IP do roteador da linha de comando
    router_port = 5000       # Porta usada pelo roteador (mesma do router.py)

    print(f"[{host_name}] Iniciado e tentando se comunicar com o roteador em {router_ip}:{router_port}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    mensagem = f"MENSAGEM_DE_{host_name}_PARA_ROTEADOR"
    try:
        sock.sendto(mensagem.encode(), (router_ip, router_port))
        print(f"[{host_name}] Enviado: {mensagem}")

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
