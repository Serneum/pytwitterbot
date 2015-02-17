#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, requests, json, re, threading, logging
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
  "bathroom",
  "toilet",
  "bowel",
  "fart",
  "gastro"
];

avoidPhrases = [
  "Merge pull request",
  "farther",
  "shitake",
  "naoshita"
];

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
def getCommitInfo(url):
  r = requests.get(url, headers=headers, auth=basicAuth)
  json = r.json()
  message = json['commit']['message']  
  htmlUrl = json['html_url']
  tweet = {
    "url": shortenUrl(htmlUrl),
    "message": message
  }
  return tweet

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
  global lastMessage
  for tweet in tweets:
    message = " ".join([tweet['message'], tweet['url']])
    if lastMessage != message:
      lastMessage = message
      logger.info("Sending tweet " + message)
      api.update_status(status=message)

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
      if checkCommit(message):
        # Generate tweet object
        url = commit['url']
        logger.debug("Found commit that meets criteria. URL: " + url)
        logger.debug("Commit message: " + message)
        tweet = getCommitInfo(url)
        tweets.append(tweet)
  logger.debug("Sending out tweets.")
  sendTweets(tweets)

poll()

