import argparse
import logging
import sys
from datetime import datetime

from enums.date_format import DateFormat


class CampingArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument(
            "--debug", "-d", action="store_true", help="Debug log level"
        )
        self.add_argument(
            "--start-date",
            required=True,
            help="Start date [YYYY-MM-DD]",
            type=self.TypeConverter.date,
        )
        self.add_argument(
            "--end-date",
            required=True,
            help="End date [YYYY-MM-DD]. You expect to leave this day, not stay the night.",
            type=self.TypeConverter.date,
        )
        self.add_argument(
            "--nights",
            help="Number of consecutive nights (default is all nights in the given range).",
            type=self.TypeConverter.positive_int,
        )
        self.add_argument(
            "--campsite-ids",
            type=int,
            nargs="+",
            default=(),
            help="Optional, search for availability for a specific campsite ID.",
        )
        self.add_argument(
            "--show-campsite-info",
            action="store_true",
            help="Display campsite ID and availability dates.",
        )
        self.add_argument(
            "--campsite-type",
            help=(
                "Optional, can specify type of campsite such as:"
                '"STANDARD NONELECTRIC" or TODO'
            ),
        )
        self.add_argument(
            "--json-output",
            action="store_true",
            help=(
                "This make the script output JSON instead of human readable "
                "output. Note, this is incompatible with the twitter notifier. "
                "This output includes more precise information, such as the exact "
                "available dates and which sites are available."
            ),
        )
        self.add_argument(
            "--weekends-only",
            action="store_true",
            help=(
                "Include only weekends (i.e. starting Friday or Saturday)"
            ),
        )
        self.add_argument(
            "--exclusion-file",
            help=(
                "File with site IDs to exclude"
            ),
        )
        parks_group = self.add_mutually_exclusive_group(required=True)
        parks_group.add_argument(
            "--parks",
            dest="parks",
            metavar="park",
            nargs="+",
            help="Park ID(s)",
            type=int,
        )
        parks_group.add_argument(
            "--stdin",
            "-",
            action="store_true",
            help="Read list of park ID(s) from stdin instead",
        )

    def parse_args(self, args=None, namespace=None):
        args = super().parse_args(args, namespace)
        args.parks = args.parks or [p.strip() for p in sys.stdin]
        self._validate_args(args)
        return args

    @classmethod
    def _validate_args(cls, args):
        if len(args.parks) > 1 and len(args.campsite_ids) > 0:
            raise cls.ArgumentCombinationError(
                "--campsite-ids can only be used with a single park ID."
            )

    class TypeConverter:
        @classmethod
        def date(cls, date_str):
            try:
                return datetime.strptime(
                    date_str, DateFormat.INPUT_DATE_FORMAT.value
                )
            except ValueError as e:
                msg = "Not a valid date: '{0}'.".format(date_str)
                logging.critical(e)
                raise argparse.ArgumentTypeError(msg)

        @classmethod
        def positive_int(cls, i):
            i = int(i)
            if i <= 0:
                msg = "Not a valid number of nights: {0}".format(i)
                raise argparse.ArgumentTypeError(msg)
            return i

    class ArgumentCombinationError(Exception):
        pass
