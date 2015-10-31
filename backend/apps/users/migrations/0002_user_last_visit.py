# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 10, 21, 21, 110513, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
