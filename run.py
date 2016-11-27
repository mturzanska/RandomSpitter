import argparse
import logging

from random_shrubs.data import Data
from random_shrubs.shrubs import Node
from random_shrubs.shrubs import Shrub


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
    data.get_samples()
    data.get_attr_samples()
    shrubs = []
    counter = 0
    for sample, attrs in zip(data.samples, data.attr_samples):
        counter += 1
        logger.info(
            'Growing {nth} shrub. Attributes: {attrs}'
            .format(nth=counter, attrs=attrs)
        )
        root = Node(df=sample, is_root=True)
        shrub = Shrub(
            df=sample, attr_cols=attrs, class_col=data.class_col, root=root
        )
        shrub.grow()
        shrubs.append(shrub)
    labels = []
    for index, row in data.df.iterrows():
        labels.append(shrub.classify(row, shrub.root))
    data.df['label'] = labels

if __name__ == '__main__':

    logger = logging.getLogger('random_shrubs')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

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
