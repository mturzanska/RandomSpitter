from __future__ import division
from math import log

import numpy as np

from random_shrubs.core import logger


class Node(object):

    def __init__(self, df=None, parent=None, kids=None,
                 attr=None, attr_value=None, is_root=False):
        self.df = df
        self.parent = parent
        self.kids = kids or []
        self.attr = attr
        self.attr_value = attr_value
        self.is_root = is_root
        self.label = None


class Shrub(object):

    def __init__(self, df, attrs, label, root):
        self.df = df
        self.attrs = attrs
        self.label = label
        self.root = root
        self.nodes = []
        self.stubs = [root, ]
        self.leaves = []

    @staticmethod
    def classify(df_row, root):
        label = None
        node = root
        while label is None:
            for kid in node.kids:
                attr_value = df_row[kid.attr]
                if kid.attr_value == attr_value:
                    node = kid
                    label = kid.label
        return label

    @staticmethod
    def compute_entropy(df, label):
        entropy = 0
        data_size = len(df.index)
        label_values = df[label].unique()
        for l in label_values:
            instances = df.loc[df[label] == l]
            share = len(instances)/data_size
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

    def compute_info_gain(self, df, attr, attrs):
        info_gain = self.compute_entropy(df=df, label=self.label)
        data_size = len(df.index)
        if attr in attrs:
            attr_values = df[attr].unique()
            for value in attr_values:
                subset = df.loc[df[attr] == value]
                subset_size = len(df.index)
                share = subset_size/data_size
                entropy = self.compute_entropy(subset, self.label)
                info_gain -= share * entropy
            return info_gain

    def choose_attribute(self, df, attrs):
        info_gains = {}
        for attr in attrs:
            info_gain = self.compute_info_gain(
                df=df, attr=attr, attrs=attrs)
            info_gains[attr] = info_gain
        return max(info_gains, key=lambda x: info_gains[x])

    def grow(self):
        while self.stubs:
            stub = self.stubs.pop()
            try:
                attrs = [c for c in stub.df.columns.values if c != self.label]
                attr = self.choose_attribute(df=stub.df, attrs=attrs)
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
        for leaf in self.leaves:
            leaf.label = leaf.df[self.label].value_counts().idxmax()


class RandomShrubs(object):

    def __init__(self, data):
        self.df = data.df
        data.get_samples()
        self.samples = data.samples
        data.get_attr_samples()
        self.attr_samples = data.attr_samples
        self.label = data.class_col
        self.shrubs = None

    def grow(self):
        self.shrubs = []
        for df, attrs in zip(self.samples, self.attr_samples):
            shrub_id = len(self.shrubs) + 1 if self.shrubs else 1
            logger.info(
                'Growing {shrub_id} shrub.Attributes: {attrs}'
                .format(shrub_id=shrub_id, attrs=attrs)
            )
            root = Node(df=df, is_root=True)
            shrub = Shrub(df=df, attrs=attrs, label=self.label, root=root)
            shrub.grow()
            self.shrubs.append(shrub)

    def classify(self):
        self.df['labels'] = self.df.apply(lambda x: [], axis=1)
        for shrub in self.shrubs:
            for index, row in self.df.iterrows():
                label = shrub.classify(row, shrub.root)
                row['labels'] = row['labels'].append(label)
        self.df['label'] = self.df['labels'].apply(lambda x: sum(x) / len(x))
        self.df['label'] = np.where(self.df['label'] > 0.5, 1, 0)
