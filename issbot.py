import tweepy
import json
from keys import *
from weatherKey import *
import requests
import datetime
import time

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
                no_spaces = status_text.replace(' ','')
                test = cityToCoords(no_spaces)
                if type(test) is list:
                    reply = getPassTime(test)
                else:
                    reply = test
            else:
                reply = 'please give valid coordinates or city name.'

            try:
                api.update_status(status=reply, in_reply_to_status_id=status_id, auto_populate_reply_metadata=True)
            except tweepy.TweepError:
                time.sleep(60*2)


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

def cityToCoords(city):
    response_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}'.format(city, weatherKey))
    data = response_weather.json()
    if data['cod'] == 200:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        coords = [lat, lon]
        return coords
    else:
        error = 'The location you provided was not found'
        return error

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
            lat = parameters['lat']
            lon = parameters['lon']
            return '({0}, {1}){2}{2}{3} for {4:.1f} seconds'.format(lat, lon, '\n', risetimeread, duration)
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
