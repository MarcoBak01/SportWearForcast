from datetime import datetime
from pprint import pprint
from constants import OUT_DIR, FILE_NAME
import json

def main():

    activity_duration = 3
    activity_type = "biking"

    with open(f'{OUT_DIR}/{FILE_NAME}') as json_file:
        weather_data = json.load(json_file)

    weather_today = weather_data['days'][0]

    wheather_hourly = weather_today['hours']
    pprint(wheather_hourly)

    # TODO: Create metric for which outfit for running per temperature, also based on sun/rain/wind
    # TODO: Create metric for which outfit for biking per temperature, also based on sun/rain/wind
    # TODO: Make sure user can input data on activity and duration
    # TODO: Make nice output data




if __name__ == '__main__':
    main()
