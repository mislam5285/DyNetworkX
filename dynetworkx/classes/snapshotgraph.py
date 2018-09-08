from networkx.classes.graph import Graph

class SnapshotGraph(object):
    def __init__(self, **attr):
        self.graph = {}
        self.graph.update(attr)
        self.snapshots = []
        self.total_snapshots = 0

    def __len__(self):
        return self.total_snapshots

    def generator(self, start, end):
        """
        Generator used for producing lists of snapshots in a memory efficient way.

        Parameters
        ----------
        start : Inclusive index of first desired graph
        end : Non-inclusive ending index of graph

        Yields
        -------
        NetworkX graph object for current index in snapshot graph

        """
        snaps_traveled = 0
        snaps = 0

        while snaps < len(self.snapshots):
            iters = 0
            # if the snaps traveled plus the current snapshot is less than start
            # just get the length of the compressed snapshot, and keep moving
            # - Reduces time complexity to O(len(snapshots))

            if snaps_traveled + self.snapshots[snaps][1] < start:
                snaps_traveled += self.snapshots[snaps][1]
                snaps += 1
            else:
                while iters < self.snapshots[snaps][1]:
                    if (snaps_traveled < end) and (snaps_traveled >= start):
                        yield self.snapshots[snaps][0]
                    snaps_traveled += 1

                    if snaps_traveled >= end:
                        return
                    iters += 1
                snaps += 1

    def check_equality(self, g1, g2):
        """
        Custom equality check between two graphs based on attributes,
        edge objects and node objects.

        Parameters
        ----------
        g1: networkx graph object
        g2: networkx graph object

        Returns
        -------

        """
        return (g1._adj == g2._adj) and (g1.edges == g2.edges) and (g1.nodes == g2.nodes)

    def insert(self, g_to_insert, snap_len=None, num_in_seq=None):
        """
        Insert a graph into the snapshotgraph at a given index, with some snapshot length.

        Parameters
        ----------
        g_to_insert: networkx graph object
            networkx graph to be inserted into snapshot graph.
        snap_len: Integer
            Length of the snapshot.
        num_in_seq: Integer
            Time slot to begin insertion at.


        Returns
        -------
        None

        """
        snaps_traveled = 0
        snaps = 0

        while snaps < len(self.snapshots):
            # if next snap length + total traveled thus far is less than slot needed,
            # then just keep moving
            if snaps_traveled + self.snapshots[snaps][1] < num_in_seq:
                snaps_traveled += self.snapshots[snaps][1]
                snaps += 1

            elif snaps_traveled + self.snapshots[snaps][1] == num_in_seq:
                self.snapshots.insert(snaps + 1, (g_to_insert, snap_len))

            else:
                iters = (num_in_seq - snaps_traveled)
                snap_to_split = self.snapshots[snaps]
                # change to first part of snap
                self.snapshots[snaps] = (snap_to_split[0], iters)
                # insert new snap
                self.snapshots.insert(snaps + 1, (g_to_insert, snap_len))
                # insert second part
                self.snapshots.insert(snaps + 2, (snap_to_split[0], snap_to_split[1] - iters))

                self.total_snapshots += snap_len
                return

            snaps += 1

    def add_snapshot(self, ebunch, num_in_seq=None, weight='weight', **attr):
        """
        Add a snapshot with a bunch of edge values.

        Parameters
        ----------
        ebunch : List of edges to include in time slot of snapshot graph

        Returns
        -------
        None

        """
        # add snapshot assumes appendng to end, shoudl I combline with insert method? probs, but also need insert method
        g = Graph()
        g.add_weighted_edges_from(ebunch)

        if (not num_in_seq) or (num_in_seq == self.total_snapshots + 1):
            # compress graph
            if self.snapshots and self.check_equality(g, self.snapshots[len(self.snapshots) - 1][0]):
                last_snap_tup = self.snapshots[len(self.snapshots) - 1]
                self.snapshots[len(self.snapshots) - 1] = (last_snap_tup[0], last_snap_tup[1] + 1)
            else:
                self.snapshots.append((g, 1))
            # add one to the length
            self.total_snapshots += 1

        elif num_in_seq > self.total_snapshots:
            # add difference to graph's length
            last_snap_tup = self.snapshots[len(self.snapshots) - 1]
            self.snapshots[len(self.snapshots) - 1] = (last_snap_tup[0],
                                                       last_snap_tup[1] + num_in_seq - self.total_snapshots - 1)

            # add in new snapshot
            self.snapshots.append((g, 1))

            # add difference to the length
            self.total_snapshots += (num_in_seq - self.total_snapshots)
        else:
            self.insert(g, snap_len=1, num_in_seq=num_in_seq)

    def subgraph(self, nbunch=None, sbunch=None):
        """
        Nodes is a list of nodes that should be found in each subgraph

        Parameters
        ----------
        sbunch : List of indexes for snapshots you are interested in.
        nbunch : List of nodes you are interested in.

        Returns
        -------
            List of tuples containing the degrees of each node in each snapshot.
        """

        min_index = min(sbunch)
        max_index = max(sbunch)

        #if len(nodes) != self.total_snapshots:
        #    raise ValueError('node list({}) must be equal in length to number of desired snapshots({})'.format(len(nodes), max_index - min_index))

        snapshot_graphs = list(self.generator(min_index, max_index))
        subgraph = SnapshotGraph()

        if (len(nbunch) == 1) and (max_index - min_index) > 1:
            for snapshot in snapshot_graphs:
                subgraph.add_snapshot(snapshot.subgraph(nbunch))

        else:
            for snapshot, node_list in zip(snapshot_graphs, nbunch):
                subgraph.add_snapshot(snapshot.subgraph(node_list))
            #subgraph.graph = self.graph
        return subgraph

    def degree(self, sbunch=None, nbunch=None, weight=None):
        """
        Return a list of tuples containing the degrees of each node in each snapshot

        Parameters
        ----------
        sbunch : List of indexes for desired snapshots
            Each snapshot index in this list will be included in the returned list
            of node degrees. It is highly recommended that this list is sequential,
            however it can be out of order.
        nbunch : List of desired nodes
            Each node in the nbunch list will be included in the returned list of
            node degrees.

        Returns
        -------
            List of tuples containing the degrees of each node in each snapshot
        """
        # returns a list of degrees for each graph snapshot in snapshots
        # use generator to create list of degrees
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return_degrees = []

        for g in graph_list:
            node_list = list(g.nodes)
            for node in node_list:
                if node in nbunch:
                    return_degrees.append(node.degree(weight=weight))

        return return_degrees

    def number_of_nodes(self, sbunch=None):
        """
        Gets number of nodes in each snapshot requested in 'sbunch'.

        Parameters
        ----------
        sbunch : List of indexes for desired snapshots
            Each snapshot index in this list will be included in the returned list
            of number of nodes in the snapshot. It is highly recommended that this list is sequential,
            however it can be out of order.

        Returns
        -------

        """
        # returns a list of the number of nodes in each graph in the range
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return [g.number_of_nodes() for g in graph_list]

    def order(self, sbunch=None):
        """
        Gets order of each node requested in 'sbunch'.

        Parameters
        ----------
        sbunch : List of indexes for desired snapshots
            Each snapshot index in this list will be included in the returned list
            of node orders. It is highly recommended that this list is sequential,
            however it can be out of order.

        Returns
        -------

        """
        # returns a list of the order of the graph in the range
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return [g.order() for g in graph_list]

    def has_node(self, n, sbunch=None):
        """
        Gets boolean list of if a snapshot in 'sbunch' contains node 'n'.

        Parameters
        ----------
        n: networkx node object
            node to be checked for in requested snapshots

        sbunch : List of indexes for desired snapshots
            Each snapshot index in this list will be included in the returned list
            of if the snapshot graph includes the node. It is highly recommended
            that this list is sequential, however it can be out of order.

        Returns
        -------

        """
        # returns a list of the order of the graph in the range
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return [g.has_node(n) for g in graph_list]

    def is_multigraph(self, sbunch=None):
        """

        Parameters
        ----------
        sbunch: List of indexes for snapshots you are interested in.

        Returns
        -------

        """
        # returns a list of the order of the graph in the range
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return [g.is_multigraph() for g in graph_list]

    def is_directed(self, sbunch=None):
        """

        Parameters
        ----------
        sbunch: List of indexes for snapshots you are interested in.

        Returns
        -------

        """
        # returns a list of the order of the graph in the range
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return [g.is_directed() for g in graph_list]

    def to_directed(self, sbunch=None):
        """

        Parameters
        ----------
        sbunch: List of indexes for snapshots you are interested in.

        Returns
        -------

        """
        # returns a list of the order of the graph in the range
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return [g.to_directed() for g in graph_list]

    def to_undirected(self, sbunch=None):
        """

        Parameters
        ----------
        sbunch: List of indexes for snapshots you are interested in.

        Returns
        -------

        """
        # returns a list of the order of the graph in the range
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return [g.to_undirected() for g in graph_list]

    def size(self, sbunch=None, weight=None):
        """

        Parameters
        ----------
        sbunch: List of indexes for snapshots you are interested in.

        Parameters
        ----------
        weight

        Returns
        -------
        List of

        """
        # returns a list of the order of the graph in the range
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]

        return [g.size(weight=weight) for g in graph_list]

    def get(self, sbunch=None):
        """
        Gets all graphs in snapshot graph requested in sbunch.
        
        Parameters
        ----------
        sbunch

        Returns
        -------

        """
        min_index = min(sbunch)
        max_index = max(sbunch)
        # get all indexes between min and max
        graph_list = list(self.generator(min_index, max_index))
        # only get the indexes wanted
        graph_list = [graph_list[index - min_index] for index in sbunch]
        return graph_list
