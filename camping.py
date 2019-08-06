#!/usr/bin/env python3

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta

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

SUCCESS_EMOJI = "🏕"
FAILURE_EMOJI = "❌"

headers = {"User-Agent": UserAgent().random}


def format_date(date_object):
    date_formatted = datetime.strftime(date_object, "%Y-%m-%dT00:00:00Z")
    return date_formatted


def generate_params(start, end):
    params = {"start_date": format_date(start), "end_date": format_date(end)}
    return params


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


def get_park_information(park_id, params):
    url = "{}{}{}".format(BASE_URL, AVAILABILITY_ENDPOINT, park_id)
    return send_request(url, params)


def get_name_of_site(park_id):
    url = "{}{}{}".format(BASE_URL, MAIN_PAGE_ENDPOINT, park_id)
    resp = send_request(url, {})
    return resp["campground"]["facility_name"]


def get_num_available_sites(resp, start_date, end_date):
    maximum = resp["count"]

    num_days = (end_date - start_date).days
    dates = [end_date - timedelta(days=i) for i in range(1, num_days + 1)]
    dates = set(format_date(i) for i in dates)
    sites_avail = []
    for site in resp["campsites"].values():
        available = False
        dates_avail = []
        for date, status in site["availabilities"].items():
            if date not in dates:
                continue
            if status == "Available":
                d = datetime.strptime(date, '%Y-%m-%dT00:00:00Z')
                ## filter out weekdays if needed:
                #if args.weekend and d.weekday() not in [4, 5]:
                #    continue
                available = True
                dates_avail.append(d)
        if available:
            sites_avail.append({'site': "site {}: {} {}".format(site['campsite_id'], site['site'], site['campsite_type']), 'dates': dates_avail })
            LOG.debug("Available site {}: {}".format(len(sites_avail), json.dumps(site, indent=1)))
    return maximum, sites_avail 

def display_date(d):
    return d.strftime("%a, %d %b %Y")

def valid_date(s):
    try:
        return datetime.strptime(s, INPUT_DATE_FORMAT)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def extract_consecutive_weekends(entry):
    weekends = []
    for d in entry["dates"]:
        LOG.debug("{} is a {}".format(display_date(d), d.weekday()))
        if d.weekday() == 4: # it's a friday
            following_saturday = d+timedelta(days=1)
            if following_saturday in entry['dates']:
                weekends.append(d)
                weekends.append(following_saturday)
    return weekends

def weekend_filter(sites_available):
    return [
            {
                "site": s["site"],
                "dates": extract_consecutive_weekends(s)
            }
            for s in sites_available
            if extract_consecutive_weekends(s)
            ]

def print_findings(dates_avail):
    formatted_dates = [
            {
                "site": s["site"],
                "dates": [display_date(d) for d in s["dates"]]
            }
            for s in dates_avail
            ]
    return json.dumps(formatted_dates, sort_keys=True,  indent=4)

def _main(parks):
    out = []
    availabilities = False
    for park_id in parks:
        params = generate_params(args.start_date, args.end_date)
        LOG.debug("Querying for {} with these params: {}".format(park_id, params))
        park_information = get_park_information(park_id, params)
        LOG.debug(
            "Information for {}: {}".format(
                park_id, json.dumps(park_information, indent=1)
            )
        )
        name_of_site = get_name_of_site(park_id)
        maximum, dates_avail = get_num_available_sites(
            park_information, args.start_date, args.end_date
        )
        if args.weekend:
            dates_avail = weekend_filter(dates_avail)
            
        current = len(dates_avail)
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
    if current:
        out.append(print_findings(dates_avail))

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weekend", "-w", action="store_true", help="Filter for friday-saturday availability")
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
        dest="parks", metavar="park", nargs="+", help="Park ID(s)", type=int
    )
    parser.add_argument(
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
        _main(parks)
    except Exception:
        print("Something went wrong")
        raise
