import requests
from flask import flash
from sqlalchemy.exc import SQLAlchemyError

from app.models.city import db, WeatherForecast


def parse_city_name(city_name):
    """
    We parse the city name to ensure the first letter of each word is uppercase
    and the rest are lowercase, which is common formatting for city names.
    """
    return city_name.title()


def city_exists(city_name):
    """
    We check if a city exists by making a request to the weather API with the parsed city name.
    If the API returns a successful response, the city exists; otherwise, it does not.
    """
    city_name = parse_city_name(city_name)
    api_key = '1c3026c778c04f88b4c140535242102'
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}'
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        flash(f"Failed to check city existence: {str(e)}")
        return False


def get_weather_data(city_name):
    """
    We retrieve detailed hourly weather data for the next three days excluding today.
    This involves parsing the city name, checking its existence, and parsing the API response.
    """
    city_name = parse_city_name(city_name)
    if not city_exists(city_name):
        return []

    api_key = '1c3026c778c04f88b4c140535242102'
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_name}&days=4'
    try:
        response = requests.get(url)
        weather_data = response.json()
        if 'forecast' in weather_data and 'forecastday' in weather_data['forecast']:
            # We exclude the first day as it is the current day
            forecast_days = weather_data['forecast']['forecastday'][1:]
            for day in forecast_days:
                max_temp = day['day']['maxtemp_c']
                min_temp = day['day']['mintemp_c']
                total_precip = day['day']['totalprecip_mm']
                sunrise = day['astro']['sunrise']
                sunset = day['astro']['sunset']
                date = day['date']
                insert_or_update_weather_forecast(city_name, date, max_temp, min_temp, total_precip, sunrise, sunset)

                for hour in day['hour']:
                    # We extract only the time part from the datetime string
                    hour['formatted_time'] = hour['time'].split(' ')[1]
                    hour['temp_c'] = round(hour['temp_c'])
            return forecast_days
    except requests.exceptions.RequestException as e:
        flash(f"Failed to retrieve weather data: {str(e)}")
        return []


def get_daily_weather_data(city_name):
    """
    We fetch daily weather forecast data excluding today. This function parses the city name,
    verifies city existence, and then retrieves and formats the forecast data for the next three days.
    """
    city_name = parse_city_name(city_name)
    try:
        if not city_exists(city_name):
            return []

        api_key = '1c3026c778c04f88b4c140535242102'
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_name}&days=4'
        response = requests.get(url)
        weather_data = response.json()

        if 'forecast' in weather_data:
            daily_forecast = []
            # We skip the first day as it's today
            for day in weather_data['forecast']['forecastday'][1:]:
                date = day['date']
                max_temp = day['day']['maxtemp_c']
                min_temp = day['day']['mintemp_c']
                condition = day['day']['condition']['text']
                # We ensure the URL is complete by adding "https:"
                icon_url = "https:" + day['day']['condition']['icon']
                sunrise = day['astro']['sunrise']
                sunset = day['astro']['sunset']

                # We update or insert the weather forecast data into the database
                insert_or_update_weather_forecast(city_name, date, max_temp, min_temp, day['day']['totalprecip_mm'],
                                                  sunrise, sunset)

                daily_forecast.append({
                    'date': date,
                    'max_temp': max_temp,
                    'min_temp': min_temp,
                    'condition': condition,
                    'icon': icon_url
                })
            return daily_forecast
    except requests.exceptions.RequestException as e:
        flash(f"Failed to retrieve weather data: {str(e)}")
        return []


def insert_or_update_weather_forecast(city, date, max_temp, min_temp, total_precip, sunrise, sunset):
    """
    We either insert new weather forecast data into the database or update an existing record.
    This is determined by whether a forecast for the specified city and date already exists.
    """
    try:
        existing_forecast = WeatherForecast.query.filter_by(city=city, date=date).first()
        if existing_forecast:
            existing_forecast.max_temperature = max_temp
            existing_forecast.min_temperature = min_temp
            existing_forecast.total_precipitation = total_precip
            existing_forecast.sunrise = sunrise
            existing_forecast.sunset = sunset
        else:
            new_forecast = WeatherForecast(
                city=city, date=date, max_temperature=max_temp,
                min_temperature=min_temp, total_precipitation=total_precip,
                sunrise=sunrise, sunset=sunset)
            db.session.add(new_forecast)
        db.session.commit()
    except SQLAlchemyError as e:
        # We roll back the transaction in case of an error
        db.session.rollback()
        flash(f"Failed to insert or update weather forecast: {str(e)}")


def get_all_weather_data():
    """
    This function fetches every weather forecast data from the database.
    """
    try:
        all_data = WeatherForecast.query.all()
        return all_data
    except SQLAlchemyError as e:
        flash(f"Failed to retrieve all weather data: {str(e)}")
        return []


def get_all_weather_data_by_city(city_name):
    """
    Fetches all weather data for the specified city from the database.
    Returns the data as a list of dictionaries.
    """
    try:
        city_name = parse_city_name(city_name)
        weather_data = WeatherForecast.query.filter_by(city=city_name).all()
        return [data.to_dict() for data in weather_data]
    except SQLAlchemyError as e:
        flash(f"Database query failed: {str(e)}", "error")
        return []
