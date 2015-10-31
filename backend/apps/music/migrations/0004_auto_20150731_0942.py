# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_track_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='file',
            field=models.FileField(upload_to=b'static/tracks', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='image',
            field=models.ImageField(upload_to=b'static/images'),
            preserve_default=True,
        ),
    ]
