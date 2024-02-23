from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from app.services.weatherService import get_weather_data, city_exists, get_daily_weather_data, get_all_weather_data, \
    get_all_weather_data_by_city


@app.route('/')
def start():
    """
     Renders the starting page of the weather forecast application.
     This is the main page where users can enter a city name to get forecasts.
     """
    return render_template('start.html')


@app.route('/forecast', methods=['POST'])
def get_forecast():
    """
    Handles the form submission from the start page.
    Extracts the city name and forecast type from the form data.
    Redirects to the appropriate forecast page based on the forecast type,
    or shows an error message if the city name is not provided or not found.
    """
    city_name = request.form['cityName']
    forecast_type = request.form['forecast_type']

    if not city_name:
        flash("Please enter a city name.")
        return redirect(url_for('start'))

    if not city_exists(city_name):
        flash(f"We have no data about a city named {city_name}")
        return redirect(url_for('start'))

    # We redirect based on forecast type
    if forecast_type == 'daily':
        return redirect(url_for('show_daily_forecast', city_name=city_name))
    else:
        return redirect(url_for('show_forecast', city_name=city_name))


@app.route('/forecast/hourly/<city_name>')
def show_forecast(city_name):
    """
    Renders the hourly weather forecast page for a given city.
    Fetches weather data for the specified city and displays it.
    If no data is found, redirects to the start page with an error message.
    """
    forecast_days = get_weather_data(city_name)
    return render_template('hourlyForecast.html', city_name=city_name, forecast_days=forecast_days)


@app.route('/forecast/daily/<city_name>')
def show_daily_forecast(city_name):
    """
    Renders the daily weather forecast page for a given city.
    Fetches daily forecast data for the specified city and displays it.
    If no data is found, redirects to the start page with an informational message.
    """
    daily_forecast = get_daily_weather_data(city_name)
    if not daily_forecast:
        flash(f"No daily forecast data available for {city_name}.", "info")
        return redirect(url_for('start'))
    return render_template('dailyForecast.html', city_name=city_name, daily_forecast=daily_forecast)


@app.route('/all')
def get_all_data():
    """
    Returns a JSON response containing all weather forecast data.
    This was created to have some interaction with the db and should only be used with Postman.
    """
    all_weather_data = get_all_weather_data()
    # We convert the data to a list of dictionaries for JSON response
    data_list = [data.to_dict() for data in all_weather_data]
    return jsonify(data_list)


@app.route('/<cityName>')
def show_weather_by_city(cityName):
    """
    Returns all weather data for a given city.
    This was created to have some interaction with the db and should only be used with Postman.
    """
    weather_data = get_all_weather_data_by_city(cityName)
    return jsonify(weather_data)
