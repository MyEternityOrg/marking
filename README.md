## Система маркировки Честный Знак

Основные системные требования:

* Ubuntu 22.04 / Windows 10+
* Python 3.10 + https://www.python.org/downloads/
* Git https://git-scm.com/download/

### Запуск приложения Windows

Клонирование репозитория

* git clone https://github.com/MyEternityOrg/marking.git
* cd marking
* git pull

Создание виртуального окружения
* python -m venv venv
* venv\scripts\python.exe -m pip install --upgrade pip
* venv\Scripts\pip install -r requirements.txt
  Создание файла настроек проекта
* IF NOT EXIST .env copy .env.sample .env

Настройка параметров подключения к СУБД в .env

```
ENGINE_SECRET_KEY = 'django-insecure-***'
SQL_ENGINE = 'mssql'
SQL_DB_NAME = 'dbname'
SQL_DB_USER = 'login'
SQL_DB_PASSWORD = 'password'
SQL_DB_HOST = 'server'
SQL_DB_PORT = 1433 
```

Запуск приложения

* venv\Scripts\python manage.py runserver 0.0.0.0:8000