#!/bin/sh
#this script sets the environment and calls the camping script
cd /Users/smarthealth/Documents/rec_check
source myvenv/bin/activate
python3 camping.py --start-date 2022-02-04 --end-date 2022-02-05 --parks 232472 272300 232470 | python3 notifier2.py @campbot4
python3 camping.py --start-date 2022-02-05 --end-date 2022-02-06 --parks 232472 272300 232470 | python3 notifier2.py @campbot4
