**О проекте:**
----------

Проект Api-Yatube

**Как запустить проект:**
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/ushakov-ya2016/api_yamdb
```
```
cd api_yamdb
```
2. Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
3. Обновите pip до последней версии:
```
python3 -m pip install --upgrade pip command
```
4. Установите необходимые зависимости:
```
pip install -r requirements.txt command
```
5. Создайте миграции:
```
python3 manage.py makemigrations
```
6. Примените миграции:
```
python3 manage.py migrate
```
7. Импортировать тестовые данные:
```
python3 manage.py import_csv
```
8. Создать суперпользователя для доступа к админке:
```
python3 manage.py createsuperuser
```
9. Запустить проект:
```
python3 manage.py runserver
```

**Полезные ссылки**
----------

Документация по API: http://127.0.0.1:8000/redoc/

Вход в панель администрирование: http://127.0.0.1:8000/admin/
