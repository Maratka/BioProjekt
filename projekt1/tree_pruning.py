#-*- coding: utf-8 -*-
import dendropy

def pruneTree(tree, leaves):
    """
    :param tree - drzewo z dendropy, leaves - zbiór liści, który ma zostać w drzewie
    :return: tree - przycięte drzewo
    """
    markedNodes = []  # węzły, które mają być sprawdzane (jeśli mają 0 dzieci - usuwane, jeśli 1 - zwijane)

    # oznaczenie wszystkich liści nie znajdujących się w podzbiorze dzieci, do którego drzewo ma być przycięte
    for leaf in tree.leaf_node_iter():
        if getLeafName(leaf) not in leaves:
            markedNodes.append(leaf)

    # przycinanie drzewa
    checkTree(markedNodes)

    # czy całe drzewo zostało usunięte (został tylko root)
    if len(tree.seed_node.child_nodes()) == 0:
        return None

    return tree


def checkTree(markedNodes):
    """
    Sprawdza oznaczone węzły, jeśli nie mają one żadnych dzieci są usuwane
    Jeśli oznaczony węzeł ma tylko jedno dziecko, krawędź jest "zwijana" (a->b->c  =>  a->c)
    :param markedNodes - węzły, których dziecko zostało usunięte
    :return:
    """

    # jeśli nie ma żadnych oznaczonych węzłów to kończymy
    if not markedNodes:
        return

    newMarkedNodes = []

    for node in markedNodes:
        # usunięcie węzłów, które nie mają żadnych dzieci
        if len(node.child_nodes()) == 0:
            parent = node.parent_node
            if not parent:  # sprawdzenie czy nie doszliśmy do roota
                return

            parent.remove_child(node)
            if parent not in newMarkedNodes:  # oznaczenie rodzica do sprawdzenia w kolejnej turze
                newMarkedNodes.append(parent)

        # zwinięcie krawędzi jeśli węzeł ma tylko jedno dziecko (a->b->c  =>  a->c)
        elif len(node.child_nodes()) == 1:
            parent = node.parent_node
            if not parent:  # sprawdzenie czy nie doszliśmy do roota
                return

            child = node.child_nodes()[0]
            parent.remove_child(node)
            parent.add_child(child)

    checkTree(newMarkedNodes)


def getLeafName(leaf):
    return str(leaf.taxon).replace('\'', "")
