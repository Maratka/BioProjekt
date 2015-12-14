from projekt1.consensus_tree_file import find_consensus_tree


class CommonExtend(object):

    def get_common_extend(self, trees):
        """Wspolne rozszerzenie bedace suma wszystkich klastrow dla wszystkich drzew"""
        return find_consensus_tree(trees, 0)
