from dendropy import Tree, Node
from projekt1.New_Node import New_Node

__author__ = 'Gosia'
from projekt1.Cluster import Cluster

class Converter:

    def get_cluster_list(self,tree):
        return self.prepare_cluster_list_for_node(tree.seed_node)

    def prepare_cluster_list_for_node(self, node):
        cluster_list = []
        if node.is_leaf():
            taxon = node.taxon
            cluster = Cluster(taxon, node)
            cluster_list.append(cluster)
        else:
            leafs = node.leaf_nodes()
            taxon = node.taxon
            cluster = Cluster(taxon,leafs)
            childs = node. child_nodes()
            cluster_list.append(cluster)

            for child in childs:
                child_cluster = self.prepare_cluster_list_for_node(child)
                cluster_list += child_cluster


        return cluster_list

    def get_dendropy_tree(self, cluster_tree):

        consensus_tree_dendropy =  Tree()
        #wydizelenie lisc i nodów
        leafs = []
        nodes = []
        for cluster in cluster_tree.get_cluster_list():
            if cluster.taxon is not None:
                leafs.append(cluster)
            if cluster.taxon is None:
                nodes.append(New_Node(cluster))

        nodes.sort(key=lambda x: x.num_leafs)
        created_nodes = []
        for node in nodes:

            created_node = Node()
            for leaf in node.node.clusters:
                if not self.is_leaf_in_leafs(leaf,leafs):
                    sub_created_node, created_nodes = self.find_created_node_with_leaf(created_nodes, leaf)
                    if sub_created_node is not None:
                        created_node.add_child(sub_created_node)
                else:
                    created_node.add_child(leaf)
                    leafs = self.remove_leaf_from_list(leaf,leafs)

            created_nodes.append(created_node)


        tree = Tree(seed_node=created_nodes[0])
        return tree

    def find_created_node_with_leaf(self, created_nodes, leaf):

        for created_node in created_nodes:
            for leaf_of_creaded_node in created_node.leaf_nodes():
                if leaf_of_creaded_node.taxon.label is leaf.taxon.label:
                    created_nodes.remove(created_node)
                    return created_node, created_nodes

        return None, created_nodes

    def is_leaf_in_leafs(self, leaf, leafs):

        for leaf_tmp in leafs:
            if leaf_tmp.taxon.label is leaf.taxon.label:
                return True

        return False

    def remove_leaf_from_list(self,leaf,leafs):

        for leaf_in_list in leafs:
            if leaf_in_list.taxon.label is leaf.taxon.label:
                leafs.remove(leaf_in_list)

        return  leafs




