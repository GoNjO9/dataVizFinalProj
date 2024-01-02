import json

from fetch import fetch_weather_history, fetch_station
from data_helpers import find_middle_time

import pandas as pd

fetch_weather_history()
fetch_station()

WEATHER_HISTORY_DATA_PATH = './data/weather-history.json'
STATION_DATA_PATH = './data/station.json'


print(get_county_temperature_history('臺北市'))