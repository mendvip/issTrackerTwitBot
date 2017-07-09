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

parameters = {'lat': 'a', 'lon': 80}
# parameters = {'lat': 27.9506, 'lon': -82.4572}
response_pass = requests.get('http://api.open-notify.org/iss-pass.json', params=parameters)
print response_pass.content
try:
    data = response_pass.json()
    message = data['message']
    if message == 'success':
        response = data['response'][0]
        risetime = response['risetime']
        duration = float(response['duration'])/100
        risetimeval = datetime.datetime.fromtimestamp(risetime)
        risetimeread = risetimeval.strftime('%m/%d/%Y %I:%M:%S %p')
        print '{0} for {1} seconds'.format(risetimeread, duration)
    else:
        print 'please use correct format'
except ValueError:
    pIndex = response_pass.content.find('<p>')
    periodIndex = response_pass.content.find('.', 42)
    print response_pass.content[pIndex+3 : periodIndex]
