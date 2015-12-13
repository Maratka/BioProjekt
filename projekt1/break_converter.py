from projekt1.break_tree import BreakTree
from projekt1.tree_break_part import TreeBreakPart


class BreakConverter(object):

    @staticmethod
    def tree_to_break_tree(tree):
        seed_node = tree.seed_node
        break_tree_parts = []

        for edge in tree.levelorder_edge_iter():
            leaves_set_a = []
            leaves_set_b = []
            head_node = edge.head_node
            if head_node.parent_node is None:
                continue
            for leaf in head_node.leaf_nodes():
                leaves_set_a.append(leaf)

            for leaf in seed_node.leaf_nodes():
                if leaf not in leaves_set_a:
                    leaves_set_b.append(leaf)

            break_tree_parts.append(TreeBreakPart(leaves_set_a, leaves_set_b))
        return BreakTree(break_tree_parts)

