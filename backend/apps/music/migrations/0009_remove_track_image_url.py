# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20150803_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='image_url',
        ),
    ]
