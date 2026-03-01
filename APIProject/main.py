import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
import geocoder
import requests
from PIL import Image

from geocoder import get_spn

toponym_to_find = " ".join(sys.argv[1:])
toponym = geocoder.get_toponym(toponym_to_find)
toponym_longitude, toponym_altitude = geocoder.get_coordinates(toponym_to_find)
if toponym_longitude and toponym_altitude:
    delta = get_spn(toponym_to_find)
    apikey = "17efe1e9-c0e1-4c3d-b18c-2cf038f24953"
    ll = ",".join([toponym_longitude, toponym_altitude])
    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ll,
        "spn": delta,
        "apikey": apikey
    }
    print()
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    im = BytesIO(response.content)
    opened_image = Image.open(im)
    opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы
