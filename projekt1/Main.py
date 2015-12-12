#-*- coding: utf-8 -*-

import dendropy
import re
import draw

def loadData(path):
    """
    param: path - scieżka do pliku
    return: tree - drzewo w formacie newick (string)
    """
    file = open(path, 'r')
    tree = file.read()
    file.close()
    return tree

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

newickTree = loadData('../tree.txt')
if not checkTree(newickTree):
    print("Rodzina klastrów nie jest zgodna.")
    exit()
else:
    print("Rodzina klastrów jest zgodna.")

print("\n\n")

tree = dendropy.Tree.get(
        data=newickTree,
        schema="newick")

draw.drawTree(tree)

print("\n\n")

tree.print_plot()
