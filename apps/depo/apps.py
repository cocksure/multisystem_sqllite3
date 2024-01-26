from django.apps import AppConfig


class DepoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.depo'

    def ready(self):
        import apps.depo.signals
