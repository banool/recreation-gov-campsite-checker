import logging

import requests
from fake_useragent import UserAgent

from utils import formatter

LOG = logging.getLogger(__name__)


class RecreationClient:

    BASE_URL = "https://www.recreation.gov"
    AVAILABILITY_ENDPOINT = BASE_URL + "/api/camps/availability/campground/{park_id}/month"
    MAIN_PAGE_ENDPOINT = BASE_URL + "/api/camps/campgrounds/{park_id}"

    headers = {"User-Agent": UserAgent().random}

    @staticmethod
    def get_availability(park_id, month_date):
        params = {"start_date": formatter.format_date(month_date)}
        LOG.debug("Querying for {} with these params: {}".format(park_id, params))
        url = RecreationClient.AVAILABILITY_ENDPOINT.format(park_id=park_id)
        resp = RecreationClient._send_request(url, params)
        return resp

    @staticmethod
    def get_park_name(park_id):
        resp = RecreationClient._send_request(RecreationClient.MAIN_PAGE_ENDPOINT.format(park_id=park_id), {})
        return resp["campground"]["facility_name"]

    @staticmethod
    def _send_request(url, params):
        resp = requests.get(url, params=params, headers=RecreationClient.headers)
        if resp.status_code != 200:
            raise RuntimeError(
                "failedRequest",
                "ERROR, {status_code} code received from {url}: {resp_text}".format(
                    status_code=resp.status_code,
                    url=url,
                    resp_text=resp.text
                ),
            )
        return resp.json()
