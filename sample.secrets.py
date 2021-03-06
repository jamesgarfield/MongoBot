# Basic

CHANNEL = ''
IDENT = ''
REALNAME = ''
OWNER = ''


# Password for users to register with the bot

BOT_PASS = ''


# Simple APIs

WEATHER_API = ''
WORDNIK_API = ''
FML_API = ''
WOLFRAM_API = ''


# Meetups

MEETUP_LOCATION = '' # Information about the location goes here
MEETUP_NOTIFY = [12, 17] # Hours to notify on day of
MEETUP_DAY = '2nd Wednesday' # <-- format like this

# Server

HTTP_USER = ''
HTTP_PASS = ''


# Reddit

REDDIT_APPID = ''
REDDIT_SECRET = ''


# Delicious

DELICIOUS_USER = ''
DELICIOUS_PASS = ''


# Twilio stuff

TWILIO_SID = ''
TWILIO_TOKEN = ''
TWILIO_NUMBER = ''

# Safe numbers can send commands 
# to mongo via text message
SAFE_NUMBERS = {
    '+1234567890': 'irc_nick',
}


# Google

GOOGLE_USER = ''
GOOGLE_PASS = ''


# Facebook

FB_USER = GOOGLE_USER + '@gmail.com'
FB_PASS = ''
FB_PAGE = ''

FB_MONGOBOT_APPID = ''
FB_MONGOBOT_SECRET = ''


# Twitter

TWIT_USER = GOOGLE_USER + '@gmail.com'
TWIT_PASS = ''
TWIT_PAGE = ''

TWIT_CONSUMER_KEY = ''
TWIT_CONSUMER_SECRET = ''
TWIT_ACCESS_TOKEN = ''
TWIT_ACCESS_SECRET = ''


# Github. Nothing built for this yet

GITHUB_CLIENT_ID = ''
GITHUB_CLIENT_SECRET = ''
GITHUB_TOKEN = ''


# Marvel. This will be awesome at some point.

MARVEL_PUBLIC_KEY = ""
MARVEL_PRIVATE_KEY = ""
