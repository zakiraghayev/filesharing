release: python manage.py migrate

web: gunicorn filesharing.wsgi --log-file -

worker: python manage.py rqworker default