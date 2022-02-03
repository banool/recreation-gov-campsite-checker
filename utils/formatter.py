from datetime import datetime

from enums.date_format import DateFormat


def format_date(
    date_object, format_string=DateFormat.ISO_DATE_FORMAT_REQUEST.value
):
    """
    This function doesn't manipulate the date itself at all, it just
    formats the date in the format that the API wants.
    """
    date_formatted = datetime.strftime(date_object, format_string)
    return date_formatted


def site_date_to_human_date(date_string):
    date_object = datetime.strptime(
        date_string, DateFormat.ISO_DATE_FORMAT_RESPONSE
    )
    return format_date(
        date_object, format_string=DateFormat.INPUT_DATE_FORMAT.value
    )
