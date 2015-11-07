# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0018_auto_20150818_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultvalues',
            name='max_user_songs',
            field=models.ImageField(default=10, upload_to=b''),
            preserve_default=True,
        ),
    ]
