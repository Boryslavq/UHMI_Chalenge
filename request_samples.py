import logging
import time

import requests
import json

main_host = 'http://127.0.0.1:5000'


def test_cities():
    """Function which sends get request to /cities"""
    cities_json = json.loads(requests.get(main_host + '/cities').text)
    print('Міста:', ", ".join(cities_json['cities'])) if 'cities' in cities_json else print(
        'За цим ресурсом результатів немає')
    citiess_json = json.loads(requests.get(main_host + '/citiess').text)  # wrong route
    print('Міста:', ", ".join(citiess_json['cities'])) if 'cities' in citiess_json else print(
        'За цим ресурсом результатів немає')


def parse_for_means(record: dict) -> str:
    """Function which decomposes json from route /means"""
    for k, v in record.items():
        for key, value in v.items():
            return f"{key} в місті {k}: {value}"


def test_means():
    """Function which sends get request to /means with parameters"""
    means_temp_json = json.loads(requests.get(main_host + '/means/temp/Lviv').text)
    print(parse_for_means(means_temp_json))
    means_humidity_json = json.loads(requests.get(main_host + '/means/humidity/Kiev').text)
    print(parse_for_means(means_humidity_json))


def parse_for_records(record: dict) -> str:
    """Function which decomposes json from route /records"""
    forecast = ''
    for atr, value in record['weather'].items():
        forecast += f'{atr}: {value} \n'

    return f'Прогноз погоди для міста {record["city"]} за {record["date"]} \n{forecast}'


def test_records():
    """Function which sends get request to /records with parameters"""
    records_one = json.loads(requests.get(main_host + '/records/Kiev/2021-12-20/2021-12-22').text)

    records_two = json.loads(requests.get(main_host + '/records/Lutsk/2021-12-23/2021-12-26').text)

    records_list = [records_one, records_two]
    for record in records_list:
        for rec in record:
            print('-------------------------')
            print(parse_for_records(rec))


def parse_for_moving(moving_dict: dict):
    """Function which decomposes json from route /moving_mean"""
    for key, value in moving_dict.values():
        print(key, value)


def test_moving_mean():
    """Function which sends get request to /moving_means with parameters"""

    moving_one = json.loads(requests.get(main_host + '/moving_mean/clouds/Odessa').text)
    moving_two = json.loads(requests.get(main_host + '/moving_mean/pcp/Dnipro').text)
    moving_list = [moving_one, moving_two]

    for moving in moving_list:
        print('-----------------------')

        print(f"Місто: {moving['city']} \n Ковзке середнє для {moving['result']}")


def main():
    test_cities()
    time.sleep(3)

    test_means()
    time.sleep(3)

    test_records()
    time.sleep(3)

    test_moving_mean()


if __name__ == '__main__':
    main()
