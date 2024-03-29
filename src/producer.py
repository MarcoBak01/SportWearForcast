from datetime import datetime
import requests
import sys

import json
from constants import OUT_DIR, FILE_NAME
from pprint import pprint


def main():
  # TODO: Make sure to enter location manualy, and inporperate it in the json file name if that is possible.
  # TODO: put them all in one file again for now, there are more then anough api calls for each day.
  location = "Delft"
  today = datetime.today().strftime("%d_%m_%Y")
  print(today)
  response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{today}/{today}?unitGroup=metric&key=3J9DQTVM5FWBXS86H6DRKBWD5&contentType=json")
  if response.status_code!=200:
    print('Unexpected Status code: ', response.status_code)
    sys.exit()

  weather_data = response.json()

  with open(f'{OUT_DIR}/{FILE_NAME}', 'w') as outfile:
      json.dump(weather_data, outfile)


if __name__ == '__main__':
    main()
