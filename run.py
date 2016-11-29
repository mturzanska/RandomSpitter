import argparse

from random_shrubs.core import logger
from random_shrubs.data import Data
from random_shrubs.algorithm import RandomShrubs


def run(csv, class_col, sample_frac, n_of_samples, n_of_attrs):

    logger.info(
        'Reading data from {csv}. Class column: {class_col}'
        .format(csv=csv, class_col=class_col)
    )
    data = Data(
        file_path=csv, class_col=class_col, sample_frac=sample_frac,
        n_of_samples=n_of_samples, n_of_attrs=n_of_attrs
    )
    logger.info(
        'Splitting {csv} into {n} samples, each having {frac}% of instances'
        .format(csv=csv, n=data.n_of_samples, frac=data.sample_frac)
    )

    random_shrubs = RandomShrubs(data)
    random_shrubs.grow()
    random_shrubs.classify()
    random_shrubs.set_error_rate()

    logger.info(
        'Average error rate {0}'.format(random_shrubs.error_rate)
    )


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('csv', help='path to csv file with headers')
    parser.add_argument('class_col', help='name of the class column')
    parser.add_argument(
        '--sample_fraction',
        help='sample fraction to select for single shrub buliding')
    parser.add_argument(
        '--n_of_attrs',
        help='numbers of attrbutess to bulid single shrub with')
    parser.add_argument(
        '--n_of_shrubs',
        help='number of shrubs to bulid the model on')
    args = parser.parse_args()

    sample_frac = args.sample_fraction
    n_of_attrs = args.n_of_attrs
    n_of_samples = args.n_of_shrubs

    run(csv=args.csv, class_col=args.class_col,
        sample_frac=sample_frac,
        n_of_attrs=n_of_attrs,
        n_of_samples=n_of_samples)
