import heapq

def processa_lsa(lsdb, lsa):
    origin = lsa["origin"]
    if origin not in lsdb or lsdb[origin]["timestamp"] < lsa["timestamp"]:
        lsdb[origin] = lsa
        return True
    return False

def atualiza_lsdb(router_id, lsdb):
    print(f"[{router_id}] LSDB atualizado:")
    for origin, lsa in lsdb.items():
        print(f" - {origin}: {lsa['neighbors']}")

def calcula_tabela_roteamento(router_id, lsdb):
    # Construir o grafo com base na LSDB
    grafo = {}
    for origem, lsa in lsdb.items():
        grafo[origem] = list(lsa["neighbors"].keys())

    # Dijkstra
    dist = {router: float('inf') for router in grafo}
    anterior = {router: None for router in grafo}
    dist[router_id] = 0

    fila = [(0, router_id)]
    while fila:
        custo, atual = heapq.heappop(fila)
        for vizinho in grafo.get(atual, []):
            if dist[vizinho] > custo + 1:  # custo fixo de 1
                dist[vizinho] = custo + 1
                anterior[vizinho] = atual
                heapq.heappush(fila, (dist[vizinho], vizinho))

    # Construir tabela de roteamento: destino → próximo salto
    tabela = {}
    for destino in grafo:
        if destino == router_id or dist[destino] == float('inf'):
            continue
        # Voltar até o próximo salto a partir do destino
        prox = destino
        while anterior[prox] is not None and anterior[prox] != router_id:
            prox = anterior[prox]
        if anterior[prox] is None:
            # Não conseguiu encontrar caminho confiável até o router_id
            continue
        tabela[destino] = prox

    return tabela
