from queue import PriorityQueue
from Vehicle import Vehicle
import traci


class RoadNetwork:
    def __init__(self, nodes, edges, vehicles=None):
        self.nodes = nodes
        self.edges = edges
        self.vehicles = vehicles
        self.__subscribe_edges()

    @staticmethod
    def empty():
        return not (traci.simulation.getMinExpectedNumber() > 0)

    def simulation_step(self):
        traci.simulationStep()

        subscription_results = {}
        for edge_id in self.edges:
            subscription_results[edge_id] = traci.edge.getSubscriptionResults(edge_id)
            self.edges[edge_id].weight = subscription_results[edge_id][0x10] + 1
        return subscription_results

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
            for edge in self.nodes[par[current]].edges.values():
                if edge.out_of == par[current] and edge.to == current:
                    route.append(edge.id)
                    break
            current = par[current]
        return list(reversed(route))

    def __subscribe_edges(self):
        for edge in self.edges:
            traci.edge.subscribe(edge, [0x10])
