#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests
import re
import threading
import logging
from requests.auth import HTTPBasicAuth
from ConfigParser import SafeConfigParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('bathroomcommits.log')
handler.setLevel(logging.INFO)
logger.addHandler(handler)

parser = SafeConfigParser()
parser.read('bathroomcommits.ini')

# Required keys/tokens to access Twitter and GitHub
CONSUMER_KEY = parser.get('twitter', 'consumer.key')
CONSUMER_SECRET = parser.get('twitter', 'consumer.secret')
ACCESS_KEY = parser.get('twitter', 'access.key')
ACCESS_SECRET = parser.get('twitter', 'access.secret')
GITHUB_TOKEN = parser.get('github', 'token')

# Configuration info
allowedPhrases = [
    "shit",
    ":shit:",
    "shite",
    "shitty",
    "shitastic",
    "shittastic",
    "shit-tastic",
    "shitload",
    "bathroom",
    "toilet",
    "bowel",
    "fart",
    "fuckingshit",
    "bullshit",
    "horseshit"
]

avoidPhrases = [
    "Merge",
    "pull request"
]

wordBoundary = "\\b"
allowedPhrases = [wordBoundary + phrase + wordBoundary for phrase in allowedPhrases]
avoidPhrases = [wordBoundary + phrase + wordBoundary for phrase in avoidPhrases]

lastMessage = ""

# Connect to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# GitHub Variables
git_io_url = "https://git.io"
events_url = "https://api.github.com/events"

headers = {
    "User-Agent": "bathroomcommits",
    "ETag": "a18c3bded88eb5dbb5c849a489412bf3"
}

basicAuth = HTTPBasicAuth(GITHUB_TOKEN, "x-oauth-basic")


# Helper Methods
def get_commit_info(url):
    r = requests.get(url, headers=headers, auth=basicAuth)
    json = r.json()
    message = json['commit']['message']
    html_url = json['html_url']
    tweet = {
        "url": shorten_url(html_url),
        "message": message
    }
    return tweet


def check_commit(message):
    allowed_phrase_found = re.search("|".join(allowedPhrases), message, re.I | re.M)
    avoid_phrase_found = re.search("|".join(avoidPhrases), message, re.I | re.M)
    return len(message) < 125 and allowed_phrase_found and not avoid_phrase_found


def shorten_url(url):
    shortener_url = "/".join([git_io_url, "create"])
    form = {
        "url": url
    }
    r = requests.post(shortener_url, data=form)
    return "/".join([git_io_url, r.text])


def send_tweets(tweets):
    global lastMessage
    for tweet in tweets:
        commit_message = tweet['message']
        tweet_message = " ".join([commit_message, tweet['url']])
        # Ideally this will become some sort of set of commit URLs (before shortening) and it can be
        # stored in and read from a file
        if lastMessage != commit_message:
            lastMessage = commit_message
            logger.info("Sending tweet " + tweet_message)
            api.update_status(status=tweet_message)


# Look for commits
def poll():
    logger.debug("Starting commit check thread.")
    threading.Timer(5.0, poll).start()
    logger.debug("Looking for commits...")
    tweets = []
    r = requests.get(events_url, headers=headers, auth=basicAuth)
    # Find all push events
    indices = [i for i, x in enumerate(r.json()) if x['type'] == "PushEvent"]
    for i in indices:
        # Read the commits in the push event
        for commit in r.json()[i]['payload']['commits']:
            message = commit['message']
            # Check if the commit message meets the requirements
            if check_commit(message):
                # Generate tweet object
                url = commit['url']
                logger.debug("Found commit that meets criteria. URL: " + url)
                logger.debug("Commit message: " + message)
                tweet = get_commit_info(url)
                tweets.append(tweet)
    logger.debug("Sending out tweets.")
    send_tweets(tweets)

poll()