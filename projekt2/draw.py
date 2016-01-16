#-*- coding: utf-8 -*-
import dendropy

INDENT = 4

def drawTree(tree):
    """
    :param tree - drzewo z dendropy
    :return:
    """
    children = tree.seed_node.child_nodes()
    childrenNumber = len(children)

    for i in range(0, (int)(childrenNumber/2), 1):
        pos = "MID"
        if i == 0:
            pos = "FIRST"
        elif i == (int)(childrenNumber/2) - 1:
            pos = "LAST"
        drawRightSubtree(children[i], 1, [], pos)

    print(" ", end="")
    print(" " * (INDENT-1), end="")
    print(getName(tree.seed_node))

    for i in range((int)(childrenNumber/2), childrenNumber, 1):
        childPos = "MID"
        if i == childrenNumber - 1:
            childPos = "LAST"
        elif i == (int)(childrenNumber/2):
            childPos = "FIRST"
        drawLeftSubtree(children[i], 1, [], childPos)


def drawLeftSubtree(node, depth, edges, pos):
    """
    Wyrysowywanie lewych poddrzew
    :param
    node - akutalny węzeł;
    depth - głębokość węzła;
    edges - połączenia wynikające z poprzednich poziomów, które należy rysować;
    pos - pozycja węzła w poddrzewie (FIRST, MID, LAST);
    """
    children = node.child_nodes()
    childrenNumber = len(children)

    # dodać swój poziom
    if (depth not in edges):
        edges.append(depth)

    # rysować prawe dzieci
    for i in range(0, (int)(childrenNumber/2), 1):
        childPos = "MID"
        if i == 0:
            childPos = "FIRST"
        elif i == (int)(childrenNumber/2) - 1:
            childPos = "LAST"
        drawRightSubtree(children[i], depth+1, edges, childPos)

    # wyrysować wszystkie poziomy
    currentIndent = 0
    for i in range(len(edges)):
        sign = "|"
        if (i == len(edges) - 1) and (pos == "LAST"):
            sign = "\\"
        print(" " * (edges[i] * INDENT - currentIndent), end=sign)
        currentIndent = edges[i] * INDENT + 1

    # wyrysować gałąź węzła
    print("-" * (INDENT-1), end="")
    print(getName(node))

    # rysować lewe dzieci - bez poziomu rodzica jeśli skrajny
    if (pos == "LAST") and (depth in edges):
        edges.remove(depth)

    for i in range((int)(childrenNumber/2), childrenNumber, 1):
        childPos = "MID"
        if i == childrenNumber - 1:
            childPos = "LAST"
        elif i == (int)(childrenNumber/2):
            childPos = "FIRST"
        drawLeftSubtree(children[i], depth+1, edges, childPos)

    # usunąć swój poziom
    if depth in edges:
        edges.remove(depth)


def drawRightSubtree(node, depth, edges, pos):
    """
    Wyrysowywanie prawych poddrzew
    :param
    node - akutalny węzeł;
    depth - głębokość węzła;
    edges - połączenia wynikające z poprzednich poziomów, które należy rysować;
    pos - pozycja węzła w poddrzewie (FIRST, MID, LAST);
    """
    children = node.child_nodes()
    childrenNumber = len(children)

    # rysować prawe dzieci - bez poziomu rodzica jeśli skrajny
    if (pos != "FIRST") and (depth not in edges):
        edges.append(depth)

    for i in range(0, (int)(childrenNumber/2), 1):
        childPos = "MID"
        if i == 0:
            childPos = "FIRST"
        elif i == (int)(childrenNumber/2) - 1:
            childPos = "LAST"
        drawRightSubtree(children[i], depth+1, edges, childPos)

    # dodać swój poziom
    if (depth not in edges):
        edges.append(depth)

    # wyrysować wszystkie poziomy
    currentIndent = 0
    for i in range(len(edges)):
        sign = "|"
        if (i == len(edges) - 1) and (pos == "FIRST"):
            sign = "/"
        print(" " * (edges[i] * INDENT - currentIndent), end=sign)
        currentIndent = edges[i] * INDENT + 1

    # wyrysować gałąź węzła
    print("-" * (INDENT-1), end="")
    print(getName(node))

    # rysować lewe dzieci
    for i in range((int)(childrenNumber/2), childrenNumber, 1):
        childPos = "MID"
        if i == childrenNumber - 1:
            childPos = "LAST"
        elif i == (int)(childrenNumber/2):
            childPos = "FIRST"
        drawLeftSubtree(children[i], depth+1, edges, childPos)

    # usunąć swój poziom
    if depth in edges:
        edges.remove(depth)


def getName(node):
    if node.taxon:
        return str(node.taxon).replace('\'', "")
    if node.label:
        return node.label
    return "+"
