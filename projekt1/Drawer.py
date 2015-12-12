__author__ = 'Gosia'

class Drawer:

    def drawTree(self, tree):
        """
        :param tree - drzewo z dendropy
        :return:
        """
        #leavesNumber = len(tree.leaf_edges())
        #width = leavesNumber * 2 - 1
        self.__drawNode(tree.seed_node, 0, [], "MID", "")


    def __drawNode(self, node, depth, edges, nodeType, side):
        INDENT = 4

        children = node.child_nodes()
        childrenNumber = len(children)

        if childrenNumber != 0 and depth != 0 and side == "L" and (depth not in edges):
            edges.append(depth)

        for i in range(0, (int)(childrenNumber/2), 1):
            type = "MID"
            if i == 0:
                type = "FIRST"
            self.__drawNode(children[i], depth+1, edges, type, "R")


        if (side == "L") and (depth in edges) and (nodeType == "LAST"):
            edges.remove(depth)

        sign = "|"
        if nodeType == "FIRST":
            sign = "/"
        elif nodeType == "LAST":
            sign = "\\"
        elif (depth in edges):
            sign = ""


        currentIndent = 0
        sorted(edges, key=int)
        for i in range(len(edges)):
            print(" " * (edges[i] * INDENT - currentIndent), end="|")
            currentIndent = edges[i] * INDENT + 1

        print(" " * (depth * INDENT - currentIndent), end=sign)
        print("-" * (INDENT-1), end="")

        if node.taxon:
            print(str(node.taxon).replace('\'', ""))
        elif node.label:
            print(node.label)
        else:
            print("+")


        if childrenNumber != 0 and depth != 0 and side == "R" and (depth not in edges):
            edges.append(depth)

        for i in range((int)(childrenNumber/2), childrenNumber, 1):
            type = "MID"
            if i == childrenNumber - 1:
                type = "LAST"
            self.__drawNode(children[i], depth+1, edges, type, "L")

        if (side == "R") and (depth in edges):
            edges.remove(depth)
