#!/usr/bin/env python
# encoding: utf-8
import json
import os

import tweepy
import csv

from utils import get_config
from utils import URL_LIST_PATH, LAST_IDS_JSON, TWEETS_PATH

conf = get_config()

# Twitter API credentials
consumer_key = conf["twitter"]["consumer_key"]
consumer_secret = conf["twitter"]["consumer_secret"]
access_key = conf["twitter"]["access_key"]
access_secret = conf["twitter"]["access_secret"]


def get_new_tweets(screen_name, last_id=None):
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    if not last_id:
        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    else:
        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, since_id=last_id)

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [(tweet.id_str, tweet.created_at, tweet.text) for tweet in new_tweets]

    # write the csv
    with open(TWEETS_PATH, 'at') as f:
        writer = csv.writer(f)
        writer.writerows(outtweets)

    return outtweets[-1][0]  # last received tweet id


def get_name_and_last_id():
    names = []
    with open(URL_LIST_PATH) as f:
        for line in f:
            l = line.strip()
            if l:
                names.append(l.strip("/")[-1])

    if not os.path.exists(LAST_IDS_JSON):
        last_ids = dict([(x, None) for x in names])
    else:
        with open(LAST_IDS_JSON) as f:
            last_ids = json.load(f)
        for name in names:
            if name not in last_ids:
                last_ids[name] = None

    return last_ids


if __name__ == '__main__':
    if not os.path.exists(TWEETS_PATH):
        with open(TWEETS_PATH, "wt") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text"])

    last_ids = get_name_and_last_id()
    new_last_ids = {}
    for name, last_id in last_ids.items():
        new_last_id = get_new_tweets(name, last_id)
        new_last_ids[name] = new_last_id
