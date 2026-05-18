from django.apps import AppConfig


class EcommConfig(AppConfig):
    name = 'ecomm'
    default_auto_field = 'django.db.models.BigAutoField'
    def ready(self):
        import ecomm.signals

