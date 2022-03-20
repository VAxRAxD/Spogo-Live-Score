from django.apps import AppConfig
from . jobs import start


class ScoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Score'

    def ready(self):
        start()