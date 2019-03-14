from xml.etree import ElementTree as ET
from Node import Node
from Edge import Edge

PATH_TO_NODES_FILE = './name.nod.xml'

nodes_tree = ET.parse(PATH_TO_NODES_FILE)
nodes_root = nodes_tree.getroot()

nodes = {}

for node in nodes_root:
    if node.tag == 'node':
        attributes = node.attrib
        nodes[attributes['id']] = Node(attributes['id'])

PATH_TO_EDGES_FILE = './name.edg.xml'

edges_tree = ET.parse(PATH_TO_EDGES_FILE)
edges_root = edges_tree.getroot()

edges = {}

for edge in edges_root:
    if edge.tag == 'edge':
        attributes = edge.attrib
        new_edge = Edge(attributes['id'], attributes['from'], attributes['to'])
        edges[attributes['id']] = new_edge
        nodes[new_edge.out_of].add_edge(new_edge)

for _id in edges:
    print(_id, edges[_id])

for _id in nodes:
    print(_id, nodes[_id])
