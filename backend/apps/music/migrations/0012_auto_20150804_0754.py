# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0011_auto_20150803_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='category',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
