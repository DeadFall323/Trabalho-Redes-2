import json

# Simula uma lista de vizinhos (em um projeto real, isso viria de config ou args)
def get_neighbors(router_id):
    if router_id == "routerA":
        return [{"id": "routerB", "ip": "10.0.0.2", "cost": 1}]
    elif router_id == "routerB":
        return [{"id": "routerA", "ip": "10.0.0.1", "cost": 1}]
    else:
        return []

def create_lsa_packet(router_id, neighbors):
    return json.dumps({
        "id": router_id,
        "neighbors": neighbors
    })
