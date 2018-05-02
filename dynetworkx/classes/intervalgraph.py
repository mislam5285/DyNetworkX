from networkx.classes.graph import Graph


class IntervalGraph(object):
    def __init__(self, **attr):
        self.graphs = {}
        self.graph.update(attr)
        self.snapshots = []