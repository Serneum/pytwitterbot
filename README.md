# Twitter Bot

Example Bot: https://twitter.com/bathroomcommits

This is a simple Twitter bot that reads commits from GitHub and tweets any of those commits that meet
certain criteria

## Requirements

The Python Twitter bot requires Tweepy to run. You can get Tweepy from pip.

```
sudo apt-get install python-pip
pip install tweepy
```

## Running Twitter Bot

`./start.sh`

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
user.agent = <your user agent>
etag = <your ETag>
allowed.phrases = bathroom, toilet
avoid.phrases = merge, pull request
```
