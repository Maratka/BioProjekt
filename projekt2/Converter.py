from dendropy import Tree, Node

__author__ = 'Gosia'
from Cluster import Cluster

class Converter:

    #Metoda zwracaj�ca list� klastr�w dla drzewa
    def get_cluster_list(self,tree):
        return self.prepare_cluster_list_for_node(tree.seed_node)

    #Przygotowanie listy klastr�w, jako reprezanetacji drzewa - rekurancja
    def prepare_cluster_list_for_node(self, node):
        cluster_list = []
        #Je�eli element drzewa jest li�ciem, to do listy klastr�w dodajemy klaster, kt�ry ma nazw� tego li�cia - taxon i tego liscia w �rodku
        if node.is_leaf():
            taxon = node.taxon
            cluster = Cluster(taxon, node)
            cluster_list.append(cluster)
        else:
            #Je�eli dany w�ze� drzewa jest w�z�em, to do listy dodawany jest klaster z brakiem nazwy - taxon, a lista to lista wszystkich li�ci, do kt�rych mo�na od niego doj��
            leafs = node.leaf_nodes()
            taxon = node.taxon
            cluster = Cluster(taxon,leafs)
            childs = node.child_nodes()
            cluster_list.append(cluster)
            #Nast�pnie dla ka�dego jego dziecka wykonywana jest ta sama funkcja
            for child in childs:
                child_cluster = self.prepare_cluster_list_for_node(child)
                cluster_list += child_cluster

        #Na koniec zwracana jest lista klastr�w
        return cluster_list

    #Konwersja drzewa z�o�onego z klastr�w na drzewo grafowe
    def get_dendropy_tree(self, cluster_tree):

        consensus_tree_dendropy =  Tree()
        #Rozr�nienie li�ci od w�z��w i zapisanie ich do dw�ch osobnych tablic
        leafs = []
        nodes = []
        for cluster in cluster_tree.get_cluster_list():
            if cluster.taxon is not None:
                leafs.append(cluster)
            if cluster.taxon is None:
                nodes.append(cluster)
        #Posortowanie listy w�z��w po to, aby zacz�� przeszukiwa� je od tych, kt�re maj� najmniej li�ci i budowa� drzewo od do�u
        nodes.sort(key=lambda x: len(x.clusters))
        #Tablica tymczasowych utworzonych ju� w�z��w, z kt�rych budowane jest drzewo
        created_nodes = []
        for node in nodes:

            #Dla ka�ego znalezionego w�z�a, tworzony jest w�ze� drzewa
            # a nast�pnie dodawane s� do niego jego li�cie

            created_node = Node()
            for leaf in node.clusters:
                #Je�eli jego li�ci nie jest na li�cie lisci, oznacza to, �e zosta� ju� wcze�niej zu�yty
                #Czyli znajduje si� ju� w tymczasowym w�le i nale�y jako dziecko doda� ten tymczasowy w�ze�
                if not self.is_leaf_in_leafs(leaf,leafs):
                    # Nale�y znale�� stworzony w�ze� z li�ciem i doda� go jako dziecko do nowego w�z�a
                    # A zu�yty w�ze� usun��
                    sub_created_node, created_nodes = self.find_created_node_with_leaf(created_nodes, leaf)
                    if sub_created_node is not None:
                        created_node.add_child(sub_created_node)
                else:
                    #je�eli li�c nie zosta� jeszcze zu�yty, to nale�y go doda� jako dziecko w�z�a
                    # i usun�� z listy li�ci
                    created_node.add_child(leaf)
                    leafs = self.remove_leaf_from_list(leaf,leafs)

            created_nodes.append(created_node)

        # Finalnie, w�ze� ze wszystkimi li�ciami oraz w�z�ami b�dzie na pierwszym i jedynym miejscu w li�cie tymczasowych
        tree = Tree(seed_node=created_nodes[0])
        return tree

    #Wyszukanie w li�cie tymczasowych w�z��w drzewa wez�a, kt�re zawiera szukany lis�
    #A nast�pnie usuni�cie tego w�z�a z listy tymczasowych w�z��w poniewa� zosta� on ju� zu�yty
    def find_created_node_with_leaf(self, created_nodes, leaf):

        for created_node in created_nodes:
            for leaf_of_creaded_node in created_node.leaf_nodes():
                if leaf_of_creaded_node.taxon.label is leaf.taxon.label:
                    created_nodes.remove(created_node)
                    return created_node, created_nodes

        return None, created_nodes

    #Sprawdzenie czy li�� znajduje si� na li�ci li�ci
    def is_leaf_in_leafs(self, leaf, leafs):

        for leaf_tmp in leafs:
            if leaf_tmp.taxon.label is leaf.taxon.label:
                return True

        return False

    #Usuniecie li�cia z listy li�ci i zwr�cenie tej listy
    def remove_leaf_from_list(self,leaf,leafs):

        for leaf_in_list in leafs:
            if leaf_in_list.taxon.label is leaf.taxon.label:
                leafs.remove(leaf_in_list)

        return leafs

    def get_dendropy_tree_from_break_tree(self, break_tree):
        nodes = self._extract_break_tree_leaves(break_tree)
        sorted_break_tree_leaves_sets, max_leaves_set_size = self._sort_break_tree_leaves_sets(break_tree)

        for leave_set_size in range(max_leaves_set_size):
            if leave_set_size not in sorted_break_tree_leaves_sets:
                continue

            for leave_set in sorted_break_tree_leaves_sets[leave_set_size]:
                one_step_parents = []
                for leaf in leave_set:
                    node = self._find_node_with_same_taxon(nodes, leaf)
                    oldest_parent = self._get_oldest_parent(node)
                    if oldest_parent not in one_step_parents:
                        one_step_parents.append(oldest_parent)

                new_oldest_parent = Node()
                if len(one_step_parents) > 1:
                    for parent in one_step_parents:
                        parent.parent_node = new_oldest_parent

        oldest_parents = []
        for node in nodes:
            oldest_parent = self._get_oldest_parent(node)
            if oldest_parent not in oldest_parents:
                oldest_parents.append(oldest_parent)

        if len(oldest_parents) > 1:
            seed = Node()
            for oldest_parent in oldest_parents:
                oldest_parent.parent_node = seed
        elif len(oldest_parents) == 1:
            seed = oldest_parents[0]
        else:
            seed = Node()

        tree = Tree(seed_node=seed)
        tree.deroot()
        return tree

    def _extract_break_tree_leaves(self, break_tree):
        leaves = []
        tree_break_parts_to_remove = []
        for tree_break_part in break_tree.tree_break_parts:
            break_part_to_remove = False
            if len(tree_break_part.leaves_set_a) == 1:
                cloned_leaves = self._clone_and_detach_leaves_set(tree_break_part.leaves_set_a)
                leaves.append(cloned_leaves[0])
                break_part_to_remove = True
            if len(tree_break_part.leaves_set_b) == 1:
                cloned_leaves = self._clone_and_detach_leaves_set(tree_break_part.leaves_set_b)
                leaves.append(cloned_leaves[0])
                break_part_to_remove = True
            if break_part_to_remove:
                tree_break_parts_to_remove.append(tree_break_part)

        for tree_break_part_to_remove in tree_break_parts_to_remove:
            break_tree.tree_break_parts.remove(tree_break_part_to_remove)

        return leaves

    def _clone_and_detach_leaves_set(self, leaves_set):
        cloned_leaves_set = []
        for leaf in leaves_set:
            cloned_leaf = leaf.clone(2)
            cloned_leaf.parent_node = None
            # cloned_leaf._set_parent_node(None)
            cloned_leaves_set.append(cloned_leaf)
        return cloned_leaves_set

    def _sort_break_tree_leaves_sets(self, break_tree):
        sorted_break_tree_leaves_sets = {}
        max_leaves_set_size = 0
        for tree_break_part in break_tree.tree_break_parts:
            leaves_set_a_size = len(tree_break_part.leaves_set_a)
            leaves_set_b_size = len(tree_break_part.leaves_set_b)

            if leaves_set_a_size > max_leaves_set_size:
                max_leaves_set_size = leaves_set_a_size
            if leaves_set_b_size > max_leaves_set_size:
                max_leaves_set_size = leaves_set_b_size

            if leaves_set_a_size not in sorted_break_tree_leaves_sets:
                sorted_break_tree_leaves_sets[leaves_set_a_size] = []
            sorted_break_tree_leaves_sets[leaves_set_a_size].append(self._clone_and_detach_leaves_set(tree_break_part.leaves_set_a))
            if leaves_set_b_size not in sorted_break_tree_leaves_sets:
                sorted_break_tree_leaves_sets[leaves_set_b_size] = []
            sorted_break_tree_leaves_sets[leaves_set_b_size].append(self._clone_and_detach_leaves_set(tree_break_part.leaves_set_b))
        return sorted_break_tree_leaves_sets, max_leaves_set_size

    def _get_oldest_parent(self, node):
        if node.parent_node is None:
            return node
        return self._get_oldest_parent(node.parent_node)

    def _find_node_with_same_taxon(self, nodes, wanted_node):
        for node in nodes:
            if node.taxon.label == wanted_node.taxon.label:
                return node







