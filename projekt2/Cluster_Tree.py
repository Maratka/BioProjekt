from projekt2.Comparer import Comparer
from projekt2.Converter import Converter

__author__ = 'Gosia'

#Drzewo sk�adaj�ce si� z listy klastr�w
class Cluster_Tree:

    def __init__(self, tree):
        if tree is None:
            #Je�eli tworzymy puste drzewo, lista jest pusta
            self.__clusters_list = []
        else:
            #Jezeli tworzymy drzewo z drzewa grafowego, dokonywana jest jego konwersja na list� klastr�w
            self.__clusters_list = Converter().get_cluster_list(tree)

    #Zwraca list� klastr�w
    def get_cluster_list(self):
        return self.__clusters_list

    #Dowanie klastra do listy klastr�w
    def add_cluster_to_cluster_list(self,cluster):
        self.__clusters_list.append(cluster)

    #Dla klastra z drzewa klastr�w, kt�ry jest taki sam jak sprawdzany zwi�kszany jest licznik
    def count_if_contain_the_same(self, cluster):
        for my_cluster in self.__clusters_list:
            #Por�wnanie czy dal klastry s� takie same
            if Comparer().are_the_same(my_cluster, cluster):
                    my_cluster.found += 1
        pass
