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
        set_size = len(data.index)
        classes = data[class_col].unique()
        for cls in classes:
            members = data.loc[data[class_col] == cls]
            cls_size = len(members)
            proportion = cls_size/set_size
            entropy -= proportion * log(proportion, 2)
        return entropy

    @staticmethod
    def calculate_information_gain(data, attr_col):
        pass
