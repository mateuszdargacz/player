# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0020_auto_20151107_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultvalues',
            name='balance_playlist',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
