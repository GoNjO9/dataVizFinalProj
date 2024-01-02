import os
import json
import requests as req
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WEATHER_DATA_PATH = './data/weather.json'
RAINFALL_DATA_PATH = './data/rainfall.json'
WEATHER_FORECAST_DATA_PATH = './data/weather-forecast.json'
WEATHER_HISTORY_DATA_PATH = './data/weather-history.json'
MANNED_STATION_INFORMATION = './data/manned-station-information.json'
UNMANNED_STATION_INFORMATION = './data/unmanned-station-information.json'
OBS_RECORD_30DAYS = './data/obs-record-30days.json'
DATE_FORMAT = '%Y-%m-%d %H'

def fetch_all():
	"""
    Fetch weather and rainfall data from [Open Weather Data](https://opendata.cwa.gov.tw/) into json files.
    """
	fetch_weather()
	fetch_rainfall()
	fetch_weather_forecast()
	fetch_weather_history()
	fetch_manned_station_information()
	fetch_unmanned_station_information()
	fetch_obs_record_30days() # Need some time to fetch

def fetch_weather():
	# Check if the data is already fetched today
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Weather data is already up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['Station']
		}
		with open(WEATHER_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting weather data')


def fetch_rainfall():
	# Check if the data is already fetched today
	try:
		with open(RAINFALL_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Rainfall data is already up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0002-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['Station']
		}
		with open(RAINFALL_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting rainfall data')

def fetch_weather_history():
	try:
		with open(WEATHER_HISTORY_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Weather forecast data is up to date')
				return
	except FileNotFoundError:
		pass

	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/C-B0024-001?downloadType=WEB&format=JSON'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['cwaopendata']['resources']['resource']['data']['surfaceObs']['location']
		}
		with open(WEATHER_HISTORY_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting weather history data')

def fetch_weather_forecast():
	try:
		with open(WEATHER_FORECAST_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Weather forecast data is already up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['location']
		}
		with open(WEATHER_FORECAST_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting weather forecast data')

def fetch_manned_station_information():
	try:
		with open(MANNED_STATION_INFORMATION, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Manned station information data is already up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/C-B0074-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['data']['stationStatus']['station']
		}
		with open(MANNED_STATION_INFORMATION, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting manned station  data')

def fetch_unmanned_station_information():
	try:
		with open(UNMANNED_STATION_INFORMATION, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Unmanned station information data is already up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/C-B0074-002'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['data']['stationStatus']['station']
		}
		with open(UNMANNED_STATION_INFORMATION, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting unmanned station information data')

def fetch_obs_record_30days():
	try:
		with open(OBS_RECORD_30DAYS, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('30 days data is already up to date')
				return
	except FileNotFoundError:
		pass

	url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/C-B0024-001?downloadType=WEB&format=JSON'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200:
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['cwaopendata']['resources']['resource']['data']['surfaceObs']['location']
		}
		with open(OBS_RECORD_30DAYS, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting 30days data')
