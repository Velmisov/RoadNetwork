from xml.etree import ElementTree as ET
from Node import Node
from Edge import Edge

PATH_TO_NODES_FILE = './name.nod.xml'

nodesTree = ET.parse(PATH_TO_NODES_FILE)
nodesRoot = nodesTree.getroot()

nodes = {}

for node in nodesRoot:
    if node.tag == 'node':
        attributes = node.attrib
        nodes[attributes['id']] = Node(attributes['id'])

for _id in nodes:
    print(_id, nodes[_id])

PATH_TO_EDGES_FILE = './name.edg.xml'

edgesTree = ET.parse(PATH_TO_EDGES_FILE)
edgesRoot = edgesTree.getroot()

edges = {}

for edge in edgesRoot:
    if edge.tag == 'edge':
        attributes = edge.attrib
        edges[attributes['id']] = Edge(attributes['id'], attributes['from'], attributes['to'])

for _id in edges:
    print(_id, edges[_id])
