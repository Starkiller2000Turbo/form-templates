# Проект Interactive-maps-DW

Ссылка на проект на сервере:
- :white_check_mark: [Бэкенд на сервере](http://v2191582.hosted-by-vdsina.ru/)
- :white_check_mark: [Фронтенд](http://mycharts.site/)
### Описание:

Проект Interactive-maps-DW - вервис для отслеживания движения поездов.

В данном проекте реализовано получение данных о сети станций, а также получение данных о поездах по их индексам.

Реализовано также заполнение базы данных из файлов excel с помощью Pandas.

### Как установить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@gitlab.com:valentin_oneone/interactive-maps-dw.git
cd interactive-maps-dw
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source venv/bin/activate
```

Одновить pip и установить зависимости из файла requirements.txt:

```
make pip
make req
```

Для работы приложения необходим файл .env:

```
touch .env
```

Необходимо заполнить файл .env следующим обазом:

```
SECRET_KEY=  
Секретный ключ для работы django.

DEBUG=
True/False в зависимости от необходимости режима отладки.

ALLOWED_HOSTS= 
Допустимые хосты, на которых будет работать приложение через пробел. 
Для локальной работы приложения - localhost и 127.0.0.1, для работы на сервере - также доменное имя и ip адрес. 

DATABASES= 
SQL в случае работы с файлом db.sqlite3, при работе с Postgres - любое другое значение. Другие базы данных не поддерживаются.

LOG_LEVEL=
Уровень логирования.

POSTGRES_DB= 
Название базы данных postgres.

POSTGRES_USER=
Имя пользователя базы данных postgres.

POSTGRES_PASSWORD=
Пароль пользователя базы данных postgres.

DB_NAME=
Имя базы данных.

DB_HOST=
Адрес связи с базой данных.

DB_PORT=
Порт связи с базой данных.

```
### Подготовка файлов с данными:

Чтобы заполнить данными систему, необходимо использовать 3 файла с расширением xlsx.
Разместить их необходимо в папке data, расположенной внутри папки interactive_maps_dw

```
cd interactive_maps_dw
mkdir data
cd data
```

#### Файл STATION_COORDS_HACKATON.xlsx:

| Заголовок (пример)| ST_ID                   | LATITUDE                 | LONGITUDE                |
|-------------------|-------------------------|--------------------------|--------------------------|
| Описание          | Уникальный id станции   | Широта (геогр.) станции  | Долгота (геогр.) станции |
| Примеры значений  | 2, 23, 37, 73, 5981     | -15.05, 0.0 46.567, 10.0 |-15.05, 0.0 46.567, 10.0  |

#### Файл PEREGON_HACKATON.xlsx:

| Заголовок (пример)| START_CODE              | END_CODE                 | LEN                      |
|-------------------|-------------------------|--------------------------|--------------------------|
| Описание          | id станции отправления  | id станции назначения    | Длина пути (км)          |
| Примеры значений  | 2, 23, 37, 73, 5981     | 2, 23, 37, 73, 5981      | 2, 23, 37, 73, 5981      |

#### Файл DISL_HACKATON.xlsx:

| Заголовок (пример)| WAGNUM        | OPERDATE              | ST_ID_DISL         | ST_ID_DEST            | TRAIN_INDEX   |
|-------------------|---------------|-----------------------|--------------------|-----------------------|---------------|
| Описание          | номер вагона  | время создания записи | id текущей станции | id станции назначения | Индекс поезда. Состоит из 3-х чисел, разделенных двоеточием: id станции отправления поезда, номер поезда, id конечной станции |
| Примеры значений  | 2, 23, 37, 73 | 30.08.2023 1:02:00    | 2, 23, 37, 73      | 2, 23, 37, 73, 5981   | 123-654-789   |


### Как запустить бэкенд без контейнеров:

Выполнить миграции:

```
make migrations
make migrate
```

Создать учетную запись администратора:

```
make superuser
```

Запустить приложение:

```
make run
```
Заполнить базу данных заранее собранными данными:

```
make import
```

Импортировать только данные конкретного файла:

```
make stations
make tracks
make records
```

### Как запустить бэкенд проект в контейнерах:

Запустить проект локально:

```
docker compose up
```

Выполнить миграции:

```
docker compose exec interactive_maps_dw python manage.py migrate
```

Собрать статику:
```
docker compose exec interactive_maps_dw python manage.py collectstatic
docker compose exec interactive_maps_dw cp -r /app/collected_static/. /backend_static/static/
```

Заполнить базу данных заранее собранными данными:
```
docker compose exec interactive_maps_dw python manage.py import_tags
docker compose exec interactive_maps_dw python manage.py import_ingredients
```

### Эндпоинты:

| Эндпоинт                             |Тип запроса | Тело запроса | Ответ           |
|--------------------------------------|------------|--------------|-----------------|
|/railway_wish_card/stations/          |GET         |              |```{"type": "FeatureCollection", "metadata": [{"id": int, "coordinates": [float, float], "color": "#hex"}, ... ]}```|
|/railway_wish_card/stations/{id}      |GET         |              |```{"type": "FeatureCollection", "metadata": [{"id": int, "coordinates": [float, float], "color": "#hex"}, ... ]}```|
|/railway_wish_card/stations/pagination|GET         |              |```{"pagination": int}```|
|/railway_wish_card/stations-test-100  |GET         |              |```[{"id": "2", "coordinates": [float, float], "color": "#hex"}, ... ] ```|
|/train/{train_index}                  |GET         |              |```[{"id": "unique_val","coordinates": [[float, float],[float, float]],"color": "#hex"},{"id": "2","coordinates": [[float,float],[float,float]],"color": "#hex"}] ```|


### Стек технологий использованный в проекте:

- JavaScript
- API Яндекс Карты
- Python
- Django
- PostgreSQL
- Docker
- Docker-compose
- Nginx

### Авторы:

- :white_check_mark: [Lev4iks](https://gitlab.com/Lev4iks)
- :white_check_mark: [Sergey-1221](https://gitlab.com/Sergey-1221)
- :white_check_mark: [Starkiller2000Turbo](https://gitlab.com/Starkiller2000Turbo)
- :white_check_mark: [valentin_oneone](https://gitlab.com/valentin_oneone)
