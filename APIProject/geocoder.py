import requests


def get_toponym(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym
    except Exception:
        return None


def get_coordinates(toponym_to_find):
    toponym = get_toponym(toponym_to_find)
    if not toponym:
        return None, None
    else:
        toponym_coordinates = toponym["Point"]["pos"]
        # Долгота и широта:
        toponym_longitude, toponym_altitude = toponym_coordinates.split(" ")
        return toponym_longitude, toponym_altitude


def get_spn(toponym_to_find):
    toponym = get_toponym(toponym_to_find)
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    spn = f"{dx},{dy}"
    return spn
