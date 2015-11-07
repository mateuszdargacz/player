# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0019_defaultvalues_max_user_songs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultvalues',
            name='max_user_songs',
            field=models.IntegerField(default=10),
            preserve_default=True,
        ),
    ]
