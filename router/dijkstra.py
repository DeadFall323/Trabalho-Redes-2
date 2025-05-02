def run_dijkstra(router_id, lsdb):
    # Simplesmente imprime o conteúdo da LSDB por enquanto
    print(f"\n[{router_id}] Rodando Dijkstra com LSDB:")
    for node, data in lsdb.items():
        print(f"  {node} → {data['neighbors']}")
