from flask import Flask, render_template, jsonify, redirect
from fetch import fetch_all
from data_helpers import *

app = Flask(__name__)

@app.route('/')
def index():
	return redirect('/home')

@app.route('/home')
def main_page():
	return render_template(
		'home.html',
	)

@app.route('/temperature')
def temperature():
	return render_template(
		'temperature.html',
		chart_data = get_county_mean_temperature(),
	)

@app.route('/windspeed')
def windspeed():
	return render_template(
		'windspeed.html',
		chart_data = get_county_mean_windspeed(),
	)

@app.route('/rainfall/<string:timeRange>')
def rainfall(timeRange):
	return render_template(
		'rainfall.html',
		time_range = timeRange,
		time_range_list = get_rainfall_time_range(),
		base_url = '/rainfall',
		chart_data = get_county_mean_rainfall(timeRange)
	)

@app.route('/county/<string:countyName>')
def county(countyName):
	return render_template(
		'county.html',
		location = countyName,
		counties = get_counties(),
		base_url = '/county',
		temperature_forecast_data = get_county_temperature_extremum(countyName),
		temperature_history_data = get_county_temperature_history(countyName),
		information = get_county_information(countyName)
	)


if __name__ == '__main__':
	fetch_all()
	app.run(debug=True, port=5001)