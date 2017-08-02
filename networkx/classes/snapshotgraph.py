from networkx.classes.graph import Graph

class SnapshotGraph(object):
    def __init__(self, **attr):
        self.graphs = {}
        self.graph.update(attr)
        self.snapshots = []

    def add_snapshot(self, edges):
        g = Graph()
        g.add_weighted_edges_from(edges)
        self.snapshots.append(g)
