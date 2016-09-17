import uuid


class Tree(object):

    def __init__(self, init_data):
        self.root = Node(data=init_data)
        self.nodes = [self.root, ]
        self.depth = 1


class Node(object):

    def __init__(self, parent_node=[], data=[],
                 attr=None, attr_value=None):
        self.id = uuid.uuid4()
        self.parent_node = parent_node
        self.attr = attr
        self.attr_value = attr_value
        self.is_root = False
        if not parent_node:
            self.is_root = True
        self.is_leaf = False
        if data:
            self.is_leaf = True
