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
            print len(status.text)
            if len(status.text) > 14:
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
                    coords_and_city = cityToCoords(no_spaces)
                    if status_text[0] == '(':
                        reply = 'please do not use parentheses'
                    elif type(coords_and_city) is list:
                        if len(coords_and_city) == 3:
                            coords = coords_and_city[:2]
                            cityname = coords_and_city[2]
                            reply = getPassTime(coords, cityname=cityname)
                        else:
                            reply = getPassTime(coords_and_city)
                    else:
                        reply = coords_and_city
                else:
                    reply = 'please give valid coordinates or city name.'
            else:
                reply = 'please provide valid location'
            try:
                api.update_status(status=reply, in_reply_to_status_id=status_id, auto_populate_reply_metadata=True)
            except tweepy.TweepError:
                time.sleep(60*2)


def notBlank(tweet):
    if len(tweet) > 0:
        return True
    else:
        return False

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
        cityname = data['name']
        coords = [lat, lon, cityname]
        return coords
    else:
        error = 'The location you provided was not found'
        return error

def getPassTime(coords, **kwargs):
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
            if kwargs and 'cityname' in kwargs:
                tweet = '{5}{2}({0}, {1}){2}{3} UTC for {4:.1f} seconds'.format(lat, lon, '\n', risetimeread, duration, kwargs['cityname'])
            else:
                tweet = '({0}, {1}){2}{3} UTC for {4:.1f} seconds'.format(lat, lon, '\n', risetimeread, duration)
            return tweet
        else:
            return data['reason']

    except ValueError:
        return 'The ISS will not be passing over that location in the near future'



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['@issTrackerPy', '@isstrackerpy'])
