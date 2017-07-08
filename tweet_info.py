import tweepy
import json
from keys import *
import requests
import datetime

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
public_tweets = api.home_timeline()
# print public_tweets[0].text
# print public_tweets[0].text[:2]
# for tweet in public_tweets:
#     tweet_json_string = json.dumps(tweet._json, indent=4)
    # tweet_json_object = json.loads(tweet_json_string)
    # print tweet_json_string
    # print tweet.text

# test_accounts = ['issTrackerPy', 'test1_daniel']
# for account in test_accounts:
#     timeline = api.user_timeline(account)
#     print account
#     for tweet in timeline:
#         print tweet.text

parameters = {'lat': 80, 'lon': 80}
# parameters = {'lat': 27.9506, 'lon': -82.4572}
response_pass = requests.get('http://api.open-notify.org/iss-pass.json', params=parameters)
print response_pass.content
# data = response_pass.json()
# print data['message']
# print '500 Internal Server Error' in response_pass.content
# print data
