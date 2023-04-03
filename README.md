# Campsite Availability Scraping

**This has been updated to work with the new recreation.gov site and API!!!**

This script scrapes the https://recreation.gov website for campsite availabilities.

**Note:** Please don't abuse this script. Most folks out there don't know how to run scrapers against websites, so you're at an unfair advantage by using this.

## Example Usage
```
$ python camping.py --start-date 2018-07-20 --end-date 2018-07-23 --parks 232448 232450 232447 232770
❌ TUOLUMNE MEADOWS: 0 site(s) available out of 148 site(s)
🏕 LOWER PINES: 11 site(s) available out of 73 site(s)
❌ UPPER PINES: 0 site(s) available out of 235 site(s)
❌ BASIN MONTANA CAMPGROUND: 0 site(s) available out of 30 site(s)
```

You can also read from stdin. Define a file (e.g. `parks.txt`) with park IDs like this:
```
232447
232449
232450
232448
```
and then use it like this:
```
$ python camping.py --start-date 2018-07-20 --end-date 2018-07-23 --stdin < parks.txt
```
For powershell, try this:
```
PS > Get-Content parks.txt | python camping.py --start-date 2021-09-24 --end-date 2022-09-24 --stdin
```

If you want to see more information about which campsites are available, pass `--show-campsite-info` along with `--nights <int>`:
```
$ python camping.py --start-date 2018-07-20 --end-date 2018-07-23 --parks 232448 232450 232447 232770 --show-campsite-info --nights 1 
There are campsites available from 2018-07-20 to 2018-07-23!!!
🏕 ELK CREEK CAMPGROUND (SAWTOOTH NF) (232042): 1 site(s) available out of 1 site(s)
  * Site 69800 is available on the following dates:
    * 2018-07-20 -> 2018-07-21 
    * 2018-07-21 -> 2018-07-22
```

If you only want results for certain campsite IDs, pass `--campsite-ids <int>`:
```bash
$ python camping.py --start-date 2018-07-20 --end-date 2018-07-23 --parks 232431 --show-campsite-info --nights 1 --campsite-ids 18621 
```

You'll want to put this script into a 5 minute crontab. You could also grep the output for the success emoji (🏕) and then do something in response, like notify you that there is a campsite available. See the "Twitter Notification" section below.

## Number of nights
If you're flexible on travel dates, you can search for a specific number of contiguous nights within a wide range of dates. This is useful for campgrounds in high-demand areas (like Yosemite Valley) or during peak season when openings are rare. Simply specify the `--nights` argument. For example, to search for a 5-day reservation in the month of June 2020 at Chisos Basin:
```
$ python camping.py --start-date 2020-06-01 --end-date 2020-06-30 --nights 5 234038
There are campsites available from 2020-06-01 to 2020-06-30!!!
🏕 CHISOS BASIN (BIG BEND) (234038): 13 site(s) available out of 62 site(s)
```

## Getting park IDs
What you'll want to do is go to https://recreation.gov and search for the campground you want. Click on it in the search sidebar. This should take you to a page for that campground, the URL will look like `https://www.recreation.gov/camping/campgrounds/<number>`. That number is the park ID.

## Getting campsite IDs
Go to https://recreation.gov and first search for the campground you want and then select the specific campsite within that campground. The URL for the campsite should look like `https://www.recreation.gov/camping/campsites/<number>`. That number is the campsite ID.

## Searching for availability at a specific campsite within a campground
You can search for availability at just a single specific campsite using the '--campsite-ids' argument. This can be useful if you have a favorite campsite you like to use or if you have a reservation at a specific campsite that you want to add days to before or after your existing reservation. This search only works for one campground/campsite combination at a time.
```
$ python camping.py --start-date 2020-06-01 --end-date 2020-06-30 --nights 5 --parks 234038 --campsite-ids 6943
There are campsites available from 2020-06-01 to 2020-06-30!!!
🏕 CHISOS BASIN (BIG BEND) (234038): 1 site(s) available out of 62 site(s)
```

You can also take [this site for a spin](https://pastudan.github.io/national-parks/). Thanks to [pastudan](https://github.com/pastudan)!

## Installation

I wrote this in Python 3.7 but I've tested it as working with 3.5 and 3.6 also.
```
python3 -m venv myvenv
source myvenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# You're good to go!
```

## Development
This code is formatted using black and isort:
```
black -l 80 --py36 camping.py
isort camping.py
```
Note: `black` only really supports 3.6+ so watch out!

Feel free to submit pull requests, or look at the original: https://github.com/bri-bri/yosemite-camping

### Running Tests

All tests should pass before a pull request gets merged. To run all the tests, cd into the project directory and run:
```bash
python -m unittest
``` 

### Differences from the original
- Python 3 🐍🐍🐍.
- Park IDs not hardcoded, passed via the CLI instead.
- Doesn't give you URLs for campsites with availabilities.
- Works with any park out of the box, not just those in Yosemite like with the original.
- **Update 2018-10-21:** Works with the new recreation.gov site.

## Twitter Notification
If you want to be notified about campsite availabilities via Twitter (they're the only API out there that is actually easy to use), you can do this:
1. Make an app via Twitter. It's pretty easy, go to: https://apps.twitter.com/app/new.
2. Change the values in `twitter_credentials.json` to match your key values.
3. Pipe the output of your command into `notifier.py`. See below for an example.

```
python camping.py --start-date 2018-07-20 --end-date 2018-07-23 --parks 70926 70928 | python notifier.py @banool1
```

You'll want to make the app on another account (like a bot account), not your own, so you get notified when the tweet goes out.

I left my API keys in here but don't exploit them ty thanks.

**Thanks to https://github.com/bri-bri/yosemite-camping for getting me most of the way there for the old version.**
