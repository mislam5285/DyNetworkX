"""
    Base class for dynamic edges
"""

class DynamicEdge(object):
    def __init__(self, start_time, end_time, **attrs):
        """
        Parameters
        ----------
        start_time: offset-based
        end_time: offset-based
        Returns
        -------
        """

        self.attributes = attrs
        self.start_time = start_time
        self.end_time   = end_time
