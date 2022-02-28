import unittest
from data_fetcher import *
from data_set import DataSet


class TestDataFetcher(unittest.TestCase):
    def test_nut_remover(self):
        nuts = ['DE069','DE069','DE069', 'DK420', 'SE123', 'SE123']
        expected_nuts = ['DE069', 'DK420', 'SE123']
        ind_nuts = individual_nuts(nuts)
        self.assertListEqual(ind_nuts, expected_nuts)

    def test_double_bigger_than(self):
        boolean = 2.0 * 0.95 < 2.0 < 2.0 * 1.05
        self.assertEqual(True, boolean)

    '''def test_data_splitter(self):
        rates = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        dates = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        nuts= ['DE069', 'DE069','DE069', 'DK420', 'DK420', 'DK420', 'SE123', 'SE123', 'SE123']
        DE069 = DataSet('DE069')
        DK420 = DataSet('DK420')
        SE123 = DataSet('SE123')
        DE069.rates = [1.0, 2.0, 3.0]
        DK420.rates = [4.0, 5.0, 6.0]
        SE123.rates = [7.0, 8.0, 9.0]
        DE069.dates = [1, 2, 3]
        DK420.dates = [1, 2, 3]
        SE123.dates = [1, 2, 3]
        expected_data = [DE069, DK420, SE123]
        data_sets = create_data_sets_by_nuts(rates, nuts, dates)
        self.assertListEqual(data_sets, expected_data)'''


if __name__ == '__main__':
    unittest.main()
