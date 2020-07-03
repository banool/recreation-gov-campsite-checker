#!/usr/bin/env python3

import argparse
import json
import logging
import sys
from datetime import date, datetime, timedelta
from dateutil import rrule
from itertools import count, groupby

import requests
from fake_useragent import UserAgent


LOG = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(process)s - %(levelname)s - %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(formatter)
LOG.addHandler(sh)

BASE_URL = "https://www.recreation.gov"
AVAILABILITY_ENDPOINT = "/api/camps/availability/campground/"
MAIN_PAGE_ENDPOINT = "/api/camps/campgrounds/"

INPUT_DATE_FORMAT = "%Y-%m-%d"
ISO_DATE_FORMAT_REQUEST = "%Y-%m-%dT00:00:00.000Z"
ISO_DATE_FORMAT_RESPONSE = "%Y-%m-%dT00:00:00Z"

SUCCESS_EMOJI = "🏕"
FAILURE_EMOJI = "❌"

headers = {"User-Agent": UserAgent().random}


def format_date(date_object, format_string=ISO_DATE_FORMAT_REQUEST):
    """
    This function doesn't manipulate the date itself at all, it just
    formats the date in the format that the API wants.
    """
    date_formatted = datetime.strftime(date_object, format_string)
    return date_formatted


def send_request(url, params):
    resp = requests.get(url, params=params, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(
            "failedRequest",
            "ERROR, {} code received from {}: {}".format(
                resp.status_code, url, resp.text
            ),
        )
    return resp.json()


def get_park_information(park_id, start_date, end_date, campsite_type=None):
    """
    This function consumes the user intent, collects the necessary information
    from the recreation.gov API, and then presents it in a nice format for the
    rest of the program to work with. If the API changes in the future, this is
    the only function you should need to change.

    The only API to get availability information is the `month?` query param
    on the availability endpoint. You must query with the first of the month.
    This means if `start_date` and `end_date` cross a month bounday, we must
    hit the endpoint multiple times.

    The output of this function looks like this:

    {"<campsite_id>": [<date>, <date>]}

    Where the values are a list of ISO 8601 date strings representing dates
    where the campsite is available.

    Notably, the output doesn't tell you which sites are available. The rest of
    the script doesn't need to know this to determine whether sites are available.
    """

    # Get each first of the month for months in the range we care about.
    start_of_month = datetime(start_date.year, start_date.month, 1)
    months = list(rrule.rrule(rrule.MONTHLY, dtstart=start_of_month, until=end_date))

    # Get data for each month.
    api_data = []
    for month_date in months:
        params = {"start_date": format_date(month_date)}
        LOG.debug("Querying for {} with these params: {}".format(park_id, params))
        url = "{}{}{}/month?".format(BASE_URL, AVAILABILITY_ENDPOINT, park_id)
        resp = send_request(url, params)
        api_data.append(resp)

    # Collapse the data into the described output format.
    # Filter by campsite_type if necessary.
    data = {}
    for month_data in api_data:
        for campsite_id, campsite_data in month_data["campsites"].items():
            available = []
            for date, availability_value in campsite_data["availabilities"].items():
                if availability_value != "Available":
                    continue
                if campsite_type and campsite_type != campsite_data["campsite_type"]:
                    continue
                available.append(date)
            if available:
                a = data.setdefault(campsite_id, [])
                a += available

    return data


def get_name_of_site(park_id):
    url = "{}{}{}".format(BASE_URL, MAIN_PAGE_ENDPOINT, park_id)
    resp = send_request(url, {})
    return resp["campground"]["facility_name"]


def get_num_available_sites(park_information, start_date, end_date, nights=None):
    maximum = len(park_information)

    num_available = 0
    num_days = (end_date - start_date).days
    dates = [end_date - timedelta(days=i) for i in range(1, num_days + 1)]
    dates = set(format_date(i, format_string=ISO_DATE_FORMAT_RESPONSE) for i in dates)

    if nights not in range(1, num_days + 1):
        nights = num_days
        LOG.debug('Setting number of nights to {}.'.format(nights))

    for site, availabilities in park_information.items():
        # List of dates that are in the desired range for this site.
        desired_available = []
        for date in availabilities:
            if date not in dates:
                continue
            desired_available.append(date)
        if desired_available and consecutive_nights(desired_available, nights):
            num_available += 1
            LOG.debug("Available site {}: {}".format(num_available, site))

    return num_available, maximum


def consecutive_nights(available, nights):
    """
    Returns whether there are `nights` worth of consecutive nights.
    """
    ordinal_dates = [datetime.strptime(dstr, ISO_DATE_FORMAT_RESPONSE).toordinal() for dstr in available]
    c = count()
    longest_consecutive = max((list(g) for _, g in groupby(ordinal_dates, lambda x: x-next(c))), key=len)
    return len(longest_consecutive) >= nights


def main(parks):
    out = []
    availabilities = False
    for park_id in parks:
        park_information = get_park_information(
            park_id, args.start_date, args.end_date, args.campsite_type
        )
        LOG.debug(
            "Information for park {}: {}".format(
                park_id, json.dumps(park_information, indent=2)
            )
        )
        name_of_site = get_name_of_site(park_id)
        current, maximum = get_num_available_sites(
            park_information, args.start_date, args.end_date, nights=args.nights
        )
        if current:
            emoji = SUCCESS_EMOJI
            availabilities = True
        else:
            emoji = FAILURE_EMOJI

        out.append(
            "{} {} ({}): {} site(s) available out of {} site(s)".format(
                emoji, name_of_site, park_id, current, maximum
            )
        )

    if availabilities:
        print(
            "There are campsites available from {} to {}!!!".format(
                args.start_date.strftime(INPUT_DATE_FORMAT),
                args.end_date.strftime(INPUT_DATE_FORMAT),
            )
        )
    else:
        print("There are no campsites available :(")
    print("\n".join(out))
    return availabilities


def valid_date(s):
    try:
        return datetime.strptime(s, INPUT_DATE_FORMAT)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def positive_int(i):
    i = int(i)
    if i <= 0:
        msg = "Not a valid number of nights: {0}".format(i)
        raise argparse.ArgumentTypeError(msg)
    return i


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", "-d", action="store_true", help="Debug log level")
    parser.add_argument(
        "--start-date", required=True, help="Start date [YYYY-MM-DD]", type=valid_date
    )
    parser.add_argument(
        "--end-date",
        required=True,
        help="End date [YYYY-MM-DD]. You expect to leave this day, not stay the night.",
        type=valid_date,
    )
    parser.add_argument(
        "--nights",
        help="Number of consecutive nights (default is all nights in the given range).",
        type=positive_int,
    )
    parser.add_argument(
        "--campsite-type",
        help=(
            'If you want to filter by a type of campsite. For example '
            '"STANDARD NONELECTRIC" or TODO'
        ),
    )
    parks_group = parser.add_mutually_exclusive_group(required=True)
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

    args = parser.parse_args()

    if args.debug:
        LOG.setLevel(logging.DEBUG)

    parks = args.parks or [p.strip() for p in sys.stdin]

    try:
        code = 0 if main(parks) else 1
        sys.exit(code)
    except Exception:
        print("Something went wrong")
        LOG.exception("Something went wrong")
        raise
