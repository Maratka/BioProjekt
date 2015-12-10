#-*- coding: utf-8 -*-

import dendropy
import re

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

def drawTree(tree):
    """
    :param tree - drzewo z dendropy
    :return:
    """
    #leavesNumber = len(tree.leaf_edges())
    #width = leavesNumber * 2 - 1
    drawNode(tree.seed_node, 0, [], "MID", "")


def drawNode(node, depth, edges, nodeType, side):
    INDENT = 4

    children = node.child_nodes()
    childrenNumber = len(children)

    if childrenNumber != 0 and depth != 0 and side == "L" and (depth not in edges):
        edges.append(depth)

    for i in range(0, (int)(childrenNumber/2), 1):
        type = "MID"
        if i == 0:
            type = "FIRST"
        drawNode(children[i], depth+1, edges, type, "R")


    if (side == "L") and (depth in edges) and (nodeType == "LAST"):
        edges.remove(depth)

    sign = "|"
    if nodeType == "FIRST":
        sign = "/"
    elif nodeType == "LAST":
        sign = "\\"
    elif (depth in edges):
        sign = ""


    currentIndent = 0
    sorted(edges, key=int)
    for i in range(len(edges)):
        print(" " * (edges[i] * INDENT - currentIndent), end="|")
        currentIndent = edges[i] * INDENT + 1

    print(" " * (depth * INDENT - currentIndent), end=sign)
    print("-" * (INDENT-1), end="")

    if node.taxon:
        print(str(node.taxon).replace('\'', ""))
    elif node.label:
        print(node.label)
    else:
        print("+")


    if childrenNumber != 0 and depth != 0 and side == "R" and (depth not in edges):
        edges.append(depth)

    for i in range((int)(childrenNumber/2), childrenNumber, 1):
        type = "MID"
        if i == childrenNumber - 1:
            type = "LAST"
        drawNode(children[i], depth+1, edges, type, "L")

    if (side == "R") and (depth in edges):
        edges.remove(depth)


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

drawTree(tree)

print("\n\n")

tree.print_plot()
