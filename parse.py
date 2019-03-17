from xml.etree import ElementTree as ET
from Node import Node
from Edge import Edge


def parse(path_to_nodes_file, path_to_edges_file):
    nodes_tree = ET.parse(path_to_nodes_file)
    nodes_root = nodes_tree.getroot()

    nodes = {}
    for node in nodes_root:
        if node.tag == 'node':
            attributes = node.attrib
            nodes[attributes['id']] = Node(attributes['id'])

    edges_tree = ET.parse(path_to_edges_file)
    edges_root = edges_tree.getroot()

    edges = {}
    for edge in edges_root:
        if edge.tag == 'edge':
            attributes = edge.attrib
            new_edge = Edge(attributes['id'], attributes['from'], attributes['to'])
            edges[attributes['id']] = new_edge
            nodes[new_edge.out_of].add_edge(new_edge)

    return nodes, edges
