# -*- coding: utf-8 -*-
__author__ = 'mateuszb'

import datetime
import urllib
from rest_framework import serializers

from django.contrib.auth import update_session_auth_hash, get_user_model
from apps.music.models import Track, Chart, TracktoChart, UsertoChart, Style
from apps.users.models import User, Vote
from apps.chat.models import Chat, Message


class TrackSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()
    votes_assad = serializers.SerializerMethodField()
    total_relative_votes = serializers.SerializerMethodField()
    added_username = serializers.SerializerMethodField()
    total_vote_list = serializers.SerializerMethodField()
    get_image = serializers.ReadOnlyField()

    def get_total_vote_list(self, obj):
        return obj.total_vote_list

    def get_added_username(self, obj):
        return obj.added_username

    def get_votes_assad(self, obj):
        return obj.votes_assad

    def get_total_relative_votes(self, obj):
        return obj.total_relative_votes

    def get_votes_count(self, obj):
        return obj.votes_count

    class Meta:
        model = Track
        exclude = ['image', 'total_vote_list', 'votes_assad', 'votes_count']


class VoteSerializer(serializers.ModelSerializer):
    chart_name = serializers.SerializerMethodField()
    track_name = serializers.SerializerMethodField()
    track_artist = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    get_avatar = serializers.SerializerMethodField()

    def get_chart_name(self, obj):
        return obj.chart_name

    def get_track_name(self, obj):
        return obj.track_name

    def get_track_artist(self, obj):
        return obj.track_artist

    def get_user_name(self, obj):
        return obj.user_name

    def get_get_avatar(self, obj):
        return obj.get_avatar

    class Meta:
        model = Vote
        fields = (
            'id', 'user', 'date_added', 'up_vote', 'chart_name', 'track_name', 'track_artist', 'user_name',
            'get_avatar')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    get_todays_vote = VoteSerializer(many=True, required=False)
    get_avatar = serializers.ReadOnlyField()

    class Meta:
        # model = get_user_model()
        model = User
        fields = ('id', 'email', 'username', 'password', 'confirm_password', 'get_avatar', 'get_todays_vote',)

        def create(self, validated_data):
            return User.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.save()

            password = validated_data.get('password', None, )
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style

class TracktoChartSerializer(serializers.ModelSerializer):
    total_relative_votes = serializers.SerializerMethodField()
    votes_assad = serializers.SerializerMethodField()
    title = serializers.ReadOnlyField(source='track.title')
    id = serializers.ReadOnlyField(source='track.id')
    added_username = serializers.ReadOnlyField(source='track.added_username')
    artist = serializers.ReadOnlyField(source='track.artist')
    category = serializers.ReadOnlyField(source='track.category')
    file = serializers.FileField(source='track.file', use_url=True, allow_null=True, required=False)
    link = serializers.ReadOnlyField(source='track.link')
    type = serializers.ReadOnlyField(source='track.type')
    year = serializers.ReadOnlyField(source='track.year')
    style = StyleSerializer(many=True, source='track.style')
    image = serializers.FileField(source='track.image', use_url=True, allow_null=True, required=False)

    def get_total_relative_votes(self, obj):
        return obj.total_votes

    def get_votes_assad(self, obj):
        return obj.todays_votes

    class Meta:
        model = TracktoChart
        fields = ('total_relative_votes', 'was_played_today', 'title', 'id', 'added_username', 'artist', 'category',
                  'file', 'link', 'type', 'votes_assad', 'image', 'year', 'style', 'users_votes')


class UsertoChartSerializer(serializers.ModelSerializer):
    get_vote = serializers.SerializerMethodField()
    get_todays_vote = serializers.SerializerMethodField()
    votes_left_chart = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source='user.username')
    id = serializers.ReadOnlyField(source='user.id')

    def get_get_vote(self, obj):
        return obj.total_votes_chart

    def get_get_todays_vote(self, obj):
        return obj.todays_votes_chart

    def get_votes_left_chart(self, obj):
        return obj.votes_left_chart

    class Meta:
        model = UsertoChart
        fields = ('get_vote', 'get_todays_vote', 'username', 'id', 'votes_left_chart')


class UserMiddleSerializer(serializers.ModelSerializer):
    get_vote = serializers.SerializerMethodField()
    get_todays_vote = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()

        fields = ('get_vote', 'get_todays_vote', 'username', 'id')

    def get_get_todays_vote(self, obj):
        return 0

    def get_get_vote(self, obj):
        return 0


class ChartSerializer(serializers.ModelSerializer):
    owned_by = UserSerializer(read_only=True)
    track_list = TracktoChartSerializer(source='tracktochart_set', many=True, read_only=True)
    invited_new = UsertoChartSerializer(source='usertochart_set', many=True, read_only=True)

    class Meta:
        model = Chart


class MessageSerializer(serializers.ModelSerializer):
    text_chat = serializers.CharField(required=True)
    date_chat = serializers.DateTimeField()
    name_room_chat = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_name_room_chat(self, obj):
        return obj.chat.name_room

    def get_username(self, obj):
        return obj.user.username

    def get_avatar(self, obj):
        return obj.user.get_avatar

    class Meta:
        model = Message
        fields = ('text_chat', 'date_chat', 'name_room_chat', 'username', 'avatar')


class ChatSerializer(serializers.ModelSerializer):
    name_room = serializers.CharField()

    class Meta:
        model = Chat
        fields = ('id', 'name_room')


class AllChartSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    def get_followers(self, obj):
        return obj.get_followers()

    class Meta:
        model = Chart
        fields = ('id', 'name', 'followers')


class SimpleChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ('id', 'name',)


class TrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', ]


class NewTracksSerializer(serializers.ModelSerializer):
    get_image = serializers.ReadOnlyField()

    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'link', 'get_image']

