import json
from datetime import datetime

import requests

from data import config
from database import ConnectDB
from utils.database import Statistic, Cities

db = ConnectDB()


def get_weather():
    """Function which pulls out the weather forecast for 7 days"""
    cities = ['Lviv', 'Dnipro', 'Odessa', 'Kiev', 'Lutsk']

    coordinates_of_cities = {}
    for city in cities:
        coordinates = json.loads(requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city},ua&appid=d14dd9c0ead5798cff30e728abde9c08').text)
        coordinates_of_cities[city] = coordinates['coord']
    for key, value in coordinates_of_cities.items():
        url = f"https://api.openweathermap.org/data/2.5/onecall?lon={value['lon']}&lat={value['lat']}" \
              f"&units=metric&exclude=hourly,minutely,alerts&appid={config.api_key}"
        request = requests.get(url).text
        to_dict = json.loads(request)
        days = to_dict['daily'][0:7]
        city = Cities(city=key)
        db.session.add(city)
        db.session.commit()
        for day in days:
            date = datetime.fromtimestamp(day['dt']).date()
            try:
                rain = float(day['rain'])
            except KeyError:
                rain = 0
            try:
                snow = float(day['snow'])
            except KeyError:
                snow = 0
            pcp = round(rain + snow)
            avarage_temp = round(day['temp']['min'] + day['temp']['max']) / 2
            clouds = int(day['clouds'])
            pressure = int(day['pressure'])
            humidity = int(day['humidity'])
            wind_speed = float(day['wind_speed'])

            statistic = Statistic(cities=city, date=date, temp=avarage_temp, pcp=pcp, clouds=clouds, pressure=pressure,
                                  humidity=humidity, wind_speed=wind_speed)
            db.session.add(statistic)
            db.session.commit()


if __name__ == '__main__':
    get_weather()
