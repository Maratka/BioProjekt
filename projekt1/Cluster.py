__author__ = 'Gosia'

class Cluster:

     def __init__(self, taxon, clusters):
         self.taxon = taxon
         #Lista lisci
         self.clusters = clusters
         #Ile razy wyst�puje w zbiorze drzew dany klaster
         self.found = 1