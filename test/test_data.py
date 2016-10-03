from __future__ import division

from pandas import DataFrame
import pytest

from random_shrubs.data import Data


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


class TestGetSamples:

    def test_number_of_samples(self, data):
        for i in xrange(3):
            data.n_of_samples = i
            data.get_samples()
            assert len(data.samples) == i

    def test_sample_fraction(self, data):
        sample_fractions = [0., 0.67, 1.]
        for f in sample_fractions:
            data.sample_frac = f
            data.get_samples()
            sample_size = len(data.samples[0].index)
            fraction_size = round(len(data.df.index) * f, 0)
            assert sample_size == fraction_size

    def test_sample_fraction_gt_1(self, data):
        data.sample_frac = 1.5
        with pytest.raises(ValueError):
            data.get_samples()


class TestGetAttrSets:
    pass
