# Twitter Bot

Example Bot: https://twitter.com/bathroomcommits

This is a simple Twitter bot that is currently set to read commits from GitHub and tweet any of those commits that meet
certain criteria

## Requirements

The Python Twitter bot requires Tweepy to run. You can get Tweepy from pip.

```
sudo apt-get install python-pip
pip install tweepy
```

## Running Twitter Bot

`python twitterbot.py`.

## Settings

The format of the `twitterbot.ini` file is as follows:

```
[twitter]
consumer.key =
consumer.secret =
access.key =
access.secret =

[github]
token =

[bot]
user.agent =
etag =
allowed.phrases =
avoid.phrases =
```

The allowed.phrases and avoid.phrases properties are comma-separated lists

## Example Bot Config

```
[twitter]
consumer.key = <your consumer key>
consumer.secret = <your consumer secret>
access.key = <your access key>
access.secret = <your access secret>

[github]
token = <your GitHub token>

[bot]
user.agent = bathroomcommits
etag = a18c3bded88eb5dbb5c849a489412bf3
allowed.phrases = bathroom, toilet
avoid.phrases = merge, pull request
```