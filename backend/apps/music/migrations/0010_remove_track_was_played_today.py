# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_remove_track_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='was_played_today',
        ),
    ]
