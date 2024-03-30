from datetime import datetime, timedelta
import requests
import sys
from math import floor

import json
from constants import OUT_DIR, FILE_NAME
from pprint import pprint


def main():
  # TODO: Make sure to enter location manualy, and inporperate it in the json file name if that is possible.
  # TODO: put them all in one file again for now, there are more then anough api calls for each day.

  location = input("Please input your location: ") # "Delft"
  activity_duration = None
  while activity_duration is None:
    duration_input = input("Please enter the expected duration (in hours): ") # 3
    if duration_input.isnumeric():
      activity_duration = int(duration_input)
    else:
      print(f"Please only enter a whole number for the duration, try again.")
  
  activity_type = None
  while activity_type is None:
    activity_input = input("Please input your activity (biking or running): ")
    if activity_input.lower() in ["biking", "running"]:
      activity_type = duration_input
    else:
      print(f'Please only enter "biking" or "running", try again.')
  day = datetime.today().strftime("%Y-%m-%d")
  weather_data = get_weather_data(location, day) 

  # with open(f'{OUT_DIR}/{FILE_NAME}', 'w') as outfile:
  #     json.dump(weather_data, outfile)

  # with open(f'{OUT_DIR}/{FILE_NAME}') as json_file:
  #     weather_data = json.load(json_file)

  weather_today = weather_data['days'][0]

  day = weather_today["datetime"]

  weather_hourly = weather_today['hours']

  start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  end_activity_dt = datetime.now() + timedelta(hours=activity_duration+1)
  end_activity = end_activity_dt.strftime("%Y-%m-%d %H:%M:%S")
  relevant_weather_data = [data_point for data_point in weather_hourly if start_time < f"{day} {data_point['datetime']}" < end_activity]


  # pprint(len(relevant_weather_data))
  advice = ""
  if start_time <= weather_today['sunrise']:
    advice += f"Activity starts before sunrise, make sure to be visible in the dark.\n"
  if end_activity >= weather_today['sunset']:
    advice += f"Activity ends after sunset, make sure to be visible in the dark.\n"

  if activity_type.lower() == "biking":
    mean_temp = round(sum(i['temp'] for i in relevant_weather_data)/ len(relevant_weather_data), 1)
    if floor(mean_temp) <= 2:
      advice += f"Average temperature of {mean_temp}, make sure to wear long pants and a shirt with long sleeves with extra wind jacket.\n"
      advice += f"Don't forget gloves, galoshes, snood and cap.\n"
    elif floor(mean_temp) <= 10:
      advice += f"Average temperature of {mean_temp}, make sure to wear long pants and a shirt with long sleeves.\n"
    elif floor(mean_temp) <= 15:
      advice += f"Average temperature of {mean_temp}, you can wear short pants, or leg parts and a shirt with long sleeves.\n"
    elif floor(mean_temp) <= 20:
      advice += f"Average temperature of {mean_temp}, you can wear short pants, and short sleeves but keep the rest of the conditions in mind.\n"
    elif floor(mean_temp) > 20:
      advice += f"Average temperature above {mean_temp}, you can wear short pants and short sleeves.\n"

  if activity_type.lower() == "running":
    mean_temp = round(sum(i['temp'] for i in relevant_weather_data)/ len(relevant_weather_data), 1)
    if floor(mean_temp) <= 2:
      advice += f"Average temperature of {mean_temp}, make sure to wear long pants and a shirt with long sleeves with extra jacket.\n"
      advice += f"Don't forget gloves, snood and cap.\n"
    elif floor(mean_temp) <= 10:
      advice += f"Average temperature of {mean_temp}, make sure to wear long pants and a shirt with long sleeves.\n"
    elif floor(mean_temp) <= 15:
      advice += f"Average temperature of {mean_temp}, you can wear short pants and a shirt with long sleeves.\n"
    elif floor(mean_temp) <= 20:
      advice += f"Average temperature of {mean_temp}, you can wear short pants, and short sleeves but keep the rest of the conditions in mind.\n"
    elif floor(mean_temp) > 20:
      advice += f"Average temperature above {mean_temp}, you can wear short pants and short sleeves.\n"
    
  if all(i["windspeed"] >= 15.0  for i in relevant_weather_data) and weather_today["temp"] <= 10.0:
    advice += "There can be strong winds, make sure to wear something wind thight.\n"


  if any(i['precipprob'] >= 75.0 and i['precip'] > 0.0 for i in relevant_weather_data):
    advice += "Big chance of rain, take a rain jacket with you.\n"

  mean_uvindex = sum(i['uvindex'] for i in relevant_weather_data)/ len(relevant_weather_data)
  if mean_uvindex >= 4.0:
    advice += f'UV index is higher than {mean_uvindex}, make sure to wear sunscreen.\n'

  advice += road_wettness_advice(weather_today, start_time)

  print(advice)

  # TODO: Create metric for which outfit for running per temperature, also based on sun/rain/wind
  # TODO: Make sure user can input data on activity and duration
  # TODO: Make nice output data

def get_weather_data(location, day):
  response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{day}/{day}?unitGroup=metric&key=3J9DQTVM5FWBXS86H6DRKBWD5&contentType=json")
  if response.status_code!=200:
    print('Unexpected Status code: ', response.status_code)
    sys.exit()
  return response.json()

def road_wettness_advice(weather_today, start_activity):
  relevant_data = [i for i in weather_today['hours'] if i['datetime'] < start_activity]
  total_excted_precip = sum([i["precip"] for i in relevant_data])
  if not total_excted_precip > 0.0:
    return ""
  elif total_excted_precip > 0.0 and weather_today["temp"] > 0.0:
    return f"There has been {total_excted_precip} cm of rainfall today, the roads might be wet.\n"
  elif total_excted_precip > 0.0 and weather_today["temp"] < 0.0:
    return f"There has been {total_excted_precip} cm of precipation today,while it is also freezing The roads might be slippery.\n"


if __name__ == '__main__':
    main()
