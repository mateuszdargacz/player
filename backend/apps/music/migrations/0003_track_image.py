# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20150728_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='image',
            field=models.ImageField(default=b'static/images/stachu.jpg', upload_to=b'static/images'),
            preserve_default=True,
        ),
    ]
