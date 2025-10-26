import unittest

import camping
import notifier
from utils.camping_argparser import CampingArgumentParser


class TestNotifier(unittest.TestCase):

    def testGenerateAvailabilityString_DefaultCampingOutput(self):
        info_by_park_id = {
            1000: (
                2,
                3,
                {
                    18621: [{"start": "2022-06-22", "end": "2022-06-23"}],
                    18654: [{"start": "2022-06-22", "end": "2022-06-23"}],
                },
                "SOME PARK",
            )
        }
        output, _ = camping.generate_human_output(
            info_by_park_id,
            CampingArgumentParser.TypeConverter.date("2022-06-22"),
            CampingArgumentParser.TypeConverter.date("2022-06-24"),
        )

        # raw_input.return_value = output
        availability_strings = notifier.generate_availability_strings(
            output.split("\n")
        )
        expected = [
            "{num_avail} site(s) available in {park_name_and_id}".format(
                num_avail=2, park_name_and_id="SOME PARK (1000)"
            )
        ]
        self.assertEqual(expected, availability_strings)

    def testGenerateAvailabilityString_WithSiteCampingOutput(self):
        info_by_park_id = {
            1000: (
                2,
                3,
                {
                    18621: [{"start": "2022-06-22", "end": "2022-06-23"}],
                    18654: [{"start": "2022-06-22", "end": "2022-06-23"}],
                },
                "SOME PARK",
            )
        }
        output, _ = camping.generate_human_output(
            info_by_park_id,
            CampingArgumentParser.TypeConverter.date("2022-06-22"),
            CampingArgumentParser.TypeConverter.date("2022-06-24"),
            True
        )

        # raw_input.return_value = output
        availability_strings = notifier.generate_availability_strings(
            output.split("\n")
        )
        expected = [
            "{num_avail} site(s) available in {park_name_and_id}".format(
                num_avail=2, park_name_and_id="SOME PARK (1000)"
            )
        ]
        self.assertEqual(expected, availability_strings)


if __name__ == "__main__":
    unittest.main()
