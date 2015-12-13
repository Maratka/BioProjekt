__author__ = 'Gosia'

class Comparer:

    def are_the_same(self, cluster_1, cluster_2):

        if cluster_1.taxon is not None and cluster_2.taxon is not None:
            if cluster_1.taxon.label is not cluster_2.taxon.label:
                return False
            else:
                return True
        elif cluster_1.taxon is None and cluster_2.taxon is None:

            if len(cluster_1.clusters) is not len(cluster_2.clusters):
                return False

            found_in_other = 0
            expected_found = len(cluster_1.clusters)

            for cluster_from_list_1 in cluster_1.clusters:
                for cluster_from_list_2 in cluster_2.clusters:
                    if cluster_from_list_1.taxon.label is cluster_from_list_2.taxon.label:
                        found_in_other += 1;

            if found_in_other is expected_found:
                return True

        return False