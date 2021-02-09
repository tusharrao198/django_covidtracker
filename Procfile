release: python manage.py migrate --noinput
release: python manage.py collectstatic --noinput
web: gunicorn web_main.wsgi:application --log-file - --log-level debug