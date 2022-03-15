import re

import cv2
import numpy as np
import transliterate

BACKGROUND = 'python_snippets/external_data/probe.jpg'
POSTCARD = cv2.imread(BACKGROUND)
SUN = "python_snippets/external_data/weather_img/sun.jpg"  # солнечно
RAIN = 'python_snippets/external_data/weather_img/rain.jpg'  # дождь
SNOW = 'python_snippets/external_data/weather_img/snow.jpg'  # снег
CLOUD = 'python_snippets/external_data/weather_img/cloud.jpg'  # облачность
FONT = cv2.FONT_HERSHEY_COMPLEX


class WeatherCard:
    def __init__(self):
        self.args = None
        self.open_image = None
        self.color_step_r = 0
        self.color_step_g = 0
        self.matrix_step = 0
        self.color_step_b = 0
        # self.args[0] = None
        # self.args[1] = None
        # self.args[2] = None
        # self.args[3] = None
        # self.args[4] = None
        # self.args[5] = None

    # метод наложения иконок погоды на фон карточки погоды
    def weather_icons(self, *args):
        if 'SUN' in args[0]:  # солнечно
            self.open_image = SUN

        if 'RAIN' in args[0]:  # дождь
            self.open_image = RAIN

        if 'SNOW' in args[0]:  # снег
            self.open_image = SNOW

        if 'CLOUD' in args[0]:  # пасмурно
            self.open_image = CLOUD

        sunny_weather = cv2.imread(self.open_image)  # накладываемое изображение солнце
        sun_width, sun_height = sunny_weather.shape[:2]  # ширина и высота изображения солнце
        POSTCARD[:sun_width, :sun_height] = sunny_weather[:]  # в левый верхний

    # метод наложения текста погоды на фон карточки погоды
    def text_overlay(self, *args):
        cv2.putText(POSTCARD, f'Дата: {args[0]}', (180, 30), FONT, 0.7, color=(0, 0, 0), thickness=2)
        cv2.putText(POSTCARD, f'Город: {args[1]}', (200, 70), FONT, 0.7, color=(0, 0, 0), thickness=2)
        cv2.putText(POSTCARD, f'Погода: {args[3]}', (10, 150), FONT, 0.5, color=(0, 0, 0), thickness=2)
        cv2.putText(POSTCARD, f'Температура {args[2]} С', (340, 150), FONT, 0.5, color=(0, 0, 0), thickness=2)
        cv2.putText(POSTCARD, f'Влажность {args[4]} %', (10, 190), FONT, 0.5, color=(0, 0, 0), thickness=2)
        cv2.putText(POSTCARD, f'Скорость ветра {args[5]} m/c', (270, 190), FONT, 0.5, color=(0, 0, 0), thickness=2)
        return

    def calling_methods(self, *args):
        # вызов метода наложения иконок погоды на фон карточки погоды
        self.weather_icons(args[0])

        # вызов метода наложения текста погоды на фон карточки погоды - аргументы:дата,влажность,скорость ветра
        self.text_overlay(args[1], args[2], args[3], args[4], args[5], args[6])

        # проверка ввода города на латиницу или кириллицу
        if re.search('[а-яА-Я]', args[2]):
            # вызов метода показа карточки
            self.show_card(transliterate.translit(args[2], reversed=True))  # транслит города на латиницу
        # вызов метода показа карточки
        self.show_card(args[2])  # - название карточки

    # Солнечно
    def solar(self, *args):
        for _ in range(50):
            POSTCARD[:, 0 + self.matrix_step:50 + self.matrix_step] = (
                50 + self.color_step_b, 255 - self.color_step_b / 8, 238)
            self.matrix_and_colors(20, 5)

        self.calling_methods('SUN', args[0], args[1], args[2], args[3], args[4], args[5])

    # Дождь
    def rain(self, *args):
        for _ in range(50):
            POSTCARD[:, self.matrix_step:50 + self.matrix_step] = \
                (128, 10 + self.color_step_g / 3, 10 + self.color_step_r)
            self.matrix_and_colors(12, 10, 7)

        self.calling_methods('RAIN', args[0], args[1], args[2], args[3], args[4], args[5])

    # Снег
    def snow(self, *args):
        for _ in range(50):
            POSTCARD[:, self.matrix_step:50 + self.matrix_step] = \
                (205 + self.color_step_b / 10, 90 + self.color_step_g / 3, 106 + self.color_step_r)
            self.matrix_and_colors(12, 10, 7, 0.5)

        # метод вызовов однотипных функций
        self.calling_methods('SNOW', args[0], args[1], args[2], args[3], args[4], args[5])

    # Пасмурно
    def cloudy(self, *args):
        for _ in range(50):
            POSTCARD[:, self.matrix_step:50 + self.matrix_step] = (128 + self.color_step_b / 2, 128, 128)
            self.matrix_and_colors(12, 4)
            self.matrix_step += 12
            self.color_step_b += 4

        # метод вызовов однотипных функций
        self.calling_methods('CLOUD', args[0], args[1], args[2], args[3], args[4], args[5])

    def matrix_and_colors(self, *args):
        try:
            if args[0]:
                self.matrix_step += args[0]

            if args[1]:
                self.color_step_b += args[1]

            if args[2]:
                self.color_step_g += args[2]

            if args[3]:
                self.color_step_r += args[3]

        except Exception:
            pass

    # Показ карточки
    def show_card(*args):
        cv2.imshow(args[1], POSTCARD)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite('weather_card.jpg', POSTCARD)
        exit()


weathercard = WeatherCard()
# weathercard.cloudy()
