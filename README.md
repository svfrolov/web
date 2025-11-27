# Инструкция по запуску приложения с PostgreSQL в Docker

## Шаг 1: Запуск PostgreSQL в Docker
```
docker-compose up -d
```
Эта команда запустит контейнер PostgreSQL в фоновом режиме.
Убедитесь, что Docker запущен на вашем компьютере.

## Шаг 2: Проверка статуса контейнера
```
docker ps
```
В списке должен быть контейнер postgres_db, статус "Up".

## Шаг 3: Запуск Django-приложения
```
python manage.py runserver
```
Приложение будет доступно по адресу http://127.0.0.1:8000/

## Дополнительные команды

### Остановка контейнера PostgreSQL
```
docker-compose down
```

### Перезапуск контейнера PostgreSQL
```
docker-compose restart
```

### Просмотр логов PostgreSQL
```
docker-compose logs
```

### Создание суперпользователя Django (если нужно)
```
python manage.py createsuperuser
```

### Применение миграций (если были изменения в моделях)
```
python manage.py makemigrations
python manage.py migrate
```

## Важно
- База данных PostgreSQL настроена с кодировкой UTF-8 для корректной работы с русскими символами
- Данные сохраняются в Docker-томе postgres_data и не будут потеряны при перезапуске контейнера
- Настройки подключения к базе данных находятся в файле tech_service/settings.py

## Параметры подключения к PostgreSQL
- Хост: localhost
- Порт: 5432
- База данных: mydatabase
- Пользователь: postgres
- Пароль: postgres