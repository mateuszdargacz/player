# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_user_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='votes',
        ),
    ]
