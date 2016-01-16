__author__ = 'Gosia'

class Comparer:

    #Por�wnanie, czy dwa klastry s� te same
    def are_the_same(self, cluster_1, cluster_2):

        # Je�eli ich Taxony nie s� None, to na pewno nie por�wnujemy w�z��w
        if cluster_1.taxon is not None and cluster_2.taxon is not None:
            #Je�eli dwa li�cie nie maj� takich samych taxon�w, to nie s� takie same
            if cluster_1.taxon.label is not cluster_2.taxon.label:
                return False
            else:
                return True
        elif cluster_1.taxon is None and cluster_2.taxon is None:
            #Je�eli ich taxony s� None to s� to w�z�y
            #Je�eli listy li�ci klastr�w maj� r�ne d�ugo�ci, to na pewno nie s� te same
            if len(cluster_1.clusters) is not len(cluster_2.clusters):
                return False

            #Por�wnanie listy li�ci jednego klastra i drugiego
            #Je�eli s� zgodne to s� takie same
            #Inaczej klastry s� r�ne
            found_in_other = 0
            expected_found = len(cluster_1.clusters)

            for cluster_from_list_1 in cluster_1.clusters:
                for cluster_from_list_2 in cluster_2.clusters:
                    if cluster_from_list_1.taxon.label is cluster_from_list_2.taxon.label:
                        found_in_other += 1;

            if found_in_other is expected_found:
                return True
        #Jezeli jeden jest w�z�em, a drugi li�ciem, to na pewno nie s� te same
        return False

    def is_cluster_included_in_another(self, included_cluster, cluster):
        """Czy klaster zawiera sie w drugim? Jezeli sa liscmi to sprawdz taxony.
        Jezli tylko jeden ten, ktory ma sie zawierac jest liscie to poszukaj jego w drugim.
        Jezeli tylko ten drugi jest lisciem to nie.
        Jezeli zawieraja wiele lisci to poszukaj wszystkie elementy pierwszego w drugim
        """
        if included_cluster.taxon and cluster.taxon:
            if included_cluster.taxon.label == cluster.taxon.label:
                return True
            else:
                return False
        elif included_cluster.taxon and not cluster.taxon:
            for leaf in cluster.clusters:
                if leaf.taxon.label == included_cluster.taxon.label:
                    return True
            return False
        elif not included_cluster.taxon and cluster.taxon:
            return False

        for included_leaf in included_cluster.clusters:
            found_leaf = False
            for leaf in cluster.clusters:
                if included_leaf.taxon.label == leaf.taxon.label:
                    found_leaf = True
                    break
            if not found_leaf:
                return False
        return True

    def have_clusters_common_elements(self, first_cluster, second_cluster):
        """Czy klastry maja wspolne elementy? Jezeli sa liscmi to porownaj taxony
        Jezeli tylko jeden jest lisciem to poszukaj tego liscia w drugim. Jezeli zawieraja wiele lisci
        to poszukaj jakiegokolwiek z pierwszego w drugim
        """
        if first_cluster.taxon and second_cluster.taxon:
            if first_cluster.taxon.label == second_cluster.taxon.label:
                return True
            else:
                return False
        elif not first_cluster.taxon and second_cluster.taxon:
            for first_leaf in first_cluster.clusters:
                if second_cluster.taxon.label == first_leaf.taxon.label:
                    return True
            return False
        elif first_cluster.taxon and not second_cluster.taxon:
            for second_leaf in second_cluster.clusters:
                if first_cluster.taxon.label == second_leaf.taxon.label:
                    return True
            return False

        for first_leaf in first_cluster.clusters:
            for second_leaf in second_cluster.clusters:
                if first_leaf.taxon.label == second_leaf.taxon.label:
                    return True
        return False

