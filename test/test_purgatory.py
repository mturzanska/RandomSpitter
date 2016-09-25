from numpy.random import randint
from pandas import DataFrame

from spitter.purgatory import Purgatory

mock_attributes = ['a', 'b', 'c', 'd']
mock_class = ['e']
mock_colums = mock_attributes + mock_class
mock_data = DataFrame(randint(0, 100, size=(100, 5)),
                      columns=mock_colums)


class TestCheckForMissing:

    def test_no_missing(self):
        purgatory = Purgatory(mock_data, mock_class)
        len_before = len(purgatory.data.index)
        purgatory._check_for_missing()
        len_after = len(purgatory.data.index)
        assert len_before == len_after

    def test_one_missing(self):
        mock_data['a'].iloc[0] = None
        purgatory = Purgatory(mock_data, mock_class)
        len_before = len(purgatory.data.index)
        purgatory._check_for_missing()
        len_after = len(purgatory.data.index)
        assert len_after == len_before - 1

    def test_all_missing(self):
        mock_data['a'] = None
        purgatory = Purgatory(mock_data, mock_class)
        purgatory._check_for_missing()
        assert purgatory.data.empty
