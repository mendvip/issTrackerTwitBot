import tweepy
import json
from keys import *

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    tweet_json_string = json.dumps(tweet._json, indent=4)
    tweet_json_object = json.loads(tweet_json_string)
    print tweet_json_string
