# -*- coding: utf-8 -*- 
__author__ = 'michal'

from django.apps import AppConfig


class APIConfig(AppConfig):
    name = 'apps.api'
    verbose_name = 'REST and SOCKET API'

    def ready(self):
        import sockets.events
        pass
