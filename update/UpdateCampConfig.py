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
from update.parameters import *
from update.facilityparameters import *
from dateutil.relativedelta import relativedelta
import calendar
import boto3

client = boto3.client('dynamodb')
count = 0

for key, value in campgrounds.items():
    response = client.put_item(
        TableName='campsiteconfig',
        Item={
            'facility-name': {
                'S': 'recreation.gov'},
            'campsite-name': {
                'S': key},
            'campsite-id': {
                'S': value}
        }
    )
    print (key +", " + value)
    count += 1
    print (count)
    if count >=480:
        time.sleep(60)
        count = 0


for key, value in facility.items():
    response = client.put_item(
        TableName='facilityconfig',
        Item={
            'facility-name': {
                'S': 'recreation.gov'},
            'base-url': {
                'S': value['base-url']},
            'availability-endpoint': {
                'S': value['availability-endpoint']},
            'main-page-endpoint': {
                'S': value['main-page-endpoint']
            }
        }
    )