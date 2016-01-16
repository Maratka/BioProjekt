

class TreeBreakPart(object):
    """
    Klasa reprezentujaca pojedyncze rozbicie drzewa
    """

    def __init__(self, leaves_set_a, leaves_set_b):
        # rozbicie na dwa zbiory
        self.leaves_set_a = leaves_set_a
        self.leaves_set_b = leaves_set_b
        self.found = 0

    def __str__(self):
        """Metoda do wypisywania rozbicia na ekran"""
        result = "<TreeBreakPart object: "
        result += "leaves_set_a: "
        for leaf in self.leaves_set_a:
            result += leaf.taxon.label
            result += " ,"

        result += "leaves_set_b: "
        for leaf in self.leaves_set_b:
            result += leaf.taxon.label
            result += " ,"
        return result

    def equals_to(self, tree_break_part):
        """
        Sprawdzenie czy to rozbicie (self) jest rowne temu przekazanemu w parametrze.
        Jest rowne jezeli zbiory lisci sa rowne (czyli A1 = A2 i B1 = B2 albo A1 = B2 i B1 = A2)
        """
        return (self._are_leaves_sets_equals(self.leaves_set_a, tree_break_part.leaves_set_a) and
                self._are_leaves_sets_equals(self.leaves_set_b, tree_break_part.leaves_set_b)) or \
                 (self._are_leaves_sets_equals(self.leaves_set_b, tree_break_part.leaves_set_a) and
                  self._are_leaves_sets_equals(self.leaves_set_a, tree_break_part.leaves_set_b))

    def _are_leaves_sets_equals(self, first_set, second_set):
        """
        Czy zbiory lisci sa rowne? Tak jezeli pierwszy jest podzbiorem drugiego a drugi pierwszego
        """
        return self._is_first_set_equals_or_sub_set_of_second(first_set, second_set) and\
               self._is_first_set_equals_or_sub_set_of_second(second_set, first_set)

    @staticmethod
    def _is_first_set_equals_or_sub_set_of_second(first_set, second_set):
        """Czy pierwszy zbior jest podzbiorem drugiego? Tak jezeli wszystkie elementy pierwszego wystepuja w drugim"""
        for fs_leaf in first_set:
            leaf_found = False
            for ss_leaf in second_set:
                if fs_leaf.taxon.label == ss_leaf.taxon.label:
                    leaf_found = True
                    break
            if not leaf_found:
                return False
        return True

    def check_break_compatibility(self, tree_break_part):
        """
        Sprawdzenie czy rozbicia sa zgodne
        Rozbicia {A, B} i {C, D} sa zgodne jesli dokladnie jeden ze zbiorow A*C, A*D, B*C, B*D jest pusty
        """
        disjoint_sets = 0
        if self.check_disjoint_sets(self.leaves_set_a, tree_break_part.leaves_set_a):
            disjoint_sets += 1
        if self.check_disjoint_sets(self.leaves_set_a, tree_break_part.leaves_set_b):
            disjoint_sets += 1
        if self.check_disjoint_sets(self.leaves_set_b, tree_break_part.leaves_set_a):
            disjoint_sets += 1
        if self.check_disjoint_sets(self.leaves_set_b, tree_break_part.leaves_set_b):
            disjoint_sets += 1

        if disjoint_sets == 1:
            return True

        return False

    @staticmethod
    def check_disjoint_sets(set_a, set_b):
        """Sprawdzenie czy zbiory sa rozlaczne"""
        for leaf_a in set_a:
            for leaf_b in set_b:
                if leaf_a.taxon == leaf_b.taxon:
                    return False

        return True
