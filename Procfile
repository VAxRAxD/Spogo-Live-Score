release: python manage.py migrate
web: gunicorn SpogoScore.wsgi --log-file -
python manage.py runserver 0.0.0.0:$PORT --noreload
