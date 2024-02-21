Курсовая №6.

1. Для запуска приложения необходимо настроить виртуальное окружение и установить все необходимые зависимости с помощью команд:

    1- python -m venv venv
    2- venv\Scripts\activate
    3- pip install -r requirement.txt
2. Для работы с переменными окружениями необходимо заполнить файл .env опираясь на .env.sample
3. Запустите Redis в отдельном терминале
4. Запустите Celery worker: celery -A config worker -P eventlet -l info
5. В отдельном терминале запустите Celery beat:  celery -A config.celery beat -l info
- client - приложение с CRUD по клиентам 
- client_service - приложение по рассылке спама, включает логи, настройки рассылок, и сообщение 
- config - в стандартный конфиг, добавила celery.py с допю настройками для работы celery,
так же необходимые настройки по celery добавила в init
- materials - блог (механизм CRUD)


