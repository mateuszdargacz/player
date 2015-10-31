# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0017_auto_20150818_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='style',
            field=models.ManyToManyField(to='music.Style', blank=True),
            preserve_default=True,
        ),
    ]
