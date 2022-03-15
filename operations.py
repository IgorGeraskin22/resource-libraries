# -*- coding: utf-8 -*-
from models import *

db.create_tables([Weather, Period, History])  # создание таблиц


# запись в БД текущей погоды
def records_weather(*args):
    # если записей равно 1, то это устаревшая запись - удаление и запись новой
    if len(Weather.select()) == 1:
        Weather[1].delete_instance()
        Weather.insert_many(args).execute()
    else:
        Weather.insert_many(args).execute()


# запись в БД прогноза погоды на 5 дней
def records_period(*args):
    # если записей равно 5, то это устаревшие записи - удаление и запись новых
    if len(Period.select()) == 5:
        [Period[id_].delete_instance() for id_ in range(1, 6)]
        Period.insert_many(args).execute()

    else:
        Period.insert_many(args).execute()


# запись в БД прошлых 5 дней
def records_history(*args):
    # если записей равно 3, то это устаревшие записи - удаление и запись новых
    if len(History.select()) == 5:
        [History[id_].delete_instance() for id_ in range(1, 6)]
        History.insert_many(args).execute()

    else:
        History.insert_many(args).execute()
