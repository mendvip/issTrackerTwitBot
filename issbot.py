import tweepy
import json
from keys import *

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     # tweet_json_string = json.dumps(tweet._json, indent=4)
#     # tweet_json_object = json.loads(tweet_json_string)
#     # print tweet_json_string
#     print tweet.text

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not status.retweeted:
            username = status.user.screen_name
            status_id = status.id
            reply = 'thank you. we are still in testing.'
            print 'test'
            #api.update_status

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['@issTrackerPy', '@isstrackerpy'], async=True)
