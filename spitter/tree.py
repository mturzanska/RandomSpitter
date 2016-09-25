import uuid


class Tree(object):

    def __init__(self, init_data):
        self.root = Node(data=init_data)
        self.nodes = []
        self.stubs = [self.root, ]
        self.leaves = []


class Node(object):

    def __init__(self, data=[], parent=None, kids=[],
                 attr=None, attr_value=None):
        self.id = uuid.uuid4()
        self.parent = parent
        self.kids = kids
        self.attr = attr
        self.attr_value = attr_value
        self.data = data
