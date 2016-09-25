import logging

from pandas import DataFrame


class Purgatory(object):

    def __init__(self, data, class_col):
        self.data = data
        self.class_col = class_col

    def clean(self):
        self._check_for_missing()
        self._check_for_imbalance()

    def _check_for_missing(self):
        missing = self.data.isnull().values
        missing_count = missing.sum()
        row_count = len(self.data.index)
        logging.info('Dropping {0} rows out of {1}'
                     .format(missing_count, row_count))
        if missing.any():
            self.data.dropna(inplace=True)

    def _check_for_imbalance(self):
        class_grouped = self.data.groupby(self.class_col)
        class_counts = class_grouped[self.class_col].count()
        min_count = class_counts.min().values
        max_count = class_counts.max().values
        if max_count != min_count:
            logging.info('Undersampling to {0} items per class'
                         .format(min_count))
            self._undersample(min_count)

    def _undersample(self, sample_size):
        class_groups = self.data.groupby(self.class_col)
        undersampled = DataFrame()
        for name, data in class_groups:
            sample = self.data.sample(sample_size)
            undersampled = undersampled.append(sample)
        self.data = undersampled
