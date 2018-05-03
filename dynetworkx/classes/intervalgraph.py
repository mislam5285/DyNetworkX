from networkx.classes.graph import Graph
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
            raise ValueError("IntervalGraph: edge duration must be strictly bigger than zero {0}.".format(iv_edge))

        print(self.tree[0:999999999])
