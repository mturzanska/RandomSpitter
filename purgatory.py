from pandas import DataFrame


class Purgatory(object):

    def __init__(self, dirty_data, attr_cols, class_col):
        self.clean_data = self.clean(dirty_data, class_col)

    def clean(self, data, class_col):
        data_missing = data.isnull()
        if not data_missing.empty:
            data.dropna(inplace=True)
        underrep_class_count = self._check_for_imbalance(data, class_col)
        if underrep_class_count:
            data = self._undersample(data, underrep_class_count, class_col)
        return data

    @staticmethod
    def _check_for_imbalance(data, class_col):
        class_counts = data.groupby(class_col)[class_col].count()
        min_count = class_counts.min()
        max_count = class_counts.max()
        if max_count != min_count:
            return min_count

    @staticmethod
    def _check_for_missing(data):
        missing = data.isnull()
        missing_count = missing.sum()
        return missing_count

    @staticmethod
    def _undersample(data, sample_size, class_col):
        class_groups = data.groupby(class_col)
        undersampled = DataFrame()
        for name, data in class_groups:
            sample = data.sample(sample_size)
            undersampled = undersampled.append(sample)
        return undersampled
