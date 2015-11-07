# -*- coding: utf-8 -*-
__author__ = 'mateuszb'

import datetime

from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.db import models

from apps.music.models import Vote, DefaultValues


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address')
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username')
        user = self.model(email=self.normalize_email(email), username=kwargs.get('username'))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=35, unique=True)
    is_admin = models.BooleanField(default=False)
    # votes = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='static/images/avatars/', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __unicode__(self):
        return self.email

    def get_vote(self):
        return Vote.objects.filter(user=self).count()

    @property
    def get_todays_vote(self):
        return Vote.objects.filter(user=self, date_added=datetime.date.today())

    @property
    def get_votes(self):
        return Vote.objects.filter(user=self)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def get_avatar(self):
        if bool(self.avatar):
            return self.avatar.url
        else:
            return DefaultValues.objects.last().user_image.url

