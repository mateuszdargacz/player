# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('artist', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=b'tracks', blank=True)),
                ('link', models.CharField(max_length=500, blank=True)),
                ('type', models.CharField(max_length=50, blank=True)),
                ('was_played_today', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(related_name='tracks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TracktoChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('was_played_today', models.BooleanField(default=False)),
                ('chart', models.ForeignKey(to='music.Chart')),
                ('track', models.ForeignKey(to='music.Track')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsertoChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chart', models.ForeignKey(to='music.Chart')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField()),
                ('up_vote', models.BooleanField(default=False)),
                ('chart', models.ForeignKey(related_name='chart', default=1, to='music.Chart')),
                ('track_id', models.ForeignKey(related_name='votes', to='music.Track')),
                ('user', models.ForeignKey(related_name='vote_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tracktochart',
            name='votes',
            field=models.ManyToManyField(to='music.Vote', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chart',
            name='invited_new',
            field=models.ManyToManyField(related_name='user_invited', through='music.UsertoChart', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chart',
            name='owned_by',
            field=models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chart',
            name='track_list_new',
            field=models.ManyToManyField(related_name='newTracklist', through='music.TracktoChart', to='music.Track', blank=True),
            preserve_default=True,
        ),
    ]
