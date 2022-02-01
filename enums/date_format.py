from enum import Enum


class DateFormat(Enum):
    INPUT_DATE_FORMAT = "%Y-%m-%d"
    ISO_DATE_FORMAT_REQUEST = "%Y-%m-%dT00:00:00.000Z"
    ISO_DATE_FORMAT_RESPONSE = "%Y-%m-%dT00:00:00Z"
