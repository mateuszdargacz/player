# -*- coding: utf-8 -*-
from django.conf import settings

__author__ = 'michal'

import datetime
import operator

from django.utils import timezone
from django.shortcuts import get_object_or_404

from apps.music.models import Track, Chart, Vote, TracktoChart, UsertoChart, DefaultValues
from apps.api.serializers import TrackSerializer, ChartSerializer, UserSerializer, VoteSerializer, AllChartSerializer, \
    SimpleChartSerializer, UsertoChartSerializer, TrackListSerializer, NewTracksSerializer, MessageSerializer
from apps.users.models import User
from apps.chat.models import Message, Chat
import redis

try:
    ADMIN_USER = User.objects.get(username='automat')
except User.DoesNotExist:
    ADMIN_USER = User.objects.create_superuser('automat@zgon.xyz', 'automat', **dict(username='automat'))


class Redis():
    connection = None

    def __init__(self, *args, **kwargs):
        self.connection = self.get_connection()

    def get_connection(self):
        return self.connection or redis.StrictRedis(settings.REDIS_ENDPOINT_HOST, settings.REDIS_ENDPOINT_PORT)

    def add_to_users(self, k, v):
        self.get_connection().hset('users_online', k, v)

    def del_from_users(self, k):
        self.get_connection().hdel('users_online', k)

    def get_all_users(self):
        return set(self.get_connection().hvals('users_online'))

    def get_user(self, k):
        return self.get_connection().hget('users_online', k)

    def add_to_now_playing(self, k, v):
        self.get_connection().hset('now_playing', k, v)

    def get_now_playing(self, k):
        return self.get_connection().hget('now_playing', k)

    def del_from_now_playing(self, k):
        self.get_connection().hdel('now_playing', k)

red = Redis()

def no_action(request, socket, context, message):
    raise Exception('Action not "%s" defined' % message.get('action'))


def send_text(request, socket, context, message=None):
    socket.send(dict(action='change_title', text=message['text'] + " from server"))


def track_list(request, socket, context, message):
    track = Track.objects.all()
    serialized = TrackListSerializer(track, many=True)
    socket.send(dict(action='track_list', tracks=serialized.data))


def create_playlist(request, socket, context, message):
    user = User.objects.get(username=red.get_user(socket.session.session_id))
    chart = Chart.objects.create(owned_by=user, name=message['name'])
    UsertoChart.objects.create(user=user, chart=chart)
    UsertoChart.objects.create(user=ADMIN_USER, chart=chart)


def users_playlists(request, socket, context, message):
    user = User.objects.get(username=red.get_user(socket.session.session_id))
    u2c = UsertoChart.objects.filter(user=user)
    followed_playlist = []
    for u in u2c:
        serialized = SimpleChartSerializer(u.chart)
        followed_playlist.append(serialized.data)
    socket.send(dict(action='users_playlists', text=followed_playlist))


def get_playlist(request, socket, context, message):
    chart = get_object_or_404(Chart, id=message['playlist'])
    serialized = ChartSerializer(chart)
    serialized.data['track_list'] = sorted(serialized.data['track_list'],
                                           key=operator.itemgetter('total_relative_votes'), reverse=True)
    if len(serialized.data['track_list']) > chart.tracks_to_play:
        serialized.data['track_list'] = serialized.data['track_list'][:chart.tracks_to_play]
    user = User.objects.get(username=red.get_user(socket.session.session_id))
    try:
        u2c = UsertoChart.objects.get(user=user, chart=chart)
        serialized_u2c = UsertoChartSerializer(u2c)
        followers = get_followers(request, socket, context, message)
        socket.send_and_broadcast(
            dict(action='get_playlist', text=serialized.data, votes_left=serialized_u2c.data, followers=followers))
    except UsertoChart.DoesNotExist:
        pass
    socket.send(dict(action='playing_now', playlist=message['playlist'], track=red.get_now_playing(message['playlist'])))


def get_all_playlists(request, socket, context, message):
    charts = Chart.objects.all()
    serialized = AllChartSerializer(charts, many=True)
    socket.send_and_broadcast(dict(action='get_all_playlists', text=serialized.data))


def add_to_playlist(request, socket, context, message):
    track = Track.objects.get(id=message['track'])
    chart = Chart.objects.get(id=message['playlist'])
    if not TracktoChart.objects.filter(track=track, chart=chart).count():
        TracktoChart.objects.create(track=track, chart=chart)
        for x in range(0, chart.votes_average):
            Vote.objects.create(user=ADMIN_USER, chart=chart, track_id=track, up_vote=True)
        get_playlist(request, socket, context, message)


def follow_playlist(request, socket, context, message):
    u2c = UsertoChart()
    chart = Chart.objects.get(id=message['playlist'])
    user = User.objects.get(username=red.get_user(socket.session.session_id))
    u2c.user = user
    u2c.chart = chart
    try:
        u2c.save()
        users_playlists(request, socket, context, message)
        get_all_playlists(request, socket, context, message)
    except:
        # Inform that user can't follow this playlist
        pass


def unfollow_playlist(request, socket, context, message):
    chart = Chart.objects.get(id=message['playlist'])
    user = User.objects.get(username=red.get_user(socket.session.session_id))
    try:
        u2c = UsertoChart.objects.get(chart=chart, user=user)
        u2c.delete()
    except:
        # Inform that user can't unfollow this playlist
        pass
    users_playlists(request, socket, context, message)
    get_all_playlists(request, socket, context, message)


def get_username(request, socket, context, message):
    username = message['username']
    red.add_to_users(socket.session.session_id, username)


def users_online(request, socket, context, message):
    if message['send']:
        users = []
        for r in red.get_all_users():
            try:
                user = User.objects.get(username=r)
                users.append(user)
            except:
                pass
        serialized = UserSerializer(users, many=True)
        socket.send_and_broadcast(dict(action='users_online', users=serialized.data))


def make_vote(request, socket, context, message, up):
    user = User.objects.get(username=red.get_user(socket.session.session_id))
    chart = Chart.objects.get(id=message['playlist'])
    track = Track.objects.get(id=message['track'])
    t2c = TracktoChart.objects.get(track=track, chart=chart)
    vote = Vote.objects.filter(user=user, chart=chart, track_id=track, up_vote=not up).last()
    if vote:
        vote.delete()
    else:
        Vote.objects.create(user=user, chart=chart, track_id=track, up_vote=up)


def up_vote(request, socket, context, message):
    make_vote(request, socket, context, message, True)
    get_playlist(request, socket, context, message)
    message['send'] = True


def down_vote(request, socket, context, message):
    make_vote(request, socket, context, message, False)
    get_playlist(request, socket, context, message)
    message['send'] = True


def latest_songs(request, socket, context, message):
    track = Track.objects.order_by('-id')[:8]
    serialized = NewTracksSerializer(track, many=True)
    socket.send(dict(action='latest_songs', songs=serialized.data))


def latest_votes(request, socket, context, message):
    votes = Vote.objects.exclude(user=ADMIN_USER).order_by('-id')[:10]
    serialized = VoteSerializer(votes, many=True)
    socket.send(dict(action='latest_votes', votes=serialized.data))


def messages_chat(request, socket, context, message):
    messagechat = list(Message.objects.order_by('date_chat'))
    messagechat = messagechat[-30:]
    serialized = MessageSerializer(messagechat, many=True)
    socket.send(dict(action='chatBackEnd', chat_field=serialized.data))


def update_messages(request, socket, context, message):
    u = User.objects.get(username=red.get_user(socket.session.session_id))
    chat = Chat.objects.get(id=1)
    q = Message(text_chat=message['newmessage'], date_chat=timezone.now(), user=u, chat=chat)
    q.save()
    serialized = MessageSerializer(q)
    socket.send_and_broadcast(dict(action='chatBackEndOneMessage', chat_field=serialized.data))


def was_played(request, socket, context, message):
    t2c = TracktoChart.objects.get(track=message['track'], chart=message['playlist'])
    t2c.was_played_today = True
    t2c.save()
    red.del_from_now_playing(message['playlist'])
    # socket.broadcast(dict(action='was_played', users=serialized.data))
    get_playlist(request, socket, context, message)


def load_message_previous(request, socket, context, message):
    message_prev = []
    counter_messages = message['lengthChatComment']
    message_chat_all = list(Message.objects.order_by('date_chat'))
    lengthtab = len(message_chat_all)
    # on start load 30 messages and load 10 previous messages when scroll on top
    start_for = lengthtab - counter_messages - 30 - 10
    end_for = lengthtab - counter_messages - 30

    for i in range(start_for + 3, end_for + 3):
        message_prev.append(message_chat_all[i])

    serialized = MessageSerializer(message_prev, many=True)
    socket.send(dict(action='loadMessagePrevious', chat_field=serialized.data))


def playing_now(request, socket, context, message):
    red.add_to_now_playing(message['playlist'], message['track'])
    socket.send_and_broadcast(message=message)


def set_volume(request, socket, context, message):
    socket.broadcast(dict(action='set_volume', volume=message['volume'], playlist=message['playlist']))


def get_followers(request, socket, context, message):
    chart = Chart.objects.get(id=message['playlist'])
    serialized = UserSerializer(chart.get_followers(instances=True), many=True)
    return serialized.data



