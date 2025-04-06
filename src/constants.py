from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

OUT_DIR = 'out'
FILE_NAME = f'{datetime.today().strftime("%d_%m_%Y")}_weather.json'
API_KEY = os.getenv('OPENWEATHER_API_KEY','No API_KEY set')