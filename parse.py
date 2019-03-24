import sumolib
from Edge import Edge


def parse(path_to_net_file):
    net = sumolib.net.readNet(path_to_net_file)

    edges = {}
    for edge in net.getEdges():
        edges[edge.getID()] = Edge(edge.getID(), edge.getFromNode().getID(), edge.getToNode().getID(), edge.getLength())

    for edge in net.getEdges():
        for out in edge.getOutgoing():
            edges[edge.getID()].add_outgoing(edges[out.getID()])

    return edges
