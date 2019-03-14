from xml.etree import ElementTree as ET
from Node import Node
from Edge import Edge

PATH_TO_NODES_FILE = './name.nod.xml'

nodesTree = ET.parse(PATH_TO_NODES_FILE)
nodesRoot = nodesTree.getroot()

nodes = []

for node in nodesRoot:
    if node.tag == 'node':
        nodes.append(Node(node.attrib['id']))

for node in nodes:
    print(node)

PATH_TO_EDGES_FILE = './name.edg.xml'

edgesTree = ET.parse(PATH_TO_EDGES_FILE)
edgesRoot = edgesTree.getroot()

edges = []

for edge in edgesRoot:
    if edge.tag == 'edge':
        edges.append(Edge(edge.attrib['id'], edge.attrib['from'], edge.attrib['to']))

for edge in edges:
    print(edge)
