

class BreakTree(object):

    def __init__(self, tree_break_parts):
        self.tree_break_parts = tree_break_parts

    def get_rf_distance(self, break_tree):
        distance = self._count_differences_by_subtract_from_first_tree_break_parts_second(self, break_tree) + \
                   self._count_differences_by_subtract_from_first_tree_break_parts_second(break_tree, self)
        return distance

    @staticmethod
    def _count_differences_by_subtract_from_first_tree_break_parts_second(first_break_tree, second_break_tree):
        differences = 0
        for tree_break_part in first_break_tree.tree_break_parts:
            found_equal_break_part = False
            for second_tree_break_part in second_break_tree.tree_break_parts:
                if tree_break_part.equals_to(second_tree_break_part):
                    found_equal_break_part = True
                    break
            if not found_equal_break_part:
                differences += 1
        return differences
