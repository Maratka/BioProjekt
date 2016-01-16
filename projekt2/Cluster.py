__author__ = 'Gosia'

class Cluster:

     def __init__(self, taxon, clusters):
         self.taxon = taxon
         #Lista lisci
         self.clusters = clusters
         #Ile razy wystêpuje w zbiorze drzew dany klaster
         self.found = 1