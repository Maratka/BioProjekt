from projekt2.break_tree import BreakTree
from projekt2.tree_break_part import TreeBreakPart


class BreakConverter(object):

    @staticmethod
    def tree_to_break_tree(tree):
        """
        Metoda pobiera drzewo w postaci dendropy i konwertuje je na  rodzine rozbic
        Generowanie wszystkich rozbic polega na dzieleniu drzewa na podzbiory lisci
        usuwajac po jednej z krawedzi (usuniecie krawiedzi dzieli drzewo na dwa podzbiory -> rozbicie)
        """
        seed_node = tree.seed_node
        break_tree_parts = []

        # Dla kazdej galezi, w kolejnosci poziomow drzewa
        for edge in tree.levelorder_edge_iter():
            leaves_set_a = []
            leaves_set_b = []
            # wezel polaczony z galezia, glebiej w drzewie
            head_node = edge.head_node
            # jezeli nie ma parenta to jestesmy w galezi nad rootem (sztuczna dodana przez biblioteke)
            if head_node.parent_node is None:
                continue
            # Wez wszystkie liscie, do ktorych da sie dojsc idac wglab od tego wierzcholka
            for leaf in head_node.leaf_nodes():
                leaves_set_a.append(leaf)

            # wez pozostale liscie z drzewa
            for leaf in seed_node.leaf_nodes():
                if leaf not in leaves_set_a:
                    leaves_set_b.append(leaf)

            # utworz z tych lisci obiekt TreeBreakPart i dodaj do listy rozbic
            break_tree_parts.append(TreeBreakPart(leaves_set_a, leaves_set_b))
        # z listy rozbic stworz drzewo (obiekt) w postaci rozbic i zwroc
        return BreakTree(break_tree_parts)

