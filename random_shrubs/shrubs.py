from __future__ import division
from math import log


class Node(object):

    def __init__(self, df=[], parent=None, kids=[],
                 attr=None, attr_value=None):
        self.df = df
        self.parent = parent
        self.kids = kids
        self.attr = attr
        self.attr_value = attr_value


class Shrub(object):

    def __init__(self, df, attr_cols, class_col):
        self.df = df
        self.attr_cols = attr_cols
        self.class_col = class_col
        self.root = Node(df=self.df)
        self.nodes = [self.root, ]
        self.leaves = []
        while self.stubs:
            self.grow()

    @staticmethod
    def compute_entropy(df, class_col):
        entropy = 0
        data_size = len(df.index)
        classes = df[class_col].unique()
        for cls in classes:
            members = df.loc[df[class_col] == cls]
            cls_size = len(members)
            share = cls_size/data_size
            entropy -= share * log(share, 2)
        return entropy

    @staticmethod
    def fork(df, attr):
        branches = {}
        try:
            attr_values = df[attr].unique()
        except KeyError:
            return
        for value in attr_values:
            branch = df.loc[df[attr] == value]
            branch = branch.drop(attr, axis=1)
            branches[value] = branch
        return branches

    def compute_info_gain(self, attr):
        info_gain = self.compute_entropy(df=self.df, class_col=self.class_col)
        data_size = len(self.df.index)
        if attr in self.attr_cols:
            attr_values = self.df[attr].unique()
            for value in attr_values:
                subset = self.df.loc[self.df[attr] == value]
                subset_size = len(self.df.index)
                share = subset_size/data_size
                entropy = self.compute_entropy(subset, self.class_col)
                info_gain -= share * entropy
            return info_gain

    def choose_attribute(self):
        info_gains = {}
        for attr in self.attr_cols:
            info_gain = self.compute_info_gain(attr=attr)
            info_gains[attr] = info_gain
        return max(info_gains, key=lambda x: info_gains[x])

    def grow(self):
        stub = self.stubs.pop()
        attr = self.choose_attribute()
        branches = self.fork(stub.df, attr)
        if not branches:
            self.shrub.leaves.append(stub)
            return
        for attr_value, df in branches.iteritems():
            child = Node(df=df, parent=stub, attr=attr, attr_value=attr_value)
            stub.kids.append(child)
            self.stubs.append(child)
            self.nodes.append(stub)
