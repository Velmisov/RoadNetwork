
class Edge:
    def __init__(self, _id, out_of, to):
        self.id = _id
        self.out_of = out_of
        self.to = to

    def __str__(self):
        return "Edge. id: '" + self.id + "', out of: '" + self.out_of + "', to: '" + self.to + "'"
