from __future__ import division
from math import log


class TreeSpitter(object):

    def __init__(self, data, attrs, class_col):
        self.data = data
        self.attrs = attrs
        self.class_col = class_col

    @staticmethod
    def calculate_entropy(data, class_col):
        entropy = 0
        data_size = len(data.index)
        classes = data[class_col].unique()
        for cls in classes:
            members = data.loc[data[class_col] == cls]
            cls_size = len(members)
            proportion = cls_size/data_size
            entropy -= proportion * log(proportion, 2)
        return entropy

    def calculate_information_gain(self, data, class_col, attr):
        information_gain = self.calculate_entropy(data, class_col)
        data_size = len(data.index)
        attr_values = data[attr].unique()
        for value in attr_values:
            subset = data.loc[data[attr] == value]
            subset_size = len(data.index)
            proportion = subset_size/data_size
            entropy = self.calculate_entropy(subset, class_col)
            information_gain -= proportion * entropy
        return information_gain

    def spit_tree(self):
        pass
