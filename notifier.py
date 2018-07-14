import random
import sys

from camping import SUCCESS_EMOJI
from twitter_credentials import twitter_credentials as tc

import twitter

MAX_TWEET_LENGTH = 279

# Janky simple argument parsing.
if len(sys.argv) != 2:
    print("Please provide the user you want to tweet at!")
    sys.exit(1)

user = sys.argv[1].replace("@", "")

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
    tweet = "@{}, there are campsites available! 🏕🏕🏕\n{}".format(
        user,
        "\n".join(available_site_strings),
    )
    tweet += "\n" + "🏕" * random.randint(5, 20)  # To avoid duplicate tweets.
    tweet = tweet[:MAX_TWEET_LENGTH]
    resp = api.PostUpdate(tweet)
    api.CreateFavorite(resp)
    print("The following was tweeted: ")
    print(tweet)
else:
    print("No campsites available, not tweeting 😞")
