# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0016_auto_20150813_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='track',
            name='style',
            field=models.ManyToManyField(to='music.Style'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='year',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='link',
            field=models.CharField(unique=True, max_length=254, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(max_length=254),
            preserve_default=True,
        ),
    ]
