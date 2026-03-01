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
        self.manager.draw()

    def setup_widgets(self):
        theme_button = UIFlatButton(text="Поменять тему", width=200, height=50, color=arcade.color.BLUE)
        theme_button.on_click = lambda event: self.change_theme()  # Не только лямбду, конечно
        self.box_layout.add(theme_button)
        theme_button = UIFlatButton(text="Сброс поискового результата", width=250, height=50, color=arcade.color.BLUE)
        theme_button.on_click = lambda event: self.change_theme()  # Не только лямбду, конечно
        self.box_layout.add(theme_button)
        self.anchor_layout.center_y = -100

    def change_theme(self):
        self.theme_index += 1
        self.theme_index %= 2
        self.get_image()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.PAGEUP:
            self.default_zoom *= 2
            self.get_image()
        if key == arcade.key.PAGEDOWN:
            self.default_zoom /= 2
            self.get_image()

    def get_image(self):
        toponym_to_find = " ".join(sys.argv[1:])
        if not toponym_to_find:
            toponym_to_find = STANDART_PLACE
        toponym = geocoder.get_toponym(toponym_to_find)
        toponym_longitude, toponym_altitude = geocoder.get_coordinates(toponym_to_find)
        if toponym_longitude and toponym_altitude:
            delta = str(float(get_spn(toponym_to_find).split(",")[0]) * self.default_zoom) + "," + str(float(get_spn(toponym_to_find).split(",")[1]) * self.default_zoom)
            print(type(delta))
            apikey = "17efe1e9-c0e1-4c3d-b18c-2cf038f24953"
            ll = ",".join([toponym_longitude, toponym_altitude])
            # Собираем параметры для запроса к StaticMapsAPI:
            map_params = {
                "ll": ll,
                "spn": delta,
                "apikey": apikey,
                "theme": THEMES[self.theme_index]
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