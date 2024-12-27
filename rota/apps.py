from django.apps import AppConfig


class RotaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rota'


class RotaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rota'

    def ready(self):
        import rota.signals  # Ensure signals are loaded
