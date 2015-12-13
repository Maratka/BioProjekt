from dendropy import Tree

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
                nodes.append(cluster)

        return None




