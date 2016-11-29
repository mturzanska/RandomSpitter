import logging
import random
import sys

from pandas import DataFrame

from random_shrubs.defaults import N_OF_ATTRS, N_OF_SAMPLES, SAMPLE_FRAC


class Data(object):

    def __init__(self, file_path, class_col, sample_frac,
                 n_of_samples, n_of_attrs):
        self.df = DataFrame.from_csv(file_path, header=0, index_col=None)
        self.class_col = class_col
        self.cols = list(self.df.columns.values)
        try:
            self.attr_cols = self.cols[:]
            self.attr_cols.remove(class_col)
        except ValueError:
            print 'Class column {0} not present'.format(class_col)
            sys.exit(1)
        self.sample_frac = sample_frac if sample_frac else SAMPLE_FRAC
        self.n_of_samples = n_of_samples if n_of_samples else N_OF_SAMPLES
        self.n_of_attrs = n_of_attrs if n_of_attrs else N_OF_ATTRS
        self.samples = []
        self.valid_sets = []
        self.attr_samples = []

    def clean(self):
        self._check_for_missing()
        self._check_for_imbalance()

    def _check_for_missing(self):
        missing = self.df.isnull().values
        missing_count = missing.sum()
        row_count = len(self.df.index)
        logging.info('Dropping {0} rows out of {1}'
                     .format(missing_count, row_count))
        if missing.any():
            self.df.dropna(inplace=True)

    def _check_for_imbalance(self):
        class_grouped = self.df.groupby(self.class_col)
        class_counts = class_grouped[self.class_col].count()
        min_count = class_counts.values.min()
        max_count = class_counts.values.max()
        classes = self.df[self.class_col].unique()
        if len(classes) == 1:
            min_count = 0
        if max_count != min_count:
            logging.info('Undersampling to {0} items per class'
                         .format(min_count))
            self._undersample(min_count)

    def _undersample(self, sample_size):
        undersampled = DataFrame()
        if sample_size == 0:
            self.df = undersampled
            return
        class_groups = self.df.groupby(self.class_col)
        for name, data in class_groups:
            sample = self.df.sample(sample_size)
            undersampled = undersampled.append(sample)
        self.df = undersampled

    def get_samples(self):
        self.samples = []
        for i in range(self.n_of_samples):
            sample = self.df.sample(frac=self.sample_frac)
            valid_set = self.df[~self.df.isin(sample)].dropna()
            self.samples.append(sample)
            self.valid_sets.append(valid_set)

    def get_attr_samples(self):
        self.attr_samples = []
        n_of_attrs = min(self.n_of_attrs, len(self.attr_cols))
        for i in range(self.n_of_samples):
            attrs = random.sample(self.attr_cols, n_of_attrs)
            self.attr_samples.append(attrs)
