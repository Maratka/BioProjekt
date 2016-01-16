import itertools

from projekt2.Cluster_Tree import Cluster_Tree
from projekt2.Comparer import Comparer


class TreeCompatibility(object):

    def check_tree_compatibility(self, tree):
        cluster_tree = Cluster_Tree(tree)
        return self.check_cluster_tree_compatibility(cluster_tree)

    def check_cluster_tree_compatibility(self, cluster_tree):
        for cluster_pair in itertools.combinations(cluster_tree.get_cluster_list(), 2):
            first_cluster = cluster_pair[0]
            second_cluster = cluster_pair[1]
            if not Comparer().is_cluster_included_in_another(
                    first_cluster, second_cluster) and not Comparer().is_cluster_included_in_another(
                second_cluster, first_cluster) and Comparer().have_clusters_common_elements(
                second_cluster, first_cluster):
                return False
        return True

    def check_break_tree_compatibility(self, break_tree):
        """Sprawdzenie czy rodzina rozbic jest zgodna"""
        for i, break_part in enumerate(break_tree.tree_break_parts):
            for j in range(i+1, len(break_tree.tree_break_parts)):
                if not break_part.check_break_compatibility(break_tree.tree_break_parts[j]):
                    return False
        return True

