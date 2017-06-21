""" Base class for dynamic graphs.

"""
import networkx as nx

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
        edgelist : 4-tuple (u,v, start_time, end_time) indicating an edge
            between node u, node v, begining at start_time, and finishing at 
            end_time
        name : string, optional (default='')
            An optional name for the graph.
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

    def nodes(self):
        return self.nodes

    def edges(self):
        return self.start_edges

    def add_node(self, n, **attr):
        """ Adds node n to the Dynamic Graph
        """
        if n not in self.nodes:
            self.nodes[n] = attr
            self.adj[n] = {}
        else:
            self.nodes.update(attr)

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
            self.nodes[u] = {}
        if  v not in self.nodes:
            self.nodes[v] = {}

        if u not in self.nodes[v]:
            edge_list = []
            self.nodes[u][v] = edge_list
            self.nodes[v][u] = edge_list

        dynamic_edge = DynamicEdge(start_time, end_time, attrs)

        self.adj[u][v].append(dynamic_edge)
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
