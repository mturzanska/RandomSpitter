import os

import pytest

from random_shrubs.data import Data


@pytest.fixture
def class_col():
    return 'good_day'


@pytest.fixture
def data_file():
    name = 'sample_data.csv'
    return os.path.join(os.path.dirname(__file__), name)


@pytest.fixture
def data(class_col, data_file):
    data = Data(data_file, class_col)
    return data


@pytest.fixture
def balanced_data(data, class_col):
    row_count = len(data.df.index)
    if row_count % 2 == 1:
        data.df.drop(data.df.tail(1).index, inplace=True)
        row_count -= 1
    split = int(row_count / 2)
    data.df[class_col].iloc[:split] = 1
    data.df[class_col].iloc[split:] = 0
    return data


@pytest.fixture
def imbalanced_data(data, class_col):
    row_count = len(data.df.index)
    if row_count % 2 == 0:
        data.df.drop(data.df.tail(1).index, inplace=True)
        row_count -= 1
    split = int(row_count / 2)
    data.df[class_col].iloc[:split] = 1
    data.df[class_col].iloc[split:] = 0
    return data
