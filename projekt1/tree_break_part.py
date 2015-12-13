

class TreeBreakPart(object):

    def __init__(self, leaves_set_a, leaves_set_b):
        self.leaves_set_a = leaves_set_a
        self.leaves_set_b = leaves_set_b

    def __str__(self):
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
        return (self._are_leaves_sets_equals(self.leaves_set_a, tree_break_part.leaves_set_a) and
                self._are_leaves_sets_equals(self.leaves_set_b, tree_break_part.leaves_set_b)) or \
                 (self._are_leaves_sets_equals(self.leaves_set_b, tree_break_part.leaves_set_a) and
                  self._are_leaves_sets_equals(self.leaves_set_a, tree_break_part.leaves_set_b))

    def _are_leaves_sets_equals(self, first_set, second_set):
        return self._is_first_set_equals_or_sub_set_of_second(first_set, second_set) and\
               self._is_first_set_equals_or_sub_set_of_second(second_set, first_set)

    @staticmethod
    def _is_first_set_equals_or_sub_set_of_second(first_set, second_set):
        for fs_leaf in first_set:
            leaf_found = False
            for ss_leaf in second_set:
                if fs_leaf.taxon.label == ss_leaf.taxon.label:
                    leaf_found = True
                    break
            if not leaf_found:
                return False
        return True



