#!/usr/bin/env python3

import argparse
import json
import sys
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.recreation.gov"
AVAILABILITY_ENDPOINT = "/api/camps/availability/campground/"
MAIN_PAGE_ENDPOINT = "/api/camps/campgrounds/"

INPUT_DATE_FORMAT = "%Y-%m-%d"

SUCCESS_EMOJI = "🏕"
FAILURE_EMOJI = "❌"


def format_date(date_object):
    date_formatted = datetime.strftime(date_object, "%Y-%m-%dT00:00:00Z")
    return date_formatted


def generate_payload(start, end):
    payload = {"start_date": format_date(start), "end_date": format_date(end)}
    return payload


def send_request(park_id, payload):
    url = "{}{}{}".format(BASE_URL, AVAILABILITY_ENDPOINT, park_id)
    resp = requests.get(url, params=payload)

    if resp.status_code != 200:
        raise RuntimeError(
            "failedRequest",
            "ERROR, {} code received from {}: {}".format(
                resp.status_code, url, resp.text
            ),
        )
    return resp.json()


def get_name_of_site(park_id):
    url = "{}{}{}".format(BASE_URL, MAIN_PAGE_ENDPOINT, park_id)
    resp = requests.get(url)
    return resp.json()["campground"]["facility_name"]


def get_num_available_sites(resp, start_date, end_date):
    maximum = resp["count"]

    num_available = 0
    num_days = (end_date - start_date).days
    dates = [end_date - timedelta(days=i) for i in range(1, num_days + 1)]
    dates = set(format_date(i) for i in dates)
    for site in resp["campsites"].values():
        available = bool(len(site["availabilities"]))
        for date, status in site["availabilities"].items():
            if date not in dates:
                continue
            if status != "Available":
                available = False
                break
        if available:
            num_available += 1
    return num_available, maximum


def valid_date(s):
    try:
        return datetime.strptime(s, INPUT_DATE_FORMAT)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start-date",
        required=True,
        help="Start date [YYYY-MM-DD]",
        type=valid_date,
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

    parks = args.parks or [p.strip() for p in sys.stdin]

    print(
        "These sites are available from {} to {}:".format(
            args.start_date.strftime(INPUT_DATE_FORMAT),
            args.end_date.strftime(INPUT_DATE_FORMAT),
        )
    )
    for park_id in parks:
        payload = generate_payload(args.start_date, args.end_date)
        resp_json = send_request(park_id, payload)
        name_of_site = get_name_of_site(park_id)
        current, maximum = get_num_available_sites(
            resp_json, args.start_date, args.end_date
        )
        emoji = SUCCESS_EMOJI if current else FAILURE_EMOJI
        print(
            "{} {}: {} site(s) available out of {} site(s)".format(
                emoji, name_of_site, current, maximum
            )
        )
