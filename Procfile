release: python manage.py migrate
web: gunicorn SpogoScore.wsgi --log-file -
web: python manage.py runserver 0.0.0.0:$PORT --noreload