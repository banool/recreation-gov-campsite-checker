import random
import sys
import time

from camping import SUCCESS_EMOJI
from twitter_credentials import twitter_credentials as tc

import twitter

MAX_TWEET_LENGTH = 279
DELAY_FILE = "next.txt"
DELAY_TIME = 180

# Janky simple argument parsing.
if len(sys.argv) != 2:
    print("Please provide the user you want to tweet at!")
    sys.exit(1)

try:
    with open(DELAY_FILE, "r") as f:
        call_time = int(f.read().rstrip())
except:
    call_time = 0

if call_time + random.randint(DELAY_TIME-10, DELAY_TIME+10) > int(time.time()):
   print("It is too soon to tweet again") 
   sys.exit(0)

user = sys.argv[1].replace("@", "")

first_line = next(sys.stdin)

available_site_strings = []
for line in sys.stdin:
    line = line.strip()
    if SUCCESS_EMOJI in line:
        name = " ".join(line.split(":")[0].split(" ")[1:])
        available = line.split(":")[1][1].split(" ")[0]
        s = "{} site(s) available in {}".format(available, name)
        available_site_strings.append(s)

if available_site_strings:
    api = twitter.Api(
        consumer_key=tc["consumer_key"],
        consumer_secret=tc["consumer_secret"],
        access_token_key=tc["access_token_key"],
        access_token_secret=tc["access_token_secret"],
    )
    tweet = "@{}!!! ".format(user)
    tweet += first_line.rstrip()
    tweet += " 🏕🏕🏕\n"
    tweet += "\n".join(available_site_strings)
    tweet += "\n" + "🏕" * random.randint(5, 20)  # To avoid duplicate tweets.
    tweet = tweet[:MAX_TWEET_LENGTH]
    resp = api.PostUpdate(tweet)
    api.CreateFavorite(resp)
    print("The following was tweeted: ")
    print()
    print(tweet)
    with open(DELAY_FILE, "w") as f:
        f.write(str(int(time.time())))
else:
    print("No campsites available, not tweeting 😞")
