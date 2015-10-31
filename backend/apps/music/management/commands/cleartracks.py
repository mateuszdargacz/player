# -*- coding: utf-8 -*- 
__author__ = 'mateuszb'

from django.core.management.base import BaseCommand, CommandError
from apps.music.models import TracktoChart


class Command(BaseCommand):
    help = 'Changes was_played field to False for all TracktoChart objects'

    def handle(self, *args, **options):
        tracks = TracktoChart.objects.all()
        for track in tracks:
            track.was_played_today = False
            track.save()
        self.stdout.write('Successfully set all tracks as not played')
