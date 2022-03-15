# -*- coding: utf-8 -*-
import traceback
from datetime import *
import requests
import sqlite3
import datetime as dt
from datetime import date
import time
from send import *
from operations import *
from data_sampling import *
from card import *

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database

#  не пойму как вынести урл в константы...? Ведь там имеются переменные.Например:self.location или self.city_id...
# TODO Выделить общую часть урла и присвоить одной константе, а для каждого вида запроса к API создать свои константы,
#  где использовать форматирование строк с аргументами-ключевыми словами:
#  https://pythonru.com/osnovy/formatirovanie-v-python-s-pomoshhju-format (см. раздел "Для аргументов-ключевых слов")
'''
При запуске приложение сначала производит поиск информации в базе данных, если не находит,
то через API получает нужную информацию и записывает данные в базу данных. При повторном запуске приложения
 при тех же параметрах данные уже выводятся из базы данных. Если вводится другой город,
 то данные перезаписываются в базе данных
'''


class WeatherMaker:
    def __init__(self):
        self.d = None
        self.date = None
        self.current_db = {}  # данные текущего прогноза
        self.period_db = {}  # данные прогноза на 5 дней
        self.history_db = {}  # данные истории за 5 дней
        self.step_selection = None
        self.wind = None
        self.current_month = None
        self.this_year = None
        self.this_day = None
        self.presently = None
        self.temperature = None
        self.cloudiness = None
        self.api_link = None
        self.day_data = None
        self.historical_data = None
        self.api_data = None
        self.last_day = None
        self.city_id = None
        self.lat = None
        self.lon = None
        self.speed = None
        self.humidity = None
        self.location = None
        self.date_time = None
        self.weather_desc = None
        self.temp_city = None
        self.complete_api_link = None

    # метод получения текущего времени
    def current_time(self):
        self.date = date.today().strftime("%d.%m.%Y")  # перевод в российский формат

        self.presently = dt.datetime.now()  # текущая дата и время
        self.last_day = self.presently.day  # текущая дата
        self.current_month = self.presently.month  # текущий месяц
        self.this_year = self.presently.year  # текущий год

    # метод введения данных от пользователя
    def data_input(self, *args):
        if 'Выбор действия' in args:
            self.step_selection = input('Выбор действия: ')  # Вам доступно меню
            print('≪ ≫' * 10)
            # self.step_selection = '5'
            return
        self.location = input('Введите населенный пункт: ')
        # self.location = 'Учалы'
        self.get_city_id()

    # метод получение ID населенного пункта
    def get_city_id(self):  # получение ID населенного пункта
        try:
            res = requests.get("https://api.openweathermap.org/data/2.5/find",
                               params={'q': self.location, 'type': 'like', 'units': 'metric', 'lang': 'ru',
                                       'APPID': API})
            data = res.json()

            self.city_id = data['list'][0]['id']

        except Exception as ex:
            print('Такого населенного пункта не существует!')
            self.data_input()

        # передаю в функцию словарь с выбором действия
        print('ДОСТУПНОЕ МЕНЮ:')
        print(f'Вы быбрали - {self.location}')
        self.action_menu(action_choice)

    # метод меню выбора действий
    def action_menu(self, *args):
        for action in args:  # перебираю словарь action_choice с выбором действия
            for key in action:
                print(key, '->', action[key])  # вывод на консоль

        self.data_input('Выбор действия')
        if self.step_selection == '1':  # Сменить город
            self.data_input()

        elif self.step_selection == '2':  # Получить текущий прогноз погоды
            # basedatabase.weather_now() # обращение к  БД  на наличие записи текущей погоды - модуль  data_sampling.py
            self.current_weathe()  # иначе делается запрос к API

        elif self.step_selection == '3':  # Получить прогноз погоды на 5 дней
            # basedatabase.forecast_future() # обращение к  БД  на наличие  записи на 5 дней- модуль  data_sampling.py
            self.period_data()  # иначе делается запрос к API

        elif self.step_selection == '4':  # Получить данные погоды за период прошлых 5 дней
            self.weather_history()  # иначе делается запрос к API

        elif self.step_selection == '5':  # Создать открытку с текущей погодой
            self.weather_card()  # вызов метода работы с карточкой погоды

        elif self.step_selection == '6':  # Выйти из программы
            print('Выход из программы')
            exit()

    # метод работы с карточкой погоды
    def weather_card(self):
        self.current_weathe('weather_card')
        basedatabase.weather_now(
            'current_weather_card')  # обращение к  БД  на наличие записи текущей погоды - модуль  data_sampling.py

    # метод сообщения текущей погоды
    def present_weather_message(self):  # текущее сообщение о погоде
        print('≪ ≫' * 15)
        print(f'Погода в - {self.location.upper()} на сегодня')
        print('≪ ≫' * 15)

        print(f'Текущая температура:     {self.temp_city.__round__(2)} C')
        print(f'Текущая погода:          {self.weather_desc}')
        print(f'Текущая влажность:       {self.humidity} %')
        print(f'Текущая скорость ветра: {self.speed} m/c')
        print('≪ ≫' * 15)
        exit()

    # метод сообщения прогноза погоды за 5 дней
    def weather_forecast_message(self):
        print(f'Прогноз погоды на 5 дней - {self.location} ◆ {self.day_data["dt_txt"][:10]}')
        print(f"Температура: {self.temperature} С")
        print(f"Погода: {self.cloudiness}")
        print(f"Влажность: {self.humidity} %")
        print(f"Скорость ветра: {self.wind} м/c")
        print('≪ ≫' * 10)
        return

    # метод сообщения истории погоды за 5 дней - сейчас сервис отдает только за 3 дня
    def weather_history_message(self):
        print(f'Статистика  погоды за 5 прошлых дней для - {self.location}')
        print(f'Дата:{self.last_day} февраля 2022 года')
        print(f"Температура: {self.temperature} С")
        print(f"Погода: {self.cloudiness}")
        print(f"Влажность: {self.humidity} %")
        print(f"Скорость ветра: {self.wind} м/c")
        print('≪ ≫' * 10)
        return

    # метод текущей погоды
    def current_weathe(self, *args):

        try:
            if 'weather_card' in args[0]:
                # запрос к БД  data_sampling.py имеются ли там записи
                basedatabase.weather_now(self.location, args[0])
                raise

        except Exception as ex:
            # запрос к БД  data_sampling.py имеются ли там записи
            basedatabase.weather_now(self.location)

            self.current_time()
            self.complete_api_link = f'https://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={API}' \
                                     f'&lang={LANG}&units=metric'

            self.api_link = requests.get(self.complete_api_link)
            self.api_data = self.api_link.json()

            # выборка данных из json
            self.temp_city = (self.api_data['main']['temp'])
            self.weather_desc = self.api_data['weather'][0]['description']
            self.humidity = self.api_data['main']['humidity']
            self.speed = self.api_data['wind']['speed']

            # передача данных в словарь текущей погоды
            self.current_db['date'] = self.date
            self.current_db['location'] = self.location
            self.current_db['temperature'] = self.temp_city
            self.current_db['cloudiness'] = self.weather_desc
            self.current_db['humidity'] = self.humidity
            self.current_db['wind'] = self.speed

            # вызов функции модуля operations.py записи данных в БД
            try:
                if 'weather_card' in args[0]:
                    records_weather(self.current_db)
                    basedatabase.weather_now(self.location, args[0])
            except Exception:
                records_weather(self.current_db)

            # вызов функции сообщений прогноза текущей погоды
            self.present_weather_message()

    # метод прогноза погоды на 5 дней
    def period_data(self):
        # запрос к БД  data_sampling.py имеются ли там записи
        basedatabase.forecast_future(self.location)

        try:
            self.current_time()
            res = requests.get("https://api.openweathermap.org/data/2.5/forecast",
                               params={'id': self.city_id, 'units': 'metric', 'lang': 'ru', 'APPID': API})
            data = res.json()

            count = 0
            for self.day_data in data['list']:
                if count <= 5:  # сервис предоставляет прогноз только на 5 дней
                    if self.day_data["dt_txt"][11:13] == '15':  # берется погода на 15 часов
                        # выборка данных из json
                        self.temperature = self.day_data['main']['temp']
                        self.cloudiness = self.day_data['weather'][0]['description']
                        self.humidity = self.day_data['main']['humidity']
                        self.wind = self.day_data['wind']['speed']

                        year_month_day = self.day_data["dt_txt"][:10]

                        # перевод даты на российский формат
                        self.period_db['date'] = year_month_day[-2:] + '.' + year_month_day[6:7] + '.' + year_month_day[
                                                                                                         :4]

                        # передача данных в словарь прогноза погоды на 5 дней
                        self.period_db['location'] = self.location
                        self.period_db['temperature'] = self.temperature
                        self.period_db['cloudiness'] = self.cloudiness
                        self.period_db['humidity'] = self.humidity
                        self.period_db['wind'] = self.wind

                        # вызов функции модуля operations.py записи данных в БД
                        hy = self.period_db
                        records_period(self.period_db)

                        # вызов функции сообщений прогноза погоды за 5 дней
                        self.weather_forecast_message()
                        count += 1
                else:
                    exit()

        except Exception:
            print(f'Ошибка в методе прогноза погоды на 5 дней:{traceback.format_exc()}')

    # метод исторических данных погоды на 5 дней назад
    def weather_history(self):
        # запрос к БД  data_sampling.py имеются ли там записи
        basedatabase.weather_in_the_past(self.location)
        try:
            for day in range(1, 6):  # сервис предоставляет историю только на 5 дней
                self.current_time()  # получаю текущую дату
                self.last_day = self.last_day - day  # отматываю дату назад на 5 дней
                datetime = dt.datetime(self.this_year, self.current_month, self.last_day, 14, 00)
                unix_time = int(time.mktime(datetime.timetuple()))  # перевожу во время unix

                # получение широты и долготы населенного пункта
                get_latitude_longitude = f'https://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={API}'
                lon_lat = requests.get(get_latitude_longitude)
                lon_lat_data = lon_lat.json()
                lon = lon_lat_data['coord']['lon']
                lat = lon_lat_data['coord']['lat']

                # получение данных о погоде по API
                response = requests.get('https://api.openweathermap.org/data/2.5/onecall/timemachine?',
                                        params={'units': 'metric', 'lang': 'ru', 'lat': lat, 'lon': lon,
                                                'dt': unix_time,
                                                'appid': API})

                self.historical_data = response.json()

                # выборка данных из json
                self.temperature = self.historical_data['current']['temp']  # температура
                self.cloudiness = self.historical_data['current']['weather'][0]['description']  # Облачность
                self.humidity = self.historical_data['current']['humidity']  # влажность
                self.wind = self.historical_data['current']['wind_speed']  # скорость ветра

                # передача данных в словарь истории погоды предыдущих 5 дней
                self.history_db['date'] = datetime.strftime("%d.%m.%Y")
                self.history_db['location'] = self.location
                self.history_db['temperature'] = self.temperature
                self.history_db['cloudiness'] = self.cloudiness
                self.history_db['humidity'] = self.humidity
                self.history_db['wind'] = self.wind

                # вызов функции модуля operations.py записи данных в БД
                records_history(self.history_db)

                # функция сообщений истории погоды за 5 дней
                self.weather_history_message()

        except Exception:
            print(f'Ошибка в методе исторических данных:{traceback.format_exc()}')  # указывает номер строки ошибки


weather_maker = WeatherMaker()

if __name__ == '__main__':
    weather_maker.data_input()

