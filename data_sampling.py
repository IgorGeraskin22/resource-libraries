# -*- coding: utf-8 -*-
import peewee
from prettytable import PrettyTable
from models import *
from card import *

HEADER_TABLE = ['Дата', 'Город', 'Температура,C', 'Осадки/Облачность', 'Влажность,%', 'Скорость ветра,m/c']


class BaseDatabase:
    def __init__(self):
        self.data_table = None
        self.args = None
        self.columns = None
        self.td_data = None
        self.query = None
        self.table = None
        self.td = []

    def weather_now(self, *args):  # погода сейчас
        self.query = Weather.select()
        self.check_db_weather_data(args)

    def forecast_future(self, *args):  # прогноз на будущее 5 дней
        self.query = Period.select()

        self.check_db_weather_data(args)
        # k = self.td[1]
        # return self.td[1]

    def weather_in_the_past(self, *args):  # погода прошлых 5 дней
        self.query = History.select()
        self.check_db_weather_data(args)

    def message(self):
        print(self.table)

    def check_db_weather_data(self, *args):
        # проверка, если в базе данные о погоде
        if self.query:
            self.td = []
            for self.data_table in self.query:
                self.td.extend(
                    [self.data_table.date, self.data_table.location, self.data_table.temperature, self.data_table.cloudiness,
                     self.data_table.humidity, self.data_table.wind]
                )

                self.columns = len(HEADER_TABLE)
                self.table = PrettyTable(HEADER_TABLE)
                self.td_data = self.td[:]
            if args[0][0] in self.td[1]:
                self.conditions_choosing_weather_card(args, self.td_data, self.table)

    # метод условий выбора карты погоды
    def conditions_choosing_weather_card(self, *args):
        try:
            if 'weather_card' in args[0][0][1]:
                # создание карточки в методе cloudy()  модуля card.py
                if 'пасмурно' in self.td_data[3] or 'переменная облачность' in self.td_data[3] \
                        or 'облачно с прояснениями' in self.td_data[3] or 'небольшая облачность' in self.td_data[3] \
                        or 'туман' in self.td_data[3] or 'мгла' in self.td_data[3]:
                    weathercard.cloudy(self.td[0], self.td[1], self.td[2], self.td[3], self.td[4], self.td[5])
                    exit()

                # создание карточки в методе snow()  модуля card.py
                if 'небольшой снегопад' in self.td_data[3] or 'небольшой снег' in self.td_data[3] or 'снег' in \
                        self.td_data[3]:
                    weathercard.snow(self.td[0], self.td[1], self.td[2], self.td[3], self.td[4], self.td[5])
                    exit()

                # создание карточки в методе rain()  модуля card.py
                if 'дождь' in self.td_data[3] or 'небольшой дождь' in self.td_data[3]:
                    weathercard.rain(self.td[0], self.td[1], self.td[2], self.td[3], self.td[4], self.td[5])
                    exit()

                # создание карточки в методе solar()  модуля card.py
                if 'ясно' in self.td_data[3]:
                    weathercard.solar(self.td[0], self.td[1], self.td[2], self.td[3], self.td[4], self.td[5])
                    exit()

        except Exception:
            count = 0
            while self.td_data:
                self.table.add_row(self.td_data[:self.columns])
                self.td_data = self.td_data[self.columns:]
                h = self.data_table
                gh = type(self.data_table)
                if self.data_table in Weather:
                    self.message()
                    exit()
                count += 1
                if count == 5:
                    self.message()
                    exit()


basedatabase = BaseDatabase()
