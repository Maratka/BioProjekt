#-*- coding: utf-8 -*-

import dendropy
import re
from projekt1 import draw
import projekt1.draw
import sys
from projekt1.Comparer import Comparer
from projekt1.Converter import Converter
from projekt1.Cluster_Tree import Cluster_Tree
from projekt1.break_converter import BreakConverter
from dendropy import Tree, TaxonNamespace

def loadData(path):
    """
    param: path - scieżka do pliku
    return: tree - drzewo w formacie newick (string)
    """
    file = open(path, 'r')
    trees = []
    while True:
        tree = file.readline()
        if tree is "":
            break
        trees.append(tree)

    file.close()
    return trees

def checkTree(tree):
    """ Sprawdza zgodność rodziny klastrów
    param: tree - drzewo w formacie newick (string)
    return: boolean
    """
    #nazwy węzłów
    tree = re.findall(r"[a-zA-Z]+", tree)

    #liczba wystapień każdej nazwy
    nodesCount = {}
    for node in tree:
        if node in nodesCount:
            return False
        else:
            nodesCount[node] = 1

    return True


def find_consensus_tree(trees, precent):

    consensus_tree = None
    cluster_trees = []
    num_of_trees = len(trees)
    # Tworzenie wszystkich rozbić drzewa i wstawianie ich do tablicy
    for tree in trees:
        cluster_tree = Cluster_Tree(tree)
        cluster_trees.append(cluster_tree)

    # Porówanie każdgo elementu z tablicy z innymi tablicami
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
            if cluster.found > num_of_similar:
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

if __name__ == "__main__":
    percent = sys.argv.pop()
    file_path = sys.argv.pop()

    newickTrees = loadData(file_path)
    trees = []
    break_trees = []
    for newickTree in newickTrees:
        if not checkTree(newickTree):
            print("Rodzina klastrów nie jest zgodna.")
            exit()
        else:
            print("Rodzina klastrów jest zgodna.")

        print("\n\n")

        tree = dendropy.Tree.get(
                data=newickTree,
                schema="newick")
        trees.append(tree)
        draw.drawTree(tree)
        break_tree = BreakConverter().tree_to_break_tree(tree)
        break_trees.append(break_tree)

        print("\n\n")

        # tree.print_plot()

    for break_tree_index in range(len(break_trees)):
        if break_tree_index+1 < len(break_trees):
            distance = break_trees[break_tree_index].get_rf_distance(break_trees[break_tree_index+1])
            print(str(distance))

    consensus_tree = find_consensus_tree(trees, percent)
    print("Consensus tree \n\n")
    draw.drawTree(consensus_tree)

