""" Base class for dynamic graphs.

"""
import networkx as nx

class DynamicGraph(object):

    def __init__(self, edgelist, **attr):
        """ Initialize a continuous dynamic graph with edges, name, and graph attributes.

        Parameters
        ----------
        edgelist : 4-tuple (u,v, start_time, end_time) indicating an edge
            between node u, node v, begining at start_time, and finishing at 
            end_time
        name : string, optional (default='')
            An optional name for the graph.
        attr : keyword arguments, optional (default= no attributes)
            Attributes to add to graph as key=value pairs.
        """
        pass

    def __str__(self):
        pass

    def __contains__(self, n):
        pass

    def add_node(self, n, **attr):
        """ Adds node n to the Dynamic Graph
        """
        pass

    def add_edge(self, u, v, start_time, end_time):
        """ Creates an undirected edge between node u and node v,
            begining at start_time and finishing at end_time
        """
        pass

    def timestamp_filter(self, start_time, end_time):
        """ Creates a static graph of all nodes and edges that exist between
            start_time and end_time
        """
        pass

    def node_filter(self, nbunch):
        """ Creates a dynamic subgraph consisting of only nodges and edges that
            are in nbunch
        """
        pass

    def coarsen(self, node_dict):
        """ Returns a dynamic graph where multiple nodes have been combined 
            together into a supernode

            Parameters
            ----------
            node_dict: A mapping of supernodes to list of nodes
                {
                    supernode_0: [1, ..., i],
                    ...
                    supernode_n: [1, ..., j],
                }
        """
        pass
    
    def to_snapshots(self, number_of_snapshots):
        """ Returns number_of_snapshots snapshots
        """
        pass
