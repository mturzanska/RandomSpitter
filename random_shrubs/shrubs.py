from __future__ import division
from math import log


class Node(object):

    def __init__(self, df=[], parent=None, kids=[],
                 attr=None, attr_value=None, is_root=False):
        self.df = df
        self.parent = parent
        self.kids = kids
        self.attr = attr
        self.attr_value = attr_value
        self.is_root = is_root


class Shrub(object):

    def __init__(self, df, attr_cols, class_col):
        self.df = df
        self.attr_cols = attr_cols
        self.class_col = class_col
        self.root = Node(df=self.df, is_root=True)
        self.nodes = []
        self.stubs = [self.root, ]
        self.leaves = []

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

    def compute_info_gain(self, df, attr, attr_cols):
        info_gain = self.compute_entropy(df=df, class_col=self.class_col)
        data_size = len(df.index)
        if attr in attr_cols:
            attr_values = df[attr].unique()
            for value in attr_values:
                subset = df.loc[df[attr] == value]
                subset_size = len(df.index)
                share = subset_size/data_size
                entropy = self.compute_entropy(subset, self.class_col)
                info_gain -= share * entropy
            return info_gain

    def choose_attribute(self, df, attr_cols):
        info_gains = {}
        for attr in attr_cols:
            info_gain = self.compute_info_gain(
                df=df, attr=attr, attr_cols=attr_cols)
            info_gains[attr] = info_gain
        return max(info_gains, key=lambda x: info_gains[x])

    def grow(self):
        while self.stubs:
            stub = self.stubs.pop()
            try:
                attr_cols = [c for c in stub.df.columns.values
                             if c != self.class_col]
                attr = self.choose_attribute(df=stub.df, attr_cols=attr_cols)
                branches = self.fork(stub.df, attr)
                for attr_value, df in branches.iteritems():
                    child = Node(df=df, parent=stub, attr=attr,
                                 attr_value=attr_value)
                    stub.kids.append(child)
                    self.stubs.append(child)
                    if stub not in self.nodes:
                        self.nodes.append(stub)
            except ValueError:
                self.leaves.append(stub)
