#!/usr/bin/env python3

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta
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


def site_date_to_human_date(date_string):
    date_object = datetime.strptime(date_string, ISO_DATE_FORMAT_RESPONSE)
    return format_date(date_object, format_string=INPUT_DATE_FORMAT)


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
            a = data.setdefault(campsite_id, [])
            for date, availability_value in campsite_data["availabilities"].items():
                if availability_value != "Available":
                    continue
                if campsite_type and campsite_type != campsite_data["campsite_type"]:
                    continue
                available.append(date)
            if available:
                a += available

    return data


def get_name_of_park(park_id):
    url = "{}{}{}".format(BASE_URL, MAIN_PAGE_ENDPOINT, park_id)
    resp = send_request(url, {})
    return resp["campground"]["facility_name"]


def get_num_available_sites(park_information, start_date, end_date, nights=None):
    availabilities_filtered = []
    maximum = len(park_information)

    num_available = 0
    num_days = (end_date - start_date).days
    dates = [end_date - timedelta(days=i) for i in range(1, num_days + 1)]
    dates = set(format_date(i, format_string=ISO_DATE_FORMAT_RESPONSE) for i in dates)

    if nights not in range(1, num_days + 1):
        nights = num_days
        LOG.debug("Setting number of nights to {}.".format(nights))

    for site, availabilities in park_information.items():
        # List of dates that are in the desired range for this site.
        desired_available = []

        for date in availabilities:
            if date not in dates:
                continue
            desired_available.append(date)

        if not desired_available:
            continue

        appropriate_consecutive_ranges = consecutive_nights(desired_available, nights)

        if appropriate_consecutive_ranges:
            num_available += 1
            LOG.debug("Available site {}: {}".format(num_available, site))

        for r in appropriate_consecutive_ranges:
            start, end = r
            availabilities_filtered.append(
                {"site": int(site), "start": start, "end": end}
            )

    return num_available, maximum, availabilities_filtered


def consecutive_nights(available, nights):
    """
    Returns a list of dates from which you can start that have
    enough consecutive nights.

    If there is one or more entries in this list, there is at least one
    date range for this site that is available.
    """
    ordinal_dates = [
        datetime.strptime(dstr, ISO_DATE_FORMAT_RESPONSE).toordinal()
        for dstr in available
    ]
    c = count()

    consective_ranges = list(
        list(g) for _, g in groupby(ordinal_dates, lambda x: x - next(c))
    )

    long_enough_consecutive_ranges = []
    for r in consective_ranges:
        # Skip ranges that are too short.
        if len(r) < nights:
            continue
        for start_index in range(0, len(r) - nights):
            start_nice = format_date(
                datetime.fromordinal(r[start_index]), format_string=INPUT_DATE_FORMAT
            )
            end_nice = format_date(
                datetime.fromordinal(r[start_index + nights]),
                format_string=INPUT_DATE_FORMAT,
            )
            long_enough_consecutive_ranges.append((start_nice, end_nice))

    return long_enough_consecutive_ranges


def check_park(park_id, start_date, end_date, campsite_type, nights=None):
    park_information = get_park_information(
        park_id, start_date, end_date, campsite_type
    )
    LOG.debug(
        "Information for park {}: {}".format(
            park_id, json.dumps(park_information, indent=2)
        )
    )
    name_of_park = get_name_of_park(park_id)
    current, maximum, availabilities_filtered = get_num_available_sites(
        park_information, start_date, end_date, nights=nights
    )
    return current, maximum, availabilities_filtered, name_of_park


def output_human_output(parks):
    out = []
    availabilities = False
    for park_id in parks:
        current, maximum, _, name_of_park = check_park(
            park_id, args.start_date, args.end_date, args.campsite_type, nights=args.nights
        )
        if current:
            emoji = SUCCESS_EMOJI
            availabilities = True
        else:
            emoji = FAILURE_EMOJI

        out.append(
            "{} {} ({}): {} site(s) available out of {} site(s)".format(
                emoji, name_of_park, park_id, current, maximum
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


def output_json_output(parks):
    park_to_availabilities = {}
    availabilities = False
    for park_id in parks:
        current, _, availabilities_filtered, _ = check_park(
            park_id, args.start_date, args.end_date, args.campsite_type, nights=args.nights
        )
        if current:
            availabilities = True
            park_to_availabilities[park_id] = availabilities_filtered

    print(json.dumps(park_to_availabilities))

    return availabilities


def main(parks, json_output=False):
    if json_output:
        return output_json_output(parks)
    else:
        return output_human_output(parks)


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
            "If you want to filter by a type of campsite. For example "
            '"STANDARD NONELECTRIC" or TODO'
        ),
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help=(
            "This make the script output JSON instead of human readable "
            "output. Note, this is incompatible with the twitter notifier. "
            "This output includes more precise information, such as the exact "
            "avaiable dates and which sites are available."
        ),
    )
    parks_group = parser.add_mutually_exclusive_group(required=True)
    parks_group.add_argument(
        "--parks", dest="parks", metavar="park", nargs="+", help="Park ID(s)", type=int
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
        code = 0 if main(parks, json_output=args.json_output) else 1
        sys.exit(code)
    except Exception:
        print("Something went wrong")
        LOG.exception("Something went wrong")
        raise
