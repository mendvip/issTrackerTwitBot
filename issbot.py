import tweepy
import json
from keys import *
import requests
import datetime

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not isRetweet(status.text):
            username = status.user.screen_name
            status_id = status.id
            status_text = status.text[14:]

            if stringOrNum(status_text) == 'num':
                if ',' in status.text:
                    coords = status_text.split(',')
                    if coords[1][0] == ' ':
                        coords[1] = coords[1][1:]
                    reply = getPassTime(coords)
                else:
                    reply = 'please use correct format. Ex: 27.95, -82.45'

            elif stringOrNum(status_text) == 'string':
                reply = 'this is a string'
            else:
                reply = 'please give valid coordinates or city name.'

            api.update_status(status=reply, in_reply_to_status_id=status_id, auto_populate_reply_metadata=True)

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

def getPassTime(coords):
    parameters = {'lat': coords[0], 'lon': coords[1]}
    response_pass = requests.get('http://api.open-notify.org/iss-pass.json', params=parameters)
    try:
        data = response_pass.json()
        message = data['message']
        if message == 'success':
            response = data['response'][0]
            risetime = response['risetime']
            duration = float(response['duration'])/100
            risetimeval = datetime.datetime.fromtimestamp(risetime)
            risetimeread = risetimeval.strftime('%m/%d/%Y %I:%M:%S %p')
            return '{0} for {1} seconds'.format(risetimeread, duration)
        else:
            return data['reason']

    except ValueError:
        # pIndex = response_pass.content.find('<p>')
        # periodIndex = response_pass.content.find('.', 42)
        # return response_pass.content[pIndex+3 : periodIndex]
        return 'The ISS will not be passing over that location in the near future'



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['@issTrackerPy', '@isstrackerpy'])
