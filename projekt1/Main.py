#-*- coding: utf-8 -*-

import dendropy
import re
import sys
from projekt1.Drawer import Drawer
from projekt1.Tree_with_info import Tree_with_info
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
    trees_with_info = []
    num_of_trees = len(trees)
    # Tworzenie wszystkich rozbić drzewa i wstawianie ich do tablicy
    for tree in trees:
        tree_with_info = Tree_with_info(tree)
        trees_with_info.append(tree_with_info)

    # Porówanie każdgo elementu z tablicy z innymi tablicami

    for tree_with_info in trees_with_info:
        for other_tree_to_compare in trees_with_info:
            if other_tree_to_compare is not tree_with_info:
                for subtree in other_tree_to_compare.get_tree_break_table():
                    tree_with_info.check_if_tree_break_table_contains(subtree)

    # Zliczenie tych, które powtarzaja sie wiecej niz x% razy i dodanie ich do drzewa konsensusu
    num_of_similar = percent * num_of_trees
    consensus_tree = Tree()
    for tree_with_info in trees_with_info:
        for best_tree_break in tree_with_info.get_tree_breaks_that_has_more_then_x_percent_similar(percent):
            if subtree_is_not_a_child_of_already_added(consensus_tree,best_tree_break):
                consensus_tree.add_child(best_tree_break)

    return consensus_tree

def subtree_is_not_a_child_of_already_added(self, consensus_tree, subtree):

    subtree_as_a_string = subtree.as_string(schema="newick")
    if(subtree_as_a_string in consensus_tree.as_string(schema="newick")):
        return False
    return True


if __name__ == "__main__":
    percent = sys.argv.pop()
    file_path = sys.argv.pop()

    newickTrees = loadData(file_path)
    trees = []
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
        Drawer().drawTree(tree)

        print("\n\n")

        tree.print_plot()

    consensus_tree = find_consensus_tree(trees, percent)
    Drawer().drawTree(consensus_tree)

