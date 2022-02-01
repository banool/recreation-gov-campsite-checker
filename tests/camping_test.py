import unittest
import camping
from utils.camping_argparser import CampingArgParser


class CampingTest(unittest.TestCase):

    def testAggregatesDataForMultipleCampsites(self):
        park_info = {'1': [],
                     '2': ['2022-06-22T00:00:00Z', '2022-06-23T00:00:00Z', '2022-06-26T00:00:00Z'],
                     '3': ['2022-06-22T00:00:00Z', '2022-06-23T00:00:00Z', '2022-06-26T00:00:00Z',
                               '2022-06-27T00:00:00Z', '2022-06-29T00:00:00Z']}
        _, _, available_dates_by_campsite_id = \
            camping.get_num_available_sites(
                park_info,
                CampingArgParser.TypeConverter.date('2022-06-22'),
                CampingArgParser.TypeConverter.date('2022-06-23')
            )

        self.assertFalse(1 in available_dates_by_campsite_id)
        self.assertTrue(2 in available_dates_by_campsite_id)
        self.assertTrue(3 in available_dates_by_campsite_id)

