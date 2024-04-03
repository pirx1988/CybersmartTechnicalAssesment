import requests
from django.conf import settings

def fetchWeather(location):
    weather_map_api_key = settings.OPEN_WEATHER_MAP_API_KEY
    unit = "metric" # unit. I've applied here metric in order to obtain temperature in celcius degrees
    external_api_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&APPID={weather_map_api_key}&units={unit}"
    return requests.get(url=external_api_url)

def calcBackgroundColor(weather, temp):
    cold_or_rain_conditions = {'max_temp': 10,'weather': "Rain", 'color': 'blue'}
    warm_or_cloudy_conditions = {'min_temp': 10, 'max_temp': 25, 'weather': "Clouds", 'color': '#FFA500'}
    hot_or_sunny_conditions = {'min_temp': 25, 'weather': "Clear", 'color': 'red'}

    # Assume 'response' is a dictionary containing temperature and weather information
    if (temp < cold_or_rain_conditions['max_temp']) or weather == cold_or_rain_conditions['weather']:
        return cold_or_rain_conditions['color']
    elif (temp >= warm_or_cloudy_conditions['min_temp'] and temp <= warm_or_cloudy_conditions['max_temp']) or weather == warm_or_cloudy_conditions['weather']:
        return warm_or_cloudy_conditions['color']
    elif (temp > hot_or_sunny_conditions['min_temp']) or (hot_or_sunny_conditions['weather'] == hot_or_sunny_conditions['max']):
        return hot_or_sunny_conditions['color']
    else:
        # If temperature is outside of defined ranges or doesn't fit any weather description, set default background color
        return 'white'
