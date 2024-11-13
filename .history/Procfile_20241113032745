release: python tech_api/manage.py collectstatic --noinput
web: gunicorn tech_api.wsgi:application --log-file -
