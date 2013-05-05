"""
placeholder
"""
import heapq
import urllib2
from urlnorm import url_normalize

class PriorityQueue(object):

    """ A wrapper over python heapq which maintains uniqueness"""

    def __init__(self, ):
        self.heap = []
        self.hashtable = set()

    def __repr__(self):
        return str(self.heap)

    def add(self, element, priority):

        """
            Appends element to heap.
        """
        element = url_normalize(element) # only use normalized urls
        
        if element not in self.hashtable:
            heapq.heappush(self.heap, (priority, element))
            self.hashtable.add(element)

    def get(self):

        """
            @return tuple

            Pops element out from the heap.
        """

        return heapq.heappop(self.heap)[1]
        
class BalerionRedirectHandler(urllib2.HTTPRedirectHandler):

    """ add Custom URL redirects handlers here. """
    def __init__(self):
        pass

    def http_error_302(self, req, fp, code, msg, headers):
        return fp
    
    http_error_301 = http_error_303 = http_error_307 = http_error_302

class AttrDict(dict):

    """ A dict that allows for object-like property access syntax. """

    def __init__(self, new_dict=None):
        dict.__init__(self)
        if new_dict:
            self.update(new_dict)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, key, value):
        self.update({key: value})

