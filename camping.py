#!/usr/bin/env python3

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta, date
import itertools

import requests
from fake_useragent import UserAgent
from parameters import *
from dateutil.relativedelta import relativedelta

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

start = datetime.now().strftime('%Y-%m-%d')
end = date.today() + relativedelta(months=+ parameters['months-out'])

start_datetime = datetime.strptime(start, '%Y-%m-%d')
end_datetime = datetime.strptime(str(end),'%Y-%m-%d')


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


def get_num_available_sites(resp, nights=None):
    maximum = resp["count"]

    num_available = 0
    num_days = (end_datetime - start_datetime).days
    dates = [end_datetime - timedelta(days=i) for i in range(1, num_days + 1)]
    dates = set(datetime.strftime(i, "%Y-%m-%dT00:00:00Z") for i in dates)
    if nights not in range(1, num_days + 1): 
        nights = num_days

    for site in resp["campsites"].values():
        available = []
        for date, status in site["availabilities"].items():
            if date not in dates:
                continue
            if status == "Available":
                available.append(True)
            else:
                available.append(False)
        if consecutive_nights(available, nights):
            num_available += 1
    return num_available, maximum


def consecutive_nights(available, nights):
    grouped = [len(list(g)) for k, g in itertools.groupby(available) if k]
    return nights <= max(grouped, default=0)


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

def _main():
    out = []
    availabilities = False
    for park_id in parameters['parks']:
        params = {"start_date": datetime.strftime(start_datetime, "%Y-%m-%dT00:00:00Z"), "end_date": datetime.strftime(end, "%Y-%m-%dT00:00:00Z")}


        park_information = get_park_information(park_id, params)
        
        # out.append("Information for {}: {}".format(
        #         park_id, json.dumps(park_information, indent=1)
        #     ))

        LOG.debug(
            "Information for {}: {}".format(
                park_id, json.dumps(park_information, indent=1)
            )
        )
        name_of_site = get_name_of_site(park_id)
        current, maximum = get_num_available_sites(
            park_information, nights=parameters['length']
        )
        if current:
            emoji = SUCCESS_EMOJI
            availabilities = True
        else:
            emoji = FAILURE_EMOJI

        out.append(
            "<br> {} {} ({}): {} site(s) available out of {} site(s)".format(
                emoji, name_of_site, park_id, current, maximum
            )
        )

    if availabilities:
        print(
            "There are campsites available from {} to {} for {} consecutive nights!!!".format(
                start_datetime.strftime(INPUT_DATE_FORMAT),
                end.strftime(INPUT_DATE_FORMAT),parameters['length'],
            )
        )
    else:
        print("There are no campsites available :(")
    print("\n".join(out))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", "-d", action="store_true", help="Debug log level")

    args = parser.parse_args()

    if args.debug:
        LOG.setLevel(logging.DEBUG)


    try:
        _main()
    except Exception:
        print("Something went wrong")
        raise
