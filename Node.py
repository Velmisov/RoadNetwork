
class Node:
    def __init__(self, _id, edges=None):
        self.id = _id
        self.edges = edges or {}

    def __str__(self):
        return "Node. id: '" + self.id + "', edges: " + str(self.edges)

    def add_edge(self, edge):
        self.edges[edge.id] = edge

    def remove_edge(self, _id):
        self.edges.pop(_id)
