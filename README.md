# Campsite Availability Scraping

**Thanks to https://github.com/bri-bri/yosemite-camping for getting me most of the way there.**

This script scrapes the https://recreation.gov website for campsite availabilities.

## Example Usage
```
$ python camping.py --start-date 2018-07-20 --end-date 2018-07-23 70926 70928 70925 71532
❌ TUOLUMNE MEADOWS, CA: 0 site(s) available out of 148 site(s)
🏕 LOWER PINES, CA: 11 site(s) available out of 73 site(s)
❌ UPPER PINES, CA: 0 site(s) available out of 235 site(s)
❌ BASIN MONTANA CAMPGROUND, MT: 0 site(s) available out of 30 site(s)
```

You can also read from stdin. Define a file (e.g. `parks.txt`) with IDs like this:
```
70926
70928
70925
71532
```
and then use it like this:
```
$ python camping.py --start-date 2018-07-20 --end-date 2018-07-23 --stdin < parks.txt
```

You'll want to put this script into a 5 minute crontab. You could also grep the output for the success emoji (🏕) and then do something in response, like notify you that there is a campsite available. See the "Twitter Notification" section below.

## Getting park IDs
What you'll want to do is go to https://recreation.gov/unifSearchResults.do and search for the campground you want. Click on it in the search sidebar. Once it comes up it should take you to a page with `campgroundDetails.do` or `campsiteSearch.do` in the URL.

### `campgroundDetails.do`
You should be able to see the `parkId` in the URL. Example:
```
https://www.recreation.gov/camping/tuolumne-meadows/r/campgroundDetails.do?contractCode=NRSO&parkId=70926
```
You can see the park ID right at the end there.

### `campsiteSearch.do`
Open your browser's dev tools and go to the network tab. Refresh the page and look for the POST request to `campsiteSearch.do`. Open the params tab for the request and you'll see the `parkId` there.

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

Feel free to submit pull requests, or look at the original: https://github.com/bri-bri/yosemite-camping

### Differences from the original
- Python 3 🐍🐍🐍.
- Park IDs not hardcoded, passed via the CLI instead.
- Doesn't give you URLs for campsites with availabilities.
- Works with any park out of the box, not just those in Yosemite like with the original.

## Twitter Notification
If you want to be notified about campsite availabilities via Twitter (they're the only API out there that is actually easy to use), you can do this:
1. Make an app via Twitter. It's pretty easy, go to: https://apps.twitter.com/app/new.
2. Change the values in `twitter_credentials.py` to match your key values.
3. Pipe the output of your command into `notifier.py`. See below for an example.

```
python camping.py --start-date 2018-07-20 --end-date 2018-07-23 70926 70928 | python notifier.py @banool1
```

You'll want to make the app on another account (like a bot account), not your own, so you get notified when the tweet goes out.

I left my API keys in here but don't exploit them ty thanks.
