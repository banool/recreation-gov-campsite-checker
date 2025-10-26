# -*- coding: utf-8 -*-
import json
import random
import sys
import time
from hashlib import md5
from os import isatty

import twitter

from enums.emoji import Emoji

MAX_TWEET_LENGTH = 279
DELAY_FILE_TEMPLATE = "next_{}.txt"
DELAY_TIME = 1800
CREDENTIALS_FILE = "twitter_credentials.json"


def _create_tweet(tweet, tc):
    tweet = tweet[:MAX_TWEET_LENGTH]
    api = twitter.Api(
        consumer_key=tc["consumer_key"],
        consumer_secret=tc["consumer_secret"],
        access_token_key=tc["access_token_key"],
        access_token_secret=tc["access_token_secret"],
    )
    resp = api.PostUpdate(tweet)
    # api.CreateFavorite(resp)
    print("The following was tweeted: ")
    print()
    print(tweet)


def main(args, stdin):
    with open(CREDENTIALS_FILE) as f:
        tc = json.load(f)

    # Janky simple argument parsing.
    if len(args) != 2:
        print("Please provide the user you want to tweet at!")
        sys.exit(1)

    user = args[1].replace("@", "")

    first_line = next(stdin)
    print(first_line)
    first_line_hash = md5(first_line.encode("utf-8")).hexdigest()

    delay_file = DELAY_FILE_TEMPLATE.format(first_line_hash)
    try:
        with open(delay_file, "r") as f:
            call_time = int(f.read().rstrip())
    except:
        call_time = 0

#    if call_time + random.randint(DELAY_TIME - 30, DELAY_TIME + 30) > int(
#        time.time()
#    ):
#        print("It is too soon to tweet again")
#        sys.exit(0)

    if "Something went wrong" in first_line:
        _create_tweet("{}, I'm broken! Please help :'(".format(user), tc)
        sys.exit()

    available_site_strings = generate_availability_strings(stdin)

    if available_site_strings:
        tweet = generate_tweet_str(available_site_strings, first_line, user)
        _create_tweet(tweet, tc)
        with open(delay_file, "w") as f:
            f.write(str(int(time.time())))
        sys.exit(0)
    else:
        print("No campsites available, not tweeting 😞")
        sys.exit(1)


def generate_tweet_str(available_site_strings, first_line, user):
    tweet = "@{}!!! ".format(user)
    tweet += first_line.rstrip()
    tweet += " 🏕🏕🏕\n"
    tweet += "\n".join(available_site_strings)
    tweet += "\n" + "🏕" * random.randint(5, 20)  # To avoid duplicate tweets.
    return tweet


def generate_availability_strings(stdin):
    available_site_strings = []
    linkedSites = 0
    for line in stdin:
        line = line.strip()
        if Emoji.SUCCESS.value in line:
            park_name_and_id = " ".join(line.split(":")[0].split(" ")[1:])
            num_available = line.split(":")[1][1].split(" ")[0]
            s = "{} site(s) available in {}".format(
                num_available, park_name_and_id
            )
            available_site_strings.append(s)
        if "https" in line and linkedSites < 3:
            index = line.find("camping") - 1
            available_site_strings.append(line[index:])
            linkedSites += 1
    return available_site_strings


if __name__ == "__main__":
    main(sys.argv, sys.stdin)
