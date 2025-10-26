#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point for running campsite checks from Node.js backend.
Accepts JSON configuration and outputs structured JSON results.
"""

import json
import logging
import sys
from datetime import datetime

from camping import (
    check_park,
    remove_comments,
)
from enums.date_format import DateFormat
from email_notifier import send_email_notification, load_email_config

LOG = logging.getLogger(__name__)
log_formatter = logging.Formatter(
    "%(asctime)s - %(process)s - %(levelname)s - %(message)s"
)
sh = logging.StreamHandler(sys.stderr)  # Log to stderr so stdout is clean JSON
sh.setFormatter(log_formatter)
LOG.addHandler(sh)


def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, DateFormat.INPUT_DATE_FORMAT.value)


def run_check(config):
    """
    Run a single campsite availability check based on configuration.
    
    Args:
        config: Dict containing:
            - parks: List of park IDs (integers)
            - startDate: Start date (YYYY-MM-DD)
            - endDate: End date (YYYY-MM-DD)
            - nights: Number of consecutive nights
            - weekendsOnly: Boolean
            - campsiteType: Optional string
            - campsiteIds: Optional list of integers
            - excludedDates: Optional list of dates (YYYY-MM-DD)
            - exclusionFile: Optional path to file with excluded site IDs
            - emailNotifications: Boolean
            - debug: Boolean
    
    Returns:
        Dict containing results in JSON format
    """
    try:
        # Parse configuration
        parks = config.get('parks', [])
        start_date = parse_date(config.get('startDate'))
        end_date = parse_date(config.get('endDate'))
        nights = config.get('nights', 1)
        weekends_only = config.get('weekendsOnly', False)
        campsite_type = config.get('campsiteType')
        campsite_ids = config.get('campsiteIds', [])
        excluded_dates_str = config.get('excludedDates', [])
        exclusion_file = config.get('exclusionFile')
        email_notifications = config.get('emailNotifications', False)
        debug = config.get('debug', False)
        
        if debug:
            LOG.setLevel(logging.DEBUG)
        
        # Parse excluded dates
        excluded_dates = []
        if excluded_dates_str:
            excluded_dates = [parse_date(d) for d in excluded_dates_str]
        
        # Load excluded site IDs from file if provided
        excluded_site_ids = []
        if exclusion_file:
            try:
                with open(exclusion_file, 'r') as f:
                    excluded_site_ids = f.readlines()
                    excluded_site_ids = [l.strip() for l in excluded_site_ids]
                    excluded_site_ids = remove_comments(excluded_site_ids)
            except FileNotFoundError:
                LOG.warning(f"Exclusion file not found: {exclusion_file}")
        
        # Check each park
        info_by_park_id = {}
        for park_id in parks:
            info_by_park_id[str(park_id)] = check_park(
                park_id,
                start_date,
                end_date,
                campsite_type,
                tuple(campsite_ids),
                nights=nights,
                weekends_only=weekends_only,
                excluded_site_ids=excluded_site_ids,
                excluded_dates=excluded_dates,
            )
        
        # Build results
        has_availabilities = False
        parks_data = []
        
        for park_id, info in info_by_park_id.items():
            current, maximum, available_dates_by_site_id, park_name = info
            
            if current > 0:
                has_availabilities = True
            
            # Convert available dates to serializable format
            available_sites = {}
            for site_id, dates in available_dates_by_site_id.items():
                available_sites[str(site_id)] = dates
            
            parks_data.append({
                'parkId': park_id,
                'parkName': park_name,
                'current': current,
                'maximum': maximum,
                'availableSites': available_sites
            })
        
        # Send email notification if configured and sites are available
        if has_availabilities and email_notifications:
            email_config = load_email_config()
            if email_config:
                available_parks = {k: v for k, v in info_by_park_id.items() if v[0] > 0}
                send_email_notification(available_parks, email_config)
        
        # Return structured results
        result = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'hasAvailability': has_availabilities,
            'parks': parks_data,
            'searchParams': {
                'startDate': config.get('startDate'),
                'endDate': config.get('endDate'),
                'nights': nights
            }
        }
        
        return result
        
    except Exception as e:
        LOG.error(f"Error running check: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Main entry point - reads JSON config from command line arg."""
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'No configuration provided. Usage: camping_runner.py <json_config>'
        }))
        sys.exit(1)
    
    try:
        # Parse JSON configuration from command line argument
        config_json = sys.argv[1]
        config = json.loads(config_json)
        
        # Run the check
        result = run_check(config)
        
        # Output JSON result to stdout
        # Always exit with 0 so monitoring continues, error info is in JSON
        print(json.dumps(result))
        sys.exit(0)
        
    except json.JSONDecodeError as e:
        print(json.dumps({
            'success': False,
            'error': f'Invalid JSON configuration: {e}',
            'timestamp': datetime.now().isoformat()
        }))
        sys.exit(0)  # Exit with 0 so monitoring continues
    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }))
        sys.exit(0)  # Exit with 0 so monitoring continues


if __name__ == '__main__':
    main()

