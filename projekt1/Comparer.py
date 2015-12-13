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