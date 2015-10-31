"""
WSGI config for music_player project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
from sys import path

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)
path.insert(0, PROJECT_ROOT)
# settings_module = "%s.settings" % APP_ROOT.split(os.sep)[-1]
os.environ["DJANGO_SETTINGS_MODULE"] = "music_player.settings"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
