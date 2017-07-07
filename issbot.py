import tweepy
import json
from keys import *

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not isRetweet(status.text):
            username = status.user.screen_name
            status_id = status.id
            status_text = status.text
            coords = status_text[14:].split(',')
            if coords[1][0] == ' ':
                coords[1] = coords[1][1:]
            print coords
            print coords[1][0]
            reply = 'thank you. we are still in testing.'
            # api.update_status(status=reply, in_reply_to_status_id=status_id, auto_populate_reply_metadata=True)

def isRetweet(tweet):
    if tweet[:2] == 'RT':
        return True
    else:
        return False

def stringOrNum(tweet):
    try:
        int(tweet[0])
        return 'num'
    except ValueError:
        return 'string'

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['@issTrackerPy', '@isstrackerpy'])
