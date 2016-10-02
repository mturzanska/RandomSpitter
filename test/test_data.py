from __future__ import division

from pandas import DataFrame
import pytest

from spitter.data import Data


class TestDataInit:

    def test_data_load(self, data, class_col):
        assert type(data.df) == DataFrame
        assert data.class_col == class_col
        assert data.attr_cols
        assert data.cols == data.attr_cols + [data.class_col]

    def test_class_col_absent(self, data_file):
        absent_class_col = 'not_here'
        with pytest.raises(SystemExit):
            with pytest.raises(ValueError):
                Data(data_file, absent_class_col)


class TestCheckForMissing:

    def test_no_missing(self, data):
        len_before = len(data.df.index)
        data._check_for_missing()
        len_after = len(data.df.index)
        assert len_before == len_after

    def test_one_missing(self, data, class_col):
        data.df[class_col].iloc[0] = None
        len_before = len(data.df.index)
        data._check_for_missing()
        len_after = len(data.df.index)
        assert len_before == len_after + 1

    def test_all_missing(self, data, class_col):
        data.df[class_col] = None
        data._check_for_missing()
        assert data.df.empty


class TestCheckForImbalance:

    def test_no_imbalance(self, balanced_data):
        len_before = len(balanced_data.df.index)
        balanced_data._check_for_imbalance()
        len_after = len(balanced_data.df.index)
        assert len_before == len_after

    def test_imbalance_of_one(self, imbalanced_data):
        len_before = len(imbalanced_data.df.index)
        imbalanced_data._check_for_imbalance()
        len_after = len(imbalanced_data.df.index)
        assert len_before == len_after + 1

    def test_max_imbalance(self, data, class_col):
        data.df[class_col] = 1
        data._check_for_imbalance()
        assert data.df.empty
