from projekt1.Cluster_Tree import Cluster_Tree
from projekt1.Comparer import Comparer
from projekt1.Converter import Converter
from projekt1.tree_compatibility import TreeCompatibility

__author__ = 'Gosia'
#funkcja buduj�ca drzewo konsensusu o podanym procencie z podanej listy drzewe
def find_consensus_tree(trees, percent):

    consensus_tree = None
    cluster_trees = []
    num_of_trees = len(trees)
    # Tworzenie drzew w postaci reprezentacji listy klastr�w z podanych drzew i zapisywanie ich w list�
    for tree in trees:
        cluster_tree = Cluster_Tree(tree)
        cluster_trees.append(cluster_tree)

    # Por�wnanie ka�dego drzewa klastr�w z ka�dym drzewem klastr�w i zapisywanie liczby wyst�pie� klastra z jednego drzewa w innych
    for cluster_tree in cluster_trees:
        for other_cluster_tree in cluster_trees:
            if other_cluster_tree is not cluster_tree:
                for cluster in other_cluster_tree.get_cluster_list():
                    #Sprawdzenie czy w drzewie jest ten klaster co w innym
                    #Jezeli jest to zwi�kszenie licznika zgodno�ci
                    cluster_tree.count_if_contain_the_same(cluster)

    # Wyliczenie ile powinno by� tych samych wyst�pie�, kt�re powtarzaja sie wiecej niz x% razy
    num_of_similar = float(percent) * num_of_trees
    #Utworzenie pustego drzewa klastr�w, kt�re b�dzie budowanie z klastr�w, kt�rych wyst�pienia s� wi�ksze ni� x%
    consensus_tree = Cluster_Tree(None)
    for cluster_tree in cluster_trees:
        for cluster in cluster_tree.get_cluster_list():
            #Sprawdzenie czy liczba wyst�pie� spe�nia warunek
            if cluster.found >= num_of_similar:
                #Sprawdzanie czy ten klaster nie zosta� ju� wcze�niej dodany
                if not cluster_is_in_tree(cluster, consensus_tree):
                    #Dodanie klastra do listy klastr�w dla drzewa konsensusu
                    consensus_tree.add_cluster_to_cluster_list(cluster)

    # Sprawdzenie czy w znalezionym drzewie konsensusu rodzina klastrow jest zgodna
    if not TreeCompatibility().check_cluster_tree_compatibility(consensus_tree):
        raise Exception("Rodzina klastrow nie jest zgodna dla drzewa konsensusu")
    # Przekonwertowanie drzewa z�o�onego z klastr�w na zwyk�e drzewo - grafowe
    consensus_tree_dendropy = Converter().get_dendropy_tree(consensus_tree)

    return consensus_tree_dendropy

def cluster_is_in_tree(cluster, cluster_tree):
    for cluster_in_tree in cluster_tree.get_cluster_list():
        if Comparer().are_the_same(cluster_in_tree,cluster):
            return True
    return False
