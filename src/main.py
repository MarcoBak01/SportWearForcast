import requests
import sys

import json
                

response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Delft?unitGroup=metric&key=3J9DQTVM5FWBXS86H6DRKBWD5&contentType=json")
if response.status_code!=200:
  print('Unexpected Status code: ', response.status_code)
  sys.exit()  


# Parse the results as JSON
jsonData = response.json()