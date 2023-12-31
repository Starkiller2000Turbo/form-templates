# Проект шаблоны форм

### Описание:

Проект "Шаблоны форм" предназначен для хранения шаблонов форм в виде словарей с полем имени, а также полями дат, телефонов, email-адресов и текстов. 

### Как установить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Starkiller2000Turbo/form-templates.git
cd form-templates
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

LOG_LEVEL=
Уровень логирования.

```

### Как запустить бэкенд:

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
Заполнить базу данных случайными данными:

```
make fill
```

### Эндпоинты:

| Эндпоинт   |Тип запроса | Параметры запроса                       | Ответ                         |
|------------|------------|-----------------------------------------|-------------------------------|
|/get_forms/ |POST        | ?field1_name=value1&field2_name=value2  |```[{"name": "name1"}, ... ]```|


### Стек технологий использованный в проекте:

- Python
- Django
- TinyDB
- Logging
- Regex
- Validate_email


### Авторы:

- :white_check_mark: [Starkiller2000Turbo](https://gitlab.com/Starkiller2000Turbo)
