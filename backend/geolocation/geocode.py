from typing import Dict

import requests
from geopy import distance


def fetch_coordinates(apikey, address) -> Dict[str, float] | None:
    try:
        response = requests.get(
            "https://geocode-maps.yandex.ru/1.x",
            params={
                "geocode": address,
                "apikey": apikey,
                "format": "json",
            }
        )
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']
        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return {'lat': lat, 'lon': lon}
    except Exception as err:
        print(err)


def calculate_distance(from_location, to_location):
    return round(
        distance.distance(
            from_location.coordinates,
            to_location.coordinates
        ).kilometers,
        2
    )
