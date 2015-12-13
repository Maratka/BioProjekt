from projekt1.Comparer import Comparer
from projekt1.Converter import Converter

__author__ = 'Gosia'

class Cluster_Tree:

    def __init__(self, tree):
        if tree is None:
            self.__clusters_list = []
        else:
            self.__clusters_list = Converter().get_cluster_list(tree)


    def get_cluster_list(self):
        return self.__clusters_list

    def add_cluster_to_cluster_list(self,cluster):
        self.__clusters_list.append(cluster)

    def count_if_contain_the_same(self, cluster):
        for my_cluster in self.__clusters_list:
            if Comparer().are_the_same(my_cluster, cluster):
                    my_cluster.found += 1
        pass
