# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0015_auto_20150813_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='name',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='tracktochart',
            unique_together=set([('track', 'chart')]),
        ),
        migrations.AlterUniqueTogether(
            name='usertochart',
            unique_together=set([('user', 'chart')]),
        ),
    ]
