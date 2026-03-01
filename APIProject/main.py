import os
import arcade
import sys
import geocoder
import requests
from geocoder import get_spn


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"
THEMES = ['light', 'dark']
STANDART_PLACE = 'Москва'
class GameView(arcade.Window):
    def setup(self):
        self.get_image()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                (self.width - self.background.width) // 2,
                (self.height - self.background.height) // 2,
                self.background.width,
                self.background.height
            ),
        )

    def get_image(self):
        toponym_to_find = " ".join(sys.argv[1:])
        if not toponym_to_find:
            toponym_to_find = STANDART_PLACE
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
                "apikey": apikey,
                "theme": "dark"
            }
            print()
            map_api_server = "https://static-maps.yandex.ru/v1"
            response = requests.get(map_api_server, params=map_params)

            if not response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)

            # Запишем полученное изображение в файл.
            with open(MAP_FILE, "wb") as file:
                file.write(response.content)

            self.background = arcade.load_texture(MAP_FILE)


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    # Удаляем за собой файл с изображением.
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()