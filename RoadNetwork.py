from queue import PriorityQueue
from Vehicle import Vehicle


class RoadNetwork:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def Deijkstra(self, vehicle_id):
        INF = 1000
        vehicle = Vehicle(vehicle_id)
        dist = {node_id: INF for node_id in self.nodes}
        par = {node_id: node_id for node_id in self.nodes}
        pq = PriorityQueue()
        first_node_id = self.edges[vehicle.get_first_edge()].out_of
        last_node_id = self.edges[vehicle.get_last_edge()].to
        pq.put((0, first_node_id))
        while not pq.empty():
            (d, node_id) = pq.get()
            if node_id == last_node_id:
                break
            for edge in self.nodes[node_id].edges.values():
                to = edge.to
                weight = edge.weight
                if dist[to] > d + weight:
                    dist[to] = d + weight
                    par[to] = node_id
                    pq.put((dist[to], to))

        if dist[last_node_id] == INF:
            return None

        route = []
        current = last_node_id
        while par[current] != current:
            route.append(current)
            current = par[current]
        route.append(first_node_id)
        return list(reversed(route))
