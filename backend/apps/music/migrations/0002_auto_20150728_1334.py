# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='tracks_to_play',
            field=models.IntegerField(default=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chart',
            name='votes_per_day',
            field=models.IntegerField(default=25),
            preserve_default=True,
        ),
    ]
