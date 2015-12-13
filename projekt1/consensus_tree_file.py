from projekt1.Cluster_Tree import Cluster_Tree
from projekt1.Comparer import Comparer
from projekt1.Converter import Converter

__author__ = 'Gosia'
#funkcja buduj¹ca drzewo konsensusu o podanym procencie z podanej listy drzewe
def find_consensus_tree(trees, percent):

    consensus_tree = None
    cluster_trees = []
    num_of_trees = len(trees)
    # Tworzenie drzew w postaci reprezentacji listy klastrów z podanych drzew i zapisywanie ich w listê
    for tree in trees:
        cluster_tree = Cluster_Tree(tree)
        cluster_trees.append(cluster_tree)

    # Porównanie ka¿dego drzewa klastrów z ka¿dym drzewem klastrów i zapisywanie liczby wyst¹pieñ klastra z jednego drzewa w innych
    for cluster_tree in cluster_trees:
        for other_cluster_tree in cluster_trees:
            if other_cluster_tree is not cluster_tree:
                for cluster in other_cluster_tree.get_cluster_list():
                    #Sprawdzenie czy w drzewie jest ten klaster co w innym
                    #Jezeli jest to zwiêkszenie licznika zgodnoœci
                    cluster_tree.count_if_contain_the_same(cluster)

    # Wyliczenie ile powinno byæ tych samych wyst¹pieñ, które powtarzaja sie wiecej niz x% razy
    num_of_similar = float(percent) * num_of_trees
    #Utworzenie pustego drzewa klastrów, które bêdzie budowanie z klastrów, których wyst¹pienia s¹ wiêksze ni¿ x%
    consensus_tree = Cluster_Tree(None)
    for cluster_tree in cluster_trees:
        for cluster in cluster_tree.get_cluster_list():
            #Sprawdzenie czy liczba wyst¹pieñ spe³nia warunek
            if cluster.found >= num_of_similar:
                #Sprawdzanie czy ten klaster nie zosta³ ju¿ wczeœniej dodany
                if not cluster_is_in_tree(cluster, consensus_tree):
                    #Dodanie klastra do listy klastrów dla drzewa konsensusu
                    consensus_tree.add_cluster_to_cluster_list(cluster)

    # Przekonwertowanie drzewa z³o¿onego z klastrów na zwyk³e drzewo - grafowe
    consensus_tree_dendropy = Converter().get_dendropy_tree(consensus_tree)

    return consensus_tree_dendropy

def cluster_is_in_tree(cluster, cluster_tree):
    for cluster_in_tree in cluster_tree.get_cluster_list():
        if Comparer().are_the_same(cluster_in_tree,cluster):
            return True
    return False
