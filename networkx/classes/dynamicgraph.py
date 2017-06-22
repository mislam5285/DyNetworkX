""" Base class for dynamic graphs.

"""
import networkx as nx
from networkx.classes.dynamic_edge import DynamicEdge

class DynamicGraph(object):

    """ To follow existing convention, we'll assign a variable function for
        the creation of nodes and edges.  Currently we'll only allow the 
        default value of dict, but future expansions should allow the use of  
        custom dict-like objecdts
    """
    def __init__(self, **attr):
        """ Initialize a continuous dynamic graph with edges, name, and graph attributes.

        Parameters
        ----------
        attr : keyword arguments, optional (default= no attributes)
            Attributes to add to graph as key=value pairs.
        """
        # Sorted edge lists
        self.start_edges = []
        self.end_edges   = []

        self.graph = {} # graph attributes
        self.graph.update(attr)

        self.nodes = {} # Nodes in graph
        self.adj   = {} # adjacency dict

    def __str__(self):
        if 'name' in self.graph:
            return self.graph['name']
        return self.__hash__()

    def __contains__(self, n):
        pass

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.start_edges

    def add_node(self, n, **attr):
        """ Adds node n to the Dynamic Graph
        """
        if n not in self.nodes:
            self.nodes[n] = attr
            self.adj[n] = {}
        else:
            self.nodes.update(attr)

    def sort_edges(self):
        self.start_edges.sort(key=lambda x: x.start_time)
        self.end_edges.sort(key=lambda x: x.end_time)


    def add_edge(self, u, v, start_time, end_time, **attrs):
        """ Creates an undirected edge between node u and node v,
            begining at start_time and finishing at end_time

            Parameters
            ----------
            u: node from
            v: node to
            start_time: time the edge first appears 
            end_time: time the edge is no longer present
        """
        if u not in self.nodes:
            self.add_node(u)
        if  v not in self.nodes:
            self.add_node(v)

        if u not in self.adj[v]:
            edge_list = []
            self.adj[u][v] = edge_list
            self.adj[v][u] = edge_list

        dynamic_edge = DynamicEdge(start_time, end_time, attrs)

        self.adj[u][v].append(dynamic_edge)
        self.adj[v][u].append(dynamic_edge)
        self.start_edges.append(dynamic_edge) 
        self.end_edges.append(dynamic_edge) 


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
