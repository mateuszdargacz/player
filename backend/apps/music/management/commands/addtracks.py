# -*- coding: utf-8 -*-

__author__ = 'mateuszb'

import json

from django.core.management.base import BaseCommand

from apps.users.models import User
from apps.music.models import Track


class Command(BaseCommand):
    help = 'Adds tracks from json(old database)'

    def handle(self, *args, **options):
        path_track = 'res/tracks'
        path_users = 'res/users'
        json_tracks = open(path_track).read()
        json_users = open(path_users).read()
        tracks = json.loads(json_tracks)
        users = json.loads(json_users)
        for track in tracks:
            if not track['file'] and track['link']:
                name = users[track['added_by_id']-1]['username']
                if name == 'Mateuszek':
                    user = User.objects.get(username='Mati')
                elif name == 'kamil_d':
                    user = User.objects.get(username='kamil')
                else:
                    user = User.objects.get(username=name)
                if track['type'] == 'youtube':
                    link = 'https://www.youtube.com/watch?v=' + track['link']
                else:
                    link = track['link']
                if not Track.objects.filter(link=link).count() and not Track.objects.filter(title=track['title'], artist=track['artist']).count():
                    Track.objects.create(artist=track['artist'], title=track['title'], link=link, added_by=user)
        self.stdout.write('Successfully added all tracks')