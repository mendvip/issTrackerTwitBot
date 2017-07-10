import tweepy
import json
from keys import *
from weatherKey import *
import requests
import datetime

#todo
#work with openweathermap current weather api to convert city names to lat, lon coords

response_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=miami&APPID={}'.format(weatherKey))
# print response_weather.json()
print json.dumps(response_weather.json(), indent=4)
data = response_weather.json()
lat = data['coord']['lat']
lon = data['coord']['lon']
coords = [lat, lon]
print coords
