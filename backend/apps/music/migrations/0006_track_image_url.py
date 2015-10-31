# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_remove_track_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='image_url',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
    ]
