# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_last_visit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_visit',
        ),
        migrations.AddField(
            model_name='user',
            name='online',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
