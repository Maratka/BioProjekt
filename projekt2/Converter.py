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

        return  leafs




