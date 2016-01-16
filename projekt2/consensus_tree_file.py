from projekt2.break_converter import BreakConverter
from projekt2.break_tree import BreakTree
from projekt2.Cluster_Tree import Cluster_Tree
from projekt2.Comparer import Comparer
from projekt2.Converter import Converter
from projekt2.tree_compatibility import TreeCompatibility

__author__ = 'Gosia'
#funkcja buduj�ca drzewo konsensusu o podanym procencie z podanej listy drzewe
def find_consensus_tree(trees, percent):

    consensus_tree = None
    break_trees = []
    num_of_trees = len(trees)
    # Tworzenie drzew w postaci reprezentacji listy rozbić z podanych drzew i zapisywanie ich w list�
    for tree in trees:
        break_tree = BreakConverter.tree_to_break_tree(tree)
        break_trees.append(break_tree)

    # Por�wnanie ka�dego drzewa rozbić z ka�dym drzewem rozbić i zapisywanie liczby wyst�pie� rozbicia z jednego drzewa w innych
    for break_tree in break_trees:
        for other_break_tree in break_trees:
            if other_break_tree is not break_tree:
                for break_part in other_break_tree.tree_break_parts:
                    #Sprawdzenie czy w drzewie jest ten break co w innym
                    #Jezeli jest to zwi�kszenie licznika zgodno�ci
                    break_tree.count_if_contain_the_same(break_part)

    # Wyliczenie ile powinno byc tych samych wystapien, ktore powtarzaja sie wiecej niz x% razy
    num_of_similar = float(percent) * num_of_trees
    #Utworzenie pustego drzewa rozbic, ktore bedzie budowanie z rozbic, ktorych wystapienia sa wieksze niz x%
    consensus_tree = BreakTree([])
    for break_tree in break_trees:
        for break_part in break_tree.tree_break_parts:
            #Sprawdzenie czy liczba wystapien spelnia warunek
            if break_part.found >= num_of_similar:
                #Sprawdzanie czy to rozbicie nie zostalo juz wczesniej dodane
                if not break_part_is_in_tree(break_part, consensus_tree):
                    #Dodanie rozbicia do listy rozbic dla drzewa konsensusu
                    consensus_tree.tree_break_parts.append(break_part)

    # Sprawdzenie czy w znalezionym drzewie konsensusu rodzina klastrow jest zgodna
    if not TreeCompatibility().check_break_tree_compatibility(consensus_tree):
        raise Exception("Rodzina klastrow nie jest zgodna dla drzewa konsensusu")
    # Przekonwertowanie drzewa z�o�onego z klastr�w na zwyk�e drzewo - grafowe
    consensus_tree_dendropy = Converter().get_dendropy_tree_from_break_tree(consensus_tree)

    return consensus_tree_dendropy

def break_part_is_in_tree(break_part, consensus_tree):
    for break_part_in_tree in consensus_tree.tree_break_parts:
        if break_part_in_tree.equals_to(break_part):
            return True
    return False
