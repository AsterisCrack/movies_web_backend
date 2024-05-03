from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.movies" # Cambiar el nombre de la app a "apps.movies" para que Django la reconozca
