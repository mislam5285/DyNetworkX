"""
    Base class for dynamic edges
"""

class DynamicEdge(object):
    def __init__(self, edge_id, start_time, end_time, attrs):
        self.edge_id    = edge_id
        self.start_time = start_time
        self.attributes = attrs
        self.end_time   = end_time

    def __hash__(self):
        return self.edge_id

