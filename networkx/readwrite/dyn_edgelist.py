from __future__ import print_function
'''
    File Name: dyn_edgelist.py
    Author: Brian O'Leary
    Date Created: 2017-06-20
    Date Last Modified:
'''
import networkx as nx
from networkx.classes.dynamicgraph import DynamicGraph

def read_edgelist(filename):
    G = DynamicGraph()
    with open(filename, 'r') as r:
        # operating under the assumption that there is a triplet
        # with all integers
        for line in r.readlines():
            items = line.strip().split(',')
            u = int(items[0])
            v = int(items[1])
            start_time = int(items[2])
            if len(items) == 3:
                end_time = start_time
            else:
                end_time = items[3]

            G.add_edge(u, v, start_time, end_time)
    G.sort_edges()
    return G

if __name__ == '__main__':
    G = read_edgelist('../../datasets/RealityMiningCallSmsDataUnsorted.csv')
    print('helo')
