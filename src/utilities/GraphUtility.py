

import numpy as np

from CMSHash import CMShash


class Graph:
    def __init__(self):
        self.nodes = []

    def contains(self, name):
        for node in self.nodes:
            if(node.name == name):
                return True
        return False

    # Return the node with the name, create and return new node if not found
    def find(self, name):
        if(not self.contains(name)):
            new_node = Node(name)
            self.nodes.append(new_node)
            return new_node
        else:
            return next(node for node in self.nodes if node.name == name)

    def add_edge(self, parent, child):
        parent_node = self.find(parent)
        child_node = self.find(child)

        parent_node.link_child(child_node)
        child_node.link_parent(parent_node)

    def display(self):
        for node in self.nodes:
            print(
                f'{node.name} links to {[child.name for child in node.children]}')

    def sort_nodes(self):
        self.nodes.sort(key=lambda node: int(node.name))


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []
        self.auth = 1.0
        self.hub = 1.0
        self.pagerank = 1.0

    def link_child(self, new_child):
        for child in self.children:
            if(child.name == new_child.name):
                return None
        self.children.append(new_child)

    def link_parent(self, new_parent):
        for parent in self.parents:
            if(parent.name == new_parent.name):
                return None
        self.parents.append(new_parent)


def init_graph(fname):
    with open(fname) as f:
        lines = f.readlines()

    graph = Graph()

    for line in lines:
        [parent, child] = line.strip().split(',')
        graph.add_edge(parent, child)

    graph.sort_nodes()

    return graph

def hash_graph(fname):
    with open(fname) as f:
        lines = f.readlines()
      
    num_rows = 2
    num_buckets = 80
    m = 9    
    cur_count = CMShash(num_rows, num_buckets, m)

    nodeList = []
    for line in lines:
        [parent, child] = line.strip().split(',')
        cur_count.insert(int(parent), int(child), 1)

        if int(parent) not in nodeList:
            nodeList.append(int(parent))
        if int(child) not in nodeList:
            nodeList.append(int(child))
         
            
    #print(cur_count.get_count(1,3))

    return cur_count, nodeList

