from xml.etree import ElementTree as ET
from Node import Node

PATH_TO_NODES_FILE = './name.nod.xml'

nodesTree = ET.parse(PATH_TO_NODES_FILE)
nodesRoot = nodesTree.getroot()

nodes = []

for node in nodesRoot:
    print(node.attrib)
    if node.tag == 'node':
        nodes.append(Node(node.attrib['id']))

for node in nodes:
    print(node)
