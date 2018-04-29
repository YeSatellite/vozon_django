from django.apps import AppConfig


class ClientConfig(AppConfig):
    name = 'apps.client'

    def ready(self):
        from . import signals
