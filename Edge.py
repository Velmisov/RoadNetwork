
class Edge:
    def __init__(self, _id, out_of, to, weight=None):
        self.id = _id
        self.out_of = out_of
        self.to = to
        self.weight = weight or 0

    def __str__(self):
        return "Edge. id: '" + self.id + "', out of: '" + self.out_of + "', to: '" + self.to + "'"
