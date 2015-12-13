__author__ = 'Gosia'

class New_Node:

    def __init__(self, node):
        self.node = node
        self.num_leafs = len(node.clusters)
        self.is_used = False