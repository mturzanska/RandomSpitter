import argparse

from random_shrubs.core import logger
from random_shrubs.data import Data, TrainData
from random_shrubs.algorithm import RandomShrubs


def run(train_set, classify_set, class_col, sample_frac,
        n_of_shrubs, n_of_attrs):

    logger.info('Reading data from {0}'.format(train_set))
    train_data = TrainData(
        class_col=class_col, sample_frac=sample_frac, n_of_samples=n_of_shrubs,
        n_of_attrs=n_of_attrs, data_set=train_set
    )
    classify_data = Data(data_set=classify_set)
    random_shrubs = RandomShrubs(
        train_data=train_data, classify_data=classify_data
    )
    random_shrubs.grow()
    logger.info('Classifying {0}'.format(classify_set))
    random_shrubs.classify()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('train_set', help='training csv file with headers')
    parser.add_argument(
        'classify_set',
        help='unclassified csv file with headers'
    )
    parser.add_argument('class_col', help='class column header')
    parser.add_argument(
        '--sample_frac',
        help='training data fraction per shrub')
    parser.add_argument(
        '--n_of_attrs',
        help='number of attributes per shrub')
    parser.add_argument(
        '--n_of_shrubs',
        help='number of shrubs')
    args = parser.parse_args()

    run(
        train_set=args.train_set, classify_set=args.classify_set,
        class_col=args.class_col, sample_frac=args.sample_frac,
        n_of_attrs=args.n_of_attrs, n_of_shrubs=args.n_of_shrubs
    )
