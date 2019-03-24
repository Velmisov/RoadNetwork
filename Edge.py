
class Edge:
    def __init__(self, _id, out_of, to, length=None, weight=None, outgoing=None):
        self.id = _id
        self.out_of = out_of
        self.to = to
        self.length = length or 0
        self.weight = weight or 0
        self.outgoing = outgoing or {}

    def __str__(self):
        return "Edge. id: '" + self.id + "', out of: '" + self.out_of + "', to: '" + self.to + "'"

    def add_outgoing(self, edge):
        if edge.id not in self.outgoing:
            self.outgoing[edge.id] = edge
            return True
        return False
