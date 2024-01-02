import json
import pandas as pd
from datetime import datetime, timedelta
import statistics as st
import statistics as st

WEATHER_DATA_PATH = './data/weather.json'
RAINFALL_DATA_PATH = './data/rainfall.json'
WEATHER_FORECAST_DATA_PATH = './data/weather-forecast.json'

def find_middle_time(time_str_1, time_str_2):
	time_1 = datetime.strptime(time_str_1, "%Y-%m-%d %H:%M:%S")
	time_2 = datetime.strptime(time_str_2, "%Y-%m-%d %H:%M:%S")
	result = time_1 + (time_2 - time_1)/2 
	return result.strftime("%Y-%m-%d %H:%M:%S")


def get_county_mean_rainfall(time_range):
	try:
		with open(RAINFALL_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			result_list = (
				df[~df[f'RainfallElement.{time_range}.Precipitation'].isin([-99, -98, 'X', 'T'])]
					.groupby('GeoInfo.CountyName')[f'RainfallElement.{time_range}.Precipitation']
					.mean()
					.reset_index()
					.rename(columns={
						'GeoInfo.CountyName': 'location', 
						f'RainfallElement.{time_range}.Precipitation': 'z'
					})
					.to_dict(orient='records')
			)
			result_json = json.dumps(result_list, ensure_ascii=False)
				
	except FileNotFoundError:
		print('Rainfall data not found')
		return
	return result_json

def get_rainfall_time_range():
	time_range = ['Now', 'Past10Min', 'Past1hr', 'Past3hr', 'Past6Hr', 'Past12hr', 'Past24hr', 'Past2days', 'Past3days']
	return time_range

def get_county_mean_temperature():
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			result_list = (
				df[df['WeatherElement.AirTemperature'] != -99]
					.groupby('GeoInfo.CountyName')['WeatherElement.AirTemperature']
					.mean()
					.round(1)
					.reset_index()
					.rename(columns={
						'GeoInfo.CountyName': 'location', 
						'WeatherElement.AirTemperature': 'z'
					})
					.to_dict(orient='records')
			)

			result_json = json.dumps(result_list, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result_json

def get_county_temperature_extremum(location):
	try:
		with open(WEATHER_FORECAST_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			data_list = json_data['data']
			for data in data_list:
				if data['locationName'] == location:
					minT_list = []
					maxT_list = []
					x_list = []
					tick_list = []
					for element in data['weatherElement']:
						if element['elementName'] == 'MinT':
							for i, time in enumerate(element['time']):
								minT_list.append(time['parameter']['parameterName'])
								x_list.append(find_middle_time(time['startTime'], time['endTime']))
								tick_list.append(time['startTime'])
								if i == 2:
									tick_list.append(time['endTime'])
						if element['elementName'] == 'MaxT':
							for time in element['time']:
								maxT_list.append(time['parameter']['parameterName'])
					result = {
						'MinT': minT_list,
						'MaxT': maxT_list,
						'x': x_list,
						'ticks': tick_list
					}


			result_json = json.dumps(result, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result_json

def get_county_information(location):
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			data_list = json_data['data']
			temperature_list = []
			humidity_list = []
			pressure_list = []
			windspeed_list = []
			for data in data_list:
				if data['GeoInfo']['CountyName'] == location:
					if(data['WeatherElement']['AirTemperature']!= -99):
						temperature_list.append(data['WeatherElement']['AirTemperature'])
					if(data['WeatherElement']['RelativeHumidity']!= -99):
						humidity_list.append(data['WeatherElement']['RelativeHumidity'])
					if(data['WeatherElement']['AirPressure']!= -99):
						pressure_list.append(data['WeatherElement']['AirPressure'])
					if(data['WeatherElement']['WindSpeed']!= -99):
						windspeed_list.append(data['WeatherElement']['WindSpeed'])
			result = {
				'temperature': round(st.mean(temperature_list), 2),
				'pressure': round(st.mean(pressure_list), 2),
				'windspeed': round(st.mean(windspeed_list), 2),
				'humidity': round(st.mean(humidity_list), 2),
			}
			result_json = json.dumps(result, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result_json

def get_county_mean_windspeed():
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			result_list = (
				df[df['WeatherElement.WindSpeed'] != -99]
					.groupby('GeoInfo.CountyName')['WeatherElement.WindSpeed']
					.mean()
					.round(1)
					.reset_index()
					.rename(columns={
						'GeoInfo.CountyName': 'location', 
						'WeatherElement.WindSpeed': 'z'
					})
					.to_dict(orient='records')
			)

			result_json = json.dumps(result_list, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result_json

def get_counties():
	counties = ['臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣', '基隆市', '新竹市', '嘉義市']
	return counties