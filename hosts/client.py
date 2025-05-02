import os
import subprocess
import time

def ping_test(target_ip):
    print(f"[HOST] Testando ping para {target_ip}...")
    response = subprocess.run(["ping", "-c", "4", target_ip], capture_output=True, text=True)
    print(response.stdout)

if __name__ == "__main__":
    # Pode vir de variável de ambiente ou argumento
    destino = os.environ.get("PING_TARGET", "192.168.20.2")
    time.sleep(5)  # tempo para a rede "subir"
    ping_test(destino)
