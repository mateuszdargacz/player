# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0021_defaultvalues_balance_playlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultvalues',
            name='votes_expire_daily',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
