#!/usr/bin/env python3

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta, date
import itertools
import time
import requests
from fake_useragent import UserAgent
from parameters import *
from dateutil.relativedelta import relativedelta
import calendar
import boto3

LOG = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(process)s - %(levelname)s - %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(formatter)
LOG.addHandler(sh)

client = boto3.client('dynamodb')

response = client.get_item(
    TableName='campgrounds'
)
print (response)


BASE_URL = "https://www.recreation.gov"
AVAILABILITY_ENDPOINT = "/api/camps/availability/campground/"
MAIN_PAGE_ENDPOINT = "/api/camps/campgrounds/"

INPUT_DATE_FORMAT = "%Y-%m-%d"

headers = {"User-Agent": UserAgent().random}