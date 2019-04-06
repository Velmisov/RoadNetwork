from queue import PriorityQueue
from models.Vehicle import Vehicle
import traci


class RoadNetwork:
    def __init__(self, edges, vehicles=None):
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
            vehicle_number = subscription_results[edge_id][0x10]
            mean_speed = subscription_results[edge_id][0x11]
            if vehicle_number == 0 or mean_speed == 0:
                mean_speed = self.edges[edge_id].max_speed
            self.edges[edge_id].weight = self.edges[edge_id].length / mean_speed
        return subscription_results

    def Deijkstra(self, vehicle_id):
        INF = 1000
        vehicle = Vehicle(vehicle_id)
        dist = {edge_id: INF for edge_id in self.edges}
        par = {edge_id: edge_id for edge_id in self.edges}
        pq = PriorityQueue()
        first_edge_id = vehicle.get_first_edge()
        last_node_id = self.edges[vehicle.get_last_edge()].to
        last_edge_id = None
        pq.put((0, first_edge_id))
        dist[first_edge_id] = 0
        while not pq.empty():
            (d, edge_id) = pq.get()
            if self.edges[edge_id].to == last_node_id:
                last_edge_id = edge_id
                break
            for edge in self.edges[edge_id].outgoing.values():
                to = edge.id
                weight = edge.weight
                if dist[to] > d + weight:
                    dist[to] = d + weight
                    par[to] = edge_id
                    pq.put((dist[to], to))

        if last_edge_id is None or dist[last_edge_id] == INF:
            return None

        route = []
        current = last_edge_id
        while par[current] != current:
            route.append(current)
            current = par[current]
        route.append(first_edge_id)
        return list(reversed(route))

    def __subscribe_edges(self):
        for edge in self.edges:
            traci.edge.subscribe(edge, [0x10, 0x11])
