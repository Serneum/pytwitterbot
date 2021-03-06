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

#### Automatically Starting Your Bot
twitterbot.conf is a template Upstart script that can be used in Ubuntu. You need to supply a username and a path to your bot, then move it to /etc/init.

###### Sample Upstart Script
```
author "Chris Rees <serneum@gmail.com>"
description "Upstart Script to start the Python Twitter bot"

#Set username for the process.
setuid user

start on runlevel [2345]
stop on runlevel [016]

#Set the base directory for your twitter bot
env DIR=/opt/twitterbot

respawn

exec python $DIR/twitterbot.py
```

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
#### Twitter
You can get all of the information you need for the Twitter section of the .ini file at https://apps.twitter.com. You can follow the first half of [this guide](http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/) if you need any help with creating a Twitter application and obtaining the keys. 

#### GitHub
You can get the GitHub token by creating a new [personal access token](https://github.com/settings/applications).

#### Bot
Your bot's user agent should be your [username or the name of your application](https://developer.github.com/v3/#user-agent-required).

The [ETag](http://en.wikipedia.org/wiki/HTTP_ETag) is just a unique hash used when making requests.

The allowed.phrases and avoid.phrases properties are comma-separated lists

## Example Bot Config

```
[twitter]
consumer.key = abc123
consumer.secret = abc123
access.key = abc123
access.secret = abc123

[github]
token = abc123

[bot]
user.agent = bathroomcommits
etag = d18c3bded99eb5dbb5c849a489412bf5
allowed.phrases = bathroom, toilet
avoid.phrases = merge, pull request
```

## Example Bots
[Bathroom Commits](https://twitter.com/bathroomcommits)  
[Swag Commits](https://twitter.com/swagcommits)  
[Brommits](https://twitter.com/brommits)
