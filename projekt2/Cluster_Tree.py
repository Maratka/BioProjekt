from projekt2.Comparer import Comparer
from projekt2.Converter import Converter

__author__ = 'Gosia'

#Drzewo sk³adaj¹ce siê z listy klastrów
class Cluster_Tree:

    def __init__(self, tree):
        if tree is None:
            #Je¿eli tworzymy puste drzewo, lista jest pusta
            self.__clusters_list = []
        else:
            #Jezeli tworzymy drzewo z drzewa grafowego, dokonywana jest jego konwersja na listê klastrów
            self.__clusters_list = Converter().get_cluster_list(tree)

    #Zwraca listê klastrów
    def get_cluster_list(self):
        return self.__clusters_list

    #Dowanie klastra do listy klastrów
    def add_cluster_to_cluster_list(self,cluster):
        self.__clusters_list.append(cluster)

    #Dla klastra z drzewa klastrów, który jest taki sam jak sprawdzany zwiêkszany jest licznik
    def count_if_contain_the_same(self, cluster):
        for my_cluster in self.__clusters_list:
            #Porównanie czy dal klastry s¹ takie same
            if Comparer().are_the_same(my_cluster, cluster):
                    my_cluster.found += 1
        pass
