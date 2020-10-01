#!/usr/bin/env python3

import argparse
import json
import logging
from datetime import datetime, timedelta, date
import itertools
import time
import requests
from fake_useragent import UserAgent
from facilityparameters import *
import boto3

client = boto3.client('dynamodb')



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
                'S': value['main-page-endpoint'sfsafsa]
            }
        }
    )