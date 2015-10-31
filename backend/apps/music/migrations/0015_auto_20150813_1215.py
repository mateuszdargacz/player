# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_auto_20150812_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='link',
            field=models.CharField(unique=True, max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([('title', 'artist')]),
        ),
    ]
