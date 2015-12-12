from projekt1.Tree_break_counter import Tree_break_counter

__author__ = 'Gosia'

class Tree_with_info:

    def __init__(self, tree):
        self.__tree = tree
        self.__tree_break_table = []

    def get_tree_break_table(self):
        return self.__tree_break_table

    def __prepare_tree_break_table(self):
        self.__add_tree_break_to_tree_break_table(self.__tree.seed_node)

    def __add_tree_break_to_tree_break_table(self, subtree):
        childs = subtree.child_nodes()
        if not self.check_if_tree_break_table_contains(subtree):
            self.__tree_break_table.append(Tree_break_counter(subtree))
            for child in childs:
                self.__add_tree_break_to_tree_break_table(child)

    def check_if_tree_break_table_contains(self,subtree):
        if subtree not in self.__tree_break_table(lambda x : x.tree):
            return False
        self.__tree_break_table(lambda x : x.tree == subtree).counter += 1
        return True

    def get_tree_breaks_that_has_more_then_x_percent_similar(self, num_of_similar_needed):
        bigest_subtrees = []
        for subtree in self.__tree_break_table:
            if subtree.counter > num_of_similar_needed:
                if self.__subtree_is_not_a_child_of_added(bigest_subtrees,subtree):
                    bigest_subtrees.append(subtree)

        return bigest_subtrees


