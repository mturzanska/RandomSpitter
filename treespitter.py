from __future__ import division
from math import log

from tree import Node, Tree


class TreeSpitter(object):

    def __init__(self, init_data, init_attrs, class_col):
        self.init_data = init_data
        self.init_attrs = init_attrs
        self.class_col = class_col
        self.tree = Tree(init_data)

    def compute_entropy(self, data):
        entropy = 0
        data_size = len(data.index)
        classes = data[self.class_col].unique()
        for cls in classes:
            members = data.loc[data[self.class_col] == cls]
            cls_size = len(members)
            share = cls_size/data_size
            entropy -= share * log(share, 2)
        return entropy

    def compute_info_gain(self, data, attr):
        info_gain = self.compute_entropy(data)
        data_size = len(data.index)
        if attr in data.columns:
            attr_values = data[attr].unique()
            for value in attr_values:
                subset = data.loc[data[attr] == value]
                subset_size = len(data.index)
                share = subset_size/data_size
                entropy = self.compute_entropy(subset)
                info_gain -= share * entropy
            return info_gain

    def choose_attribute(self, data):
        info_gains = {}
        for attr in self.init_attrs:
            info_gain = self.compute_info_gain(data, attr)
            info_gains[attr] = info_gain
        return max(info_gains, key=lambda x: info_gains[x])

    def fork(self, data, attr):
        branches = {}
        try:
            attr_values = data[attr].unique()
        except KeyError:
            return
        for value in attr_values:
            branch = data.loc[data[attr] == value]
            branch = branch.drop(attr, axis=1)
            branches[value] = branch
        return branches

    def unstub_a_stub(self):
        stub = self.tree.stubs.pop()
        attr = self.choose_attribute(stub.data)
        branches = self.fork(stub.data, attr)
        if not branches:
            self.tree.leaves.append(stub)
            return
        for attr_value, data in branches.iteritems():
            child = Node(parent=stub, data=data, attr=attr,
                         attr_value=attr_value)
            stub.kids.append(child)
            self.tree.stubs.append(child)
            self.tree.nodes.append(stub)

    def spit_tree(self):
        while self.tree.stubs:
            self.unstub_a_stub()
        return self.tree
