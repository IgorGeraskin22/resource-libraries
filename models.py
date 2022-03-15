# -*- coding: utf-8 -*-
from peewee import *
import datetime

# Модели это таблицы в базе данных
# Это столбцы в этой таблице

db = SqliteDatabase('weather.db')


class BaseModel(Model):  # базовый класс, который включает в себя общие инструкции

    id = PrimaryKeyField(unique=True)  # обозначаем как уникальный первичный ключ
    date = DateTimeField()  # дата
    location = CharField()  # локация
    temperature = IntegerField()  # температура
    cloudiness = CharField()  # погода
    humidity = IntegerField()  # влажность в %
    wind = IntegerField()  # скорость ветра

    # order_by = 'id'  # по каким полям данные будут сортироваться по умолчанию

    # привязка к базе данных
    class Meta:  # для точной и индивидуальной настройки. Здесь указываются дополнительные параметры работы модели
        database = db  # Указываю с какой базой работать


class Weather(BaseModel):  # Weather - имя таблицы
    db_table = 'Weather'  # к какой таблице обращаться


class Period(BaseModel):
    db_table = 'Period'  # к какой таблице обращаться


class History(BaseModel):
    db_table = 'History'  # к какой таблице обращаться
