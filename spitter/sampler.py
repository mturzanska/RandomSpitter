import random


class Sampler(object):

    SAMPLE_FRAC = 0.67
    N_OF_SAMPLES = 10
    N_OF_ATTRS = 4

    def __init__(self, data, attr_names, sample_frac=SAMPLE_FRAC,
                 n_of_samples=N_OF_SAMPLES, n_of_attrs=N_OF_ATTRS):
        self.attr_names = attr_names
        self.samples = self.get_samples(data, sample_frac, n_of_samples)
        self.attrs = self.get_attr_sets(data, n_of_attrs, n_of_samples,
                                        attr_names)

    def get_samples(self, data, sample_frac, n_of_samples):
        samples = []
        for i in range(n_of_samples):
            sample = data.sample(frac=sample_frac)
            samples.append(sample)
        return samples

    def get_attr_sets(self, data, n_of_attrs, n_of_samples, attr_names):
        attr_sets = []
        if n_of_attrs > len(attr_names):
            n_of_attrs = len(attr_names)
        for i in range(n_of_samples):
            attrs = random.sample(attr_names, n_of_attrs)
            attr_sets.append(attrs)
        return attr_sets
