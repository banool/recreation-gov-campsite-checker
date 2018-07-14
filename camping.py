#!/usr/bin/env python3

import argparse
import re
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Runs the actual search
SEARCH_PAYLOAD = {
    "contractCode": "NRSO",
    "search": "site",
    "siteTypeFilter": "ALL",
    "submitSiteForm": "true",
}

DETAILS_PAYLOAD = {"contractCode": "NRSO"}

BASE_URL = "https://www.recreation.gov"
CAMPSITE_SEARCH = "/campsiteSearch.do"
CAMPGROUND_DETAILS = "/campgroundDetails.do"

INPUT_DATE_FORMAT = "%Y-%m-%d"

SUCCESS_EMOJI = "🏕"
FAILURE_EMOJI = "❌"


def format_date(date_object):
    date_formatted = datetime.strftime(date_object, "%a %b %d %Y")
    return date_formatted


def generate_details_payload(park_id):
    payload = {**DETAILS_PAYLOAD, **{"parkId": park_id}}
    return payload


def generate_search_payload(start, end):
    payload = {
        **SEARCH_PAYLOAD,
        **{
            "arrivalDate": format_date(start),
            "departureDate": format_date(end),
        },
    }
    return payload


def send_request(details_payload, search_payload):
    with requests.Session() as s:
        # We need to get the details page first to set the  session cookie.
        s.get(BASE_URL + CAMPGROUND_DETAILS, params=details_payload)
        resp = s.post(BASE_URL + CAMPSITE_SEARCH, params=search_payload)

        if resp.status_code != 200:
            raise RuntimeError(
                "failedRequest",
                "ERROR, %d code received from %s".format(
                    resp.status_code, BASE_URL + CAMPSITE_SEARCH
                ),
            )
        else:
            return resp.text


def get_name_of_site(html_resp):
    soup = BeautifulSoup(html_resp, "html.parser")
    return soup.find(id="cgroundName").string


def get_num_available_sites(html_resp):
    soup = BeautifulSoup(html_resp, "html.parser")
    container = soup.find(id="contentArea")
    availability = container.findAll("div", {"class": "matchSummary"})[0].string
    m = re.search(
        r"(\d+) site\(s\) available out of (\d+)  site\(s\)", availability
    )
    current = int(m.group(1))  # For < 3.6 compatability, instead of m[1].
    maximum = int(m.group(2))
    return current, maximum


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
        help="End date [YYYY-MM-DD]",
        type=valid_date,
    )
    parser.add_argument(
        dest="parks", metavar="park", nargs="*", help="Park ID(s)", type=int
    )
    parser.add_argument(
        "--stdin",
        "-",
        action="store_true",
        help="Read list of park ID(s) from stdin instead",
    )

    args = parser.parse_args()

    parks = args.parks or [p.strip() for p in sys.stdin]

    availabilities = {}
    for park_id in parks:
        details_payload = generate_details_payload(park_id)
        search_payload = generate_search_payload(args.start_date, args.end_date)
        resp = send_request(details_payload, search_payload)
        name_of_site = get_name_of_site(resp)
        current, maximum = get_num_available_sites(resp)
        emoji = SUCCESS_EMOJI if current else FAILURE_EMOJI
        print(
            "{} {}: {} site(s) available out of {} site(s)".format(
                emoji, name_of_site, current, maximum
            )
        )
