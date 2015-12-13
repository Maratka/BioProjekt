from Tree_break_counter import Tree_break_counter

__author__ = 'Gosia'

class Tree_with_info:

    def __init__(self, tree):
        self.__tree = tree
        self.__tree_break_table = []
        self.__prepare_tree_break_table()

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
        for tree_break_table_element in self.__tree_break_table:
            if areTwoTreesTheSame(subtree,tree_break_table_element.tree):
                tree_break_table_element.counter += 1
                return True

        return False

    def areTwoTreesTheSame(self, tree_1,tree_2):

        if tree_1.taxon is not tree_2.taxon:
            return False
        if len(tree_1._child_nodes) is not len(tree_2._child_nodes):
            return False

        if tree_1._child_nodes is [] and tree_2._child_nodes is []:
            return True





    def get_tree_breaks_that_has_more_then_x_percent_similar(self, num_of_similar_needed):
        bigest_subtrees = []
        for subtree in self.__tree_break_table:
            if subtree.counter > int(num_of_similar_needed):
                if self.__subtree_is_not_a_child_of_added(bigest_subtrees,subtree):
                    bigest_subtrees.append(subtree)

        return bigest_subtrees


