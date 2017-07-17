import tweepy
import json
from keys import *
from weatherKey import *
import requests
import datetime

#todo
#research async
#test deploy to pythonanywhere

response_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=testing&APPID={}'.format(weatherKey))
print response_weather.json()
print json.dumps(response_weather.json(), indent=4)
data = response_weather.json()
if data['cod'] == 200:
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    coords = [lat, lon]
    # print type(coords)
else:
    error = 'The location you provided was not found'
    print error
