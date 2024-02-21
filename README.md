Курсовая №6.

1. Для запуска приложения необходимо настроить виртуальное окружение и установить все необходимые зависимости с помощью команд:

    1- python -m venv venv
    2- venv\Scripts\activate
    3- pip install -r requirement.txt
2. Для работы с переменными окружениями необходимо заполнить файл .env опираясь на .env.sample
3. Запустите Redis в отдельном терминале
4. Запустите Celery worker: celery -A config worker -P eventlet -l info
5. В отдельном терминале запустите Celery beat:  celery -A config.celery beat -l info


