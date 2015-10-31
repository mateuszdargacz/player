# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_defaultvalues'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defaultvalues',
            name='user_avatar',
        ),
        migrations.AddField(
            model_name='defaultvalues',
            name='user_image',
            field=models.ImageField(upload_to=b'static/images/defaults/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='defaultvalues',
            name='song_image',
            field=models.ImageField(upload_to=b'static/images/defaults/', blank=True),
            preserve_default=True,
        ),
    ]
