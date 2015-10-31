# -*- coding: utf-8 -*- 
__author__ = 'michal'

from django.contrib.admin import register

from apps.users.models import User

register(User)