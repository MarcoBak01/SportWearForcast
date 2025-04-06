from datetime import datetime, timedelta
import requests
import sys
from math import floor

import json
from constants import OUT_DIR, FILE_NAME, API_KEY
from pprint import pprint
from weather_rule import TemperatureRule, WindRule, RainRule, ThunderStormRule, UVIndexRule


def main():
  # TODO: Make sure to enter location manualy, and inporperate it in the json file name if that is possible.
  # TODO: put them all in one file again for now, there are more then anough api calls for each day.

  location = input("Please input your location: ") # "Delft"
       
  day = datetime.today().strftime("%Y-%m-%d")
  weather_data = get_weather_data(location, day)  
  
  rules = [
    TemperatureRule(min_temp=-5, max_temp=8, action="Wear long sport pants, long-sleeve shirt, jacket, and gloves"),
    TemperatureRule(min_temp=8, max_temp=20, action="Wear a T-shirt and lightweight jacket, consider long pants depending on the wind"),
    TemperatureRule(min_temp=20, max_temp=100, action="Wear shorts and a lightweight top"),
    
    WindRule(min_wind_speed=25, action="Consider adding a windproof jacket or vest"),
    
    RainRule(action="Wear a waterproof jacket and consider a cap"),
    ThunderStormRule(action="There is a thunderstorm, now is maybe not the best time to go outside"),
  ]
  suggestions = []
  for rule in rules:
      suggestion = rule.apply(weather_data)
      if suggestion:
          suggestions.append(suggestion)
  print(f"Weather summary of today: {weather_data['weather'][0]['description']}")
  print(f"Further breakdown of the weather in {location}:")
  for item in suggestions:
      print(f"- {item}")

def get_weather_data(location, day):
  location = get_location(location)
  
  response = requests.request("GET", f"https://api.openweathermap.org/data/2.5/weather?units=metric&lat={location['lat']}&lon={location['lon']}&appid={API_KEY}")
  if response.status_code!=200:
    print('Unexpected Status code: ', response.text)
    sys.exit()
  pprint(response.json())
  return response.json()

def get_location(location, country_code="NL", n=1):
  print(API_KEY)
  response = requests.request("GET", f"http://api.openweathermap.org/geo/1.0/direct?q={location},{country_code}&limit={n}&appid={API_KEY}")
  if response.status_code!=200:
    print('Unexpected Status code getting location: ', response.text)
    sys.exit()
    
  return response.json()[0]


if __name__ == '__main__':
    main()
