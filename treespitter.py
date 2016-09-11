from __future__ import division
from math import log


class TreeSpitter(object):

    def __init__(self, data, attrs, class_col):
        self.data = data
        self.attrs = attrs
        self.class_col = class_col

    @staticmethod
    def compute_entropy(data, class_col):
        entropy = 0
        data_size = len(data.index)
        classes = data[class_col].unique()
        for cls in classes:
            members = data.loc[data[class_col] == cls]
            cls_size = len(members)
            proportion = cls_size/data_size
            entropy -= proportion * log(proportion, 2)
        return entropy

    def compute_info_gain(self, data, class_col, attr):
        info_gain = self.compute_entropy(data, class_col)
        data_size = len(data.index)
        attr_values = data[attr].unique()
        for value in attr_values:
            subset = data.loc[data[attr] == value]
            subset_size = len(data.index)
            proportion = subset_size/data_size
            entropy = self.compute_entropy(subset, class_col)
            info_gain -= proportion * entropy
        return info_gain

    def choose_attribute(self, data, attrs, class_col):
        info_gains = {}
        for attr in attrs:
            info_gain = self.compute_info_gain(data, class_col, attr)
            info_gains[attr] = info_gain
        return max(info_gains, key=lambda x: info_gains[x])

    def fork(self, data, attr):
        branches = {}
        attr_values = data[attr].unique()
        for value in attr_values:
            branch = data.loc[data[attr] == value]
            branch = branch.drop(attr, axis=1)
            branches[value] = branch,
        return branches
