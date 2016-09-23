import uuid


class Tree(object):

    def __init__(self, init_data):
        self.root = Node(data=init_data)
        self.leaves = [self.root, ]
        self.nodes = [self.root, ]


class Node(object):

    def __init__(self, parent_node=[], data=[],
                 attr=None, attr_value=None, level=1):
        self.id = uuid.uuid4()
        self.parent_node = parent_node
        self.attr = attr
        self.attr_value = attr_value
        self.is_root = False
        if not parent_node:
            self.is_root = True
        self.data = data
        self.level = level
