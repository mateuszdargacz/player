# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_remove_track_was_played_today'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='date_added',
            field=models.DateField(auto_now=True),
            preserve_default=True,
        ),
    ]
