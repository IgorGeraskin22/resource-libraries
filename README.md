Задание и решение
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
**************************************************************************************************
Task and solution
# In another rush, after checking the weather app, you ran out
# towards the review of your code that was waiting for you at the office.
# And then the day became worse - instead of the promised cloudiness, you were greeted by a downpour.

# You were wet, the mood was spoiled, and you already came to the review in a bad mood.
# As a result of such a crushing day, you decide to write your own weather program
# from a source you trust.

# For this you need:

# Create an engine module with the WeatherMaker class needed to receive and generate predictions.
# It should have a method that receives a forecast from the site you selected (parsing + re) for a certain date range,
# and then, having received the data, form it into a dictionary {weather: Cloudy, temperature: 10, date:datetime...}

# Add an ImageMaker class.
# Provide it with a postcard drawing method
# (use OpenCV, take lesson_016/python_snippets/external_data/probe.jpg as a blank):
# With text consisting of received data (cv2.putText will come in handy)
# With an image corresponding to the type of weather
# (stored in lesson_016/python_snippets/external_data/weather_img , but you can draw/add your own)
# As a background, add a color gradient that reflects the type of weather
# Sunny - yellow to white
# Rain - blue to white
# Snow - blue to white
# Cloudy - gray to white

# Add a DatabaseUpdater class with methods:
# Retrieving data from the database for the specified date range.
# Save predictions to database (use peewee)

# Make a program with a console interface, trying to put all the actions performed into separate functions.
# Among the actions available to the user should be:
# Add forecasts for a range of dates to the database
# Getting forecasts for a range of dates from the database
# Create postcards from received forecasts
# Outputting received forecasts to the console
# At startup, the console utility should load forecasts for the past week.

# Recommendations:
# You can create a separate module to initialize the database.
# How to further use this database in the engine:
# Pass DatabaseUpdater url path
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Connect using the given url-path to the database
# Initialize it via DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database
