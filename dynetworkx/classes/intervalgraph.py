from networkx.classes.graph import Graph
from networkx.exception import NetworkXError
from intervaltree import Interval, IntervalTree


class IntervalGraph(object):
    def __init__(self, **attr):
        self.tree = IntervalTree()
        # self.graph.update(attr)
        # self.snapshots = []

    def add_edge(self, u_of_edge, v_of_edge, begin, end, **attr):
        iv_edge = Interval(begin, end, (u_of_edge, v_of_edge))

        try:
            self.tree.add(iv_edge)
        except ValueError:
            raise NetworkXError("IntervalGraph: edge duration must be strictly bigger than zero {0}.".format(iv_edge))


    def add_edges_from(self, ebunch_to_add, **attr):
        # (from, to, begin, end)
        for e in ebunch_to_add:
            if len(e) != 4:
                raise NetworkXError("Edge tuple {0} must be a 4-tuple.".format(e))

            self.add_edge(e[0], e[1], e[2], e[3])

    # def subgraph(self):
    #     g = Graph()
    #

    @staticmethod
    def load_from_txt(path, delimiter=" ", nodetype=None, comments="#"):
        """Read interval graph in from path.
           Every line in the file must be an edge in the following format: "node, node, begin, end".
           Both times must be integers.
        Parameters
        ----------
        path : string or file
           Filename to read.

        nodetype : Python type, optional
           Convert nodes to this type.

        comments : string, optional
           Marker for comment lines

        delimiter : string, optional
           Separator for node labels.  The default is whitespace.

        Returns
        -------
        IG: DyNetworkX IntervalGraph
            The graph corresponding to the lines in edge list.

        Examples
        --------
        >>> G=nx.path_graph(4)
        >>> nx.write_adjlist(G, "test.adjlist")
        >>> G=nx.read_adjlist("test.adjlist")

        The path can be a filehandle or a string with the name of the file. If a
        filehandle is provided, it has to be opened in 'rb' mode.

        >>> fh=open("test.adjlist", 'rb')
        >>> G=nx.read_adjlist(fh)

        Filenames ending in .gz or .bz2 will be compressed.

        >>> nx.write_adjlist(G,"test.adjlist.gz")
        >>> G=nx.read_adjlist("test.adjlist.gz")

        The optional nodetype is a function to convert node strings to nodetype.

        For example

        >>> G=nx.read_adjlist("test.adjlist", nodetype=int)

        will attempt to convert all nodes to integer type.

        Since nodes must be hashable, the function nodetype must return hashable
        types (e.g. int, float, str, frozenset - or tuples of those, etc.)

        Notes
        -----
        This format does not store graph or node data.
        Both times must be integers.
        """

        ig = IntervalGraph()

        with open(path, 'r') as file:
            for line in file:
                p = line.find(comments)
                if p >= 0:
                    line = line[:p]
                if not len(line):
                    continue

                line = line.rstrip().split(delimiter)
                u, v, begin, end = line
                if nodetype is not None:
                    try:
                        u = nodetype(u)
                        v = nodetype(v)
                    except:
                        raise TypeError("Failed to convert node to type {0}".format(nodetype))

                try:
                    begin = int(begin)
                    end = nodetype(end)
                except:
                    raise TypeError("Failed to convert time to type int")

                ig.add_edge(u, v, begin, end)

        return ig