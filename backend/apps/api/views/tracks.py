# -*- coding: utf-8 -*- 
__author__ = 'mateuszb'
import json

from django.core.exceptions import ValidationError

from rest_framework import status, views
from rest_framework.response import Response

from apps.users.models import User
from apps.music.models import Track, TracktoChart, Chart, Vote, LimitReached, DefaultValues

try:
    ADMIN_USER = User.objects.get(username='automat')
except User.DoesNotExist:
    ADMIN_USER = User.objects.get(id=1)


class TrackView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)
        data['added_by'] = User.objects.get(id=data['added_by'])
        chart_id = data['playlist']
        del data['playlist']
        try:
            track = Track.objects.create(**data)
            try:
                chart = Chart.objects.get(id=chart_id)
                TracktoChart.objects.create(track=track, chart=chart)
                if DefaultValues.objects.first().balance_playlist:
                    for x in range(0, chart.votes_average):
                        Vote.objects.create(user=ADMIN_USER, chart=chart, track_id=track, up_vote=True)

            except Chart.DoesNotExist or ValidationError:
                return Response({
                    'status': 'Failed',
                    'message': 'The track could not be added to playlist.'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': 'OK',
                'message': 'The track has been added.'
            }, status=status.HTTP_201_CREATED)
        except LimitReached as e:
            return Response({
                'status': 'Failed',
                'message': '%s' % e
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'status': 'Failed',
                'message': 'The track could not be added. Process failed with: %s' % e
            }, status=status.HTTP_400_BAD_REQUEST)
