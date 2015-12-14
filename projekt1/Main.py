#-*- coding: utf-8 -*-

import dendropy
import re
import sys
from projekt1 import draw
from projekt1.common_extend import CommonExtend
from projekt1.tree_compatibility import TreeCompatibility
from projekt1.tree_pruning import pruneTree
from projekt1.Comparer import Comparer
from projekt1.Converter import Converter
from projekt1.Cluster_Tree import Cluster_Tree
from projekt1.break_converter import BreakConverter
from projekt1 import consensus_tree_file

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
        if not TreeCompatibility().check_tree_compatibility(tree):
            print("Niezgodnosc rodziny klastrow")
            exit()
        trees.append(tree)
        draw.drawTree(tree)
        print("\n\n")

        leaves_str = input("Podaj podzbiór liści do którego drzewo ma być obcięte (rozdzielone spacją):\n")
        if leaves_str:
            leaves = leaves_str.split(" ")
            print("\n")
            prunedTree = pruneTree(dendropy.Tree(tree), leaves)
            if prunedTree:
                draw.drawTree(prunedTree)

        break_tree = BreakConverter().tree_to_break_tree(tree)
        break_trees.append(break_tree)

        print("\n\n")

        # tree.print_plot()

    for break_tree_index in range(len(break_trees)):
        if break_tree_index+1 < len(break_trees):
            distance = break_trees[break_tree_index].get_rf_distance(break_trees[break_tree_index+1])
            print(str(distance))

    try:
        # Znajdowanie drzewa konsensusu o podanym procencie zgodności
        consensus_tree = consensus_tree_file.find_consensus_tree(trees, percent)
        print("Consensus tree \n\n")
        #Wypisywanie drzewa konsensusu
        draw.drawTree(consensus_tree)
    except Exception as error:
        # Jezeli wyjatek -> rodzina klastrow niezgodna dla drzewa konsensusu
        print(str(error))

    try:
        # Znajdowanie wspolnego rozszerzenia
        common_extend = CommonExtend().get_common_extend(trees)
        #Wypisywanie wspolnego rozszerzenia
        draw.drawTree(common_extend)
    except Exception as error:
        # Jezeli wyjatek -> nie ma wspolnego rozszerzenia bo rodzina klastrow niezgodna
        print("Nie istnieje wspolne rozszerzenie")



