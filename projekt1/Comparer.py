__author__ = 'Gosia'

class Comparer:

    #Porównanie, czy dwa klastry s¹ te same
    def are_the_same(self, cluster_1, cluster_2):

        # Je¿eli ich Taxony nie s¹ None, to na pewno nie porównujemy wêz³ów
        if cluster_1.taxon is not None and cluster_2.taxon is not None:
            #Je¿eli dwa liœcie nie maj¹ takich samych taxonów, to nie s¹ takie same
            if cluster_1.taxon.label is not cluster_2.taxon.label:
                return False
            else:
                return True
        elif cluster_1.taxon is None and cluster_2.taxon is None:
            #Je¿eli ich taxony s¹ None to s¹ to wêz³y
            #Je¿eli listy liœci klastrów maj¹ ró¿ne d³ugoœci, to na pewno nie s¹ te same
            if len(cluster_1.clusters) is not len(cluster_2.clusters):
                return False

            #Porównanie listy liœci jednego klastra i drugiego
            #Je¿eli s¹ zgodne to s¹ takie same
            #Inaczej klastry s¹ ró¿ne
            found_in_other = 0
            expected_found = len(cluster_1.clusters)

            for cluster_from_list_1 in cluster_1.clusters:
                for cluster_from_list_2 in cluster_2.clusters:
                    if cluster_from_list_1.taxon.label is cluster_from_list_2.taxon.label:
                        found_in_other += 1;

            if found_in_other is expected_found:
                return True
        #Jezeli jeden jest wêz³em, a drugi liœciem, to na pewno nie s¹ te same
        return False