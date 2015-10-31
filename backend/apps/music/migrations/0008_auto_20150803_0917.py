# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_track_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='track_list_new',
            new_name='track_list',
        ),
        migrations.AlterField(
            model_name='track',
            name='image',
            field=models.ImageField(null=True, upload_to=b'static/images/artists/', blank=True),
            preserve_default=True,
        ),
    ]
