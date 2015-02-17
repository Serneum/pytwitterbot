#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, requests, json, re, threading, logging
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
  "bathroom",
  "toilet"
];

avoidPhrases = [
  "Merge pull request"
];

lastTweet = ""

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

# Helper Methods
def checkCommit(message):
  allowedPhraseFound = re.search("|".join(allowedPhrases), message, re.I|re.M)
  avoidPhraseFound = re.search("|".join(avoidPhrases), message, re.I|re.M)
  return len(message) < 125 and allowedPhraseFound and not avoidPhraseFound

def shortenUrl(url):
  shortenerURL = "/".join([git_io_url, "create"])
  form = {
    "url": url
  }
  r = requests.post(shortenerURL, data=form)
  return "/".join([git_io_url, r.text])

def sendTweets(tweets):
  for tweet in tweets:
    message = " ".join([tweet['message'], tweet['url']])
    logger.info("Sending tweet " + message)
    api.update_status(message)

# Look for commits
def poll():
  logger.debug("Starting commit check thread.")
  threading.Timer(5.0, poll).start()
  logger.debug("Looking for commits...")
  tweets = []
  r = requests.get(events_url, headers=headers, auth=(GITHUB_TOKEN, "x-oauth-basic"))
  # Find all push events
  indices = [i for i, x in enumerate(r.json()) if x['type'] == "PushEvent"]
  for i in indices:
    json = r.json()[i]
    # Read the commits in the push event
    for commit in json['payload']['commits']:
      message = commit['message']
      # Check if the commit message meets the requirements
      if checkCommit(message):
        # Generate tweet object
        html_url = json['html_url']
        logger.debug("Found commit that meets criteria. URL: " + html_url)
        logger.debug("Commit message: " + message)
        tweet = {
          "url": shortenUrl(json['html_url']),
          "message": message
        }
        tweets.append(tweet)
  logger.debug("Sending out tweets.")
  sendTweets(tweets)

poll()

