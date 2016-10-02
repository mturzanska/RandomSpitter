from __future__ import division
import os

from pandas import DataFrame
import pytest

from spitter.data import Data

sample_data_file = 'sample_data.csv'
sample_data_path = os.path.join(os.path.dirname(__file__), sample_data_file)
class_col = 'good_day'


class TestDataInit:

    def test_data_load(self):
        data = Data(sample_data_path, class_col)
        assert type(data.df) == DataFrame
        assert data.class_col == class_col
        assert data.attr_cols
        assert data.cols == data.attr_cols + [data.class_col]

    def test_class_col_absent(self):
        absent_class_col = 'not_here'
        with pytest.raises(SystemExit):
            with pytest.raises(ValueError):
                Data(sample_data_path, absent_class_col)


class TestCheckForMissing:

    def test_no_missing(self):
        data = Data(sample_data_path, class_col)
        len_before = len(data.df.index)
        data._check_for_missing()
        len_after = len(data.df.index)
        assert len_before == len_after

    def test_one_missing(self):
        data = Data(sample_data_path, class_col)
        data.df[class_col].iloc[0] = None
        len_before = len(data.df.index)
        data._check_for_missing()
        len_after = len(data.df.index)
        assert len_before == len_after + 1

    def test_all_missing(self):
        data = Data(sample_data_path, class_col)
        data.df[class_col] = None
        data._check_for_missing()
        assert data.df.empty


class TestCheckForImbalance:

    def test_no_imbalance(self):
        data = Data(sample_data_path, class_col)
        row_count = len(data.df.index)
        if row_count % 2 == 1:
            data.df.drop(data.df.tail(1).index, inplace=True)
            row_count -= 1
        split = int(row_count / 2)
        data.df[class_col].iloc[:split] = 1
        data.df[class_col].iloc[split:] = 0
        len_before = len(data.df.index)
        data._check_for_imbalance()
        len_after = len(data.df.index)
        assert len_before == len_after

    def test_imbalance_of_one(self):
        data = Data(sample_data_path, class_col)
        row_count = len(data.df.index)
        if row_count % 2 == 0:
            data.df.drop(data.df.tail(1).index, inplace=True)
            row_count -= 1
        split = int(row_count / 2)
        data.df[class_col].iloc[:split] = 1
        data.df[class_col].iloc[split:] = 0
        len_before = len(data.df.index)
        data._check_for_imbalance()
        len_after = len(data.df.index)
        assert len_before == len_after + 1

    def test_max_imbalance(self):
        data = Data(sample_data_path, class_col)
        data.df[class_col] = 1
        data._check_for_imbalance()
        assert data.df.empty
