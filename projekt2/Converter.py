from dendropy import Tree, Node

__author__ = 'Gosia'
from Cluster import Cluster

class Converter:

    #Metoda zwracaj¹ca listê klastrów dla drzewa
    def get_cluster_list(self,tree):
        return self.prepare_cluster_list_for_node(tree.seed_node)

    #Przygotowanie listy klastrów, jako reprezanetacji drzewa - rekurancja
    def prepare_cluster_list_for_node(self, node):
        cluster_list = []
        #Je¿eli element drzewa jest liœciem, to do listy klastrów dodajemy klaster, który ma nazwê tego liœcia - taxon i tego liscia w œrodku
        if node.is_leaf():
            taxon = node.taxon
            cluster = Cluster(taxon, node)
            cluster_list.append(cluster)
        else:
            #Je¿eli dany wêze³ drzewa jest wêz³em, to do listy dodawany jest klaster z brakiem nazwy - taxon, a lista to lista wszystkich liœci, do których mo¿na od niego dojœæ
            leafs = node.leaf_nodes()
            taxon = node.taxon
            cluster = Cluster(taxon,leafs)
            childs = node.child_nodes()
            cluster_list.append(cluster)
            #Nastêpnie dla ka¿dego jego dziecka wykonywana jest ta sama funkcja
            for child in childs:
                child_cluster = self.prepare_cluster_list_for_node(child)
                cluster_list += child_cluster

        #Na koniec zwracana jest lista klastrów
        return cluster_list

    #Konwersja drzewa z³o¿onego z klastrów na drzewo grafowe
    def get_dendropy_tree(self, cluster_tree):

        consensus_tree_dendropy =  Tree()
        #Rozró¿nienie liœci od wêz³ów i zapisanie ich do dwóch osobnych tablic
        leafs = []
        nodes = []
        for cluster in cluster_tree.get_cluster_list():
            if cluster.taxon is not None:
                leafs.append(cluster)
            if cluster.taxon is None:
                nodes.append(cluster)
        #Posortowanie listy wêz³ów po to, aby zacz¹æ przeszukiwaæ je od tych, które maj¹ najmniej liœci i budowaæ drzewo od do³u
        nodes.sort(key=lambda x: len(x.clusters))
        #Tablica tymczasowych utworzonych ju¿ wêz³ów, z których budowane jest drzewo
        created_nodes = []
        for node in nodes:

            #Dla ka¿ego znalezionego wêz³a, tworzony jest wêze³ drzewa
            # a nastêpnie dodawane s¹ do niego jego liœcie

            created_node = Node()
            for leaf in node.clusters:
                #Je¿eli jego liœci nie jest na liœcie lisci, oznacza to, ¿e zosta³ ju¿ wczeœniej zu¿yty
                #Czyli znajduje siê ju¿ w tymczasowym wêŸle i nale¿y jako dziecko dodaæ ten tymczasowy wêze³
                if not self.is_leaf_in_leafs(leaf,leafs):
                    # Nale¿y znaleŸæ stworzony wêze³ z liœciem i dodaæ go jako dziecko do nowego wêz³a
                    # A zu¿yty wêze³ usun¹æ
                    sub_created_node, created_nodes = self.find_created_node_with_leaf(created_nodes, leaf)
                    if sub_created_node is not None:
                        created_node.add_child(sub_created_node)
                else:
                    #je¿eli liœc nie zosta³ jeszcze zu¿yty, to nale¿y go dodaæ jako dziecko wêz³a
                    # i usun¹æ z listy liœci
                    created_node.add_child(leaf)
                    leafs = self.remove_leaf_from_list(leaf,leafs)

            created_nodes.append(created_node)

        # Finalnie, wêze³ ze wszystkimi liœciami oraz wêz³ami bêdzie na pierwszym i jedynym miejscu w liœcie tymczasowych
        tree = Tree(seed_node=created_nodes[0])
        return tree

    #Wyszukanie w liœcie tymczasowych wêz³ów drzewa wez³a, które zawiera szukany lisæ
    #A nastêpnie usuniêcie tego wêz³a z listy tymczasowych wêz³ów poniewa¿ zosta³ on ju¿ zu¿yty
    def find_created_node_with_leaf(self, created_nodes, leaf):

        for created_node in created_nodes:
            for leaf_of_creaded_node in created_node.leaf_nodes():
                if leaf_of_creaded_node.taxon.label is leaf.taxon.label:
                    created_nodes.remove(created_node)
                    return created_node, created_nodes

        return None, created_nodes

    #Sprawdzenie czy liœæ znajduje siê na liœci liœci
    def is_leaf_in_leafs(self, leaf, leafs):

        for leaf_tmp in leafs:
            if leaf_tmp.taxon.label is leaf.taxon.label:
                return True

        return False

    #Usuniecie liœcia z listy liœci i zwrócenie tej listy
    def remove_leaf_from_list(self,leaf,leafs):

        for leaf_in_list in leafs:
            if leaf_in_list.taxon.label is leaf.taxon.label:
                leafs.remove(leaf_in_list)

        return  leafs




