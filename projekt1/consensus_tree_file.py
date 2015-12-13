from projekt1.Cluster_Tree import Cluster_Tree
from projekt1.Comparer import Comparer
from projekt1.Converter import Converter

__author__ = 'Gosia'

def find_consensus_tree(trees, percent):

    consensus_tree = None
    cluster_trees = []
    num_of_trees = len(trees)
    # Tworzenie wszystkich rozbiæ drzewa i wstawianie ich do tablicy
    for tree in trees:
        cluster_tree = Cluster_Tree(tree)
        cluster_trees.append(cluster_tree)

    # Porówanie ka¿dgo elementu z tablicy z innymi tablicami
    for cluster_tree in cluster_trees:
        for other_cluster_tree in cluster_trees:
            if other_cluster_tree is not cluster_tree:
                for cluster in other_cluster_tree.get_cluster_list():
                    cluster_tree.count_if_contain_the_same(cluster)

    # Zliczenie tych, które powtarzaja sie wiecej niz x% razy i dodanie ich do drzewa konsensusu
    num_of_similar = float(percent) * num_of_trees
    # wybranie tych klastrow z kazdego dzrzewa, ktor emaja wiecej niz percent procent zgodnosci i nie powtarzaja sie
    consensus_tree = Cluster_Tree(None)
    for cluster_tree in cluster_trees:
        for cluster in cluster_tree.get_cluster_list():
            if cluster.found >= num_of_similar:
                if not cluster_is_in_tree(cluster, consensus_tree):
                    consensus_tree.add_cluster_to_cluster_list(cluster)

    # przekonvertowanie tego drzewa na dendropy
    consensus_tree_dendropy = Converter().get_dendropy_tree(consensus_tree)

    return consensus_tree_dendropy

def cluster_is_in_tree(cluster, cluster_tree):
    for cluster_in_tree in cluster_tree.get_cluster_list():
        if Comparer().are_the_same(cluster_in_tree,cluster):
            return True
    return False
