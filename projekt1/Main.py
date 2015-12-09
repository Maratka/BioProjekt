import dendropy

tree1 = dendropy.Tree.get(
        path="../tree.txt",
        schema="newick")

tree1.print_plot()
