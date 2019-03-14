
class Edge:
    def __init__(self, _id, outOf, to):
        self.id = _id
        self.outOf = outOf
        self.to = to

    def __str__(self):
        return "Edge. id: '" + self.id + "', out of: '" + self.outOf + "', to: '" + self.to + "'"
