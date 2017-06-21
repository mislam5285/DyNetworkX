'''
    File Name: dyn_edgelist.py
    Author: Brian O'Leary
    Date Created: 2017-06-20
    Date Last Modified:
'''
import networkx as nx
from networkx.classes.dynamicgraph import DynamicGraph

def read_edgelist(filename, _type='discrete'):
    G = DynamicGraph()
    with open(filename, 'r') as r:
        for line in r.readlines():
            print line

if __name__ == '__main__':
    print 'ehlo'
    read_edgelist('../../datasets/RealityMiningCallSmsDataUnsorted.csv')

