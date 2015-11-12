# -*- coding: utf-8 -*-

__author__ = 'blaze'

import datetime
import urllib2
import discogs_client

from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.db import models


class Style(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

class LimitReached(Exception):
    pass

class TrackManager(models.Manager):
    def create(self, **kwargs):
        limit = DefaultValues.objects.first().max_user_songs
        if self.filter(added_by=kwargs['added_by']).count() >= limit:
            raise LimitReached('You can\'t add more tracks! (%s already added)' % limit)
        track = self.model(**kwargs)
        self._for_write = True
        results = track.connect_to_api()
        track.set_type()
        track.set_meta_info(results)
        track.save(force_insert=True, using=self.db)
        try:
            track.set_styles(results)
            track.set_image(results)
        except IndexError:
            pass
        return track


class Track(models.Model):
    title = models.CharField(max_length=254)
    artist = models.CharField(max_length=50)
    category = models.CharField(max_length=50, blank=True)
    added_by = models.ForeignKey('users.User', related_name='tracks')
    file = models.FileField(upload_to='static/tracks', blank=True)
    link = models.CharField(max_length=254, blank=True, unique=True)
    type = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='static/images/artists/', blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    style = models.ManyToManyField(Style, blank=True)
    objects = TrackManager()

    class Meta:
        unique_together = ('title', 'artist',)

    def connect_to_api(self):
        d = discogs_client.Client('MusicApp', user_token='lYZxOrAPASUOlpDrZMPaMdnWZczHZVoAoECIBjTM')
        results = d.search(artist=self.artist, track=self.title, type='master', format='album')
        return results

    def set_type(self):
        if self.file:
            self.type = 'file'
        if 'youtube' in self.link:
            self.type = 'youtube'
        elif 'soundcloud' in self.link:
            self.type = 'soundcloud'

    def set_meta_info(self, results):
        if results:
            try:
                self.category = results[0].data['genre'][0]
                self.year = results[0].data['year']
            except KeyError:
                pass

    def set_styles(self, results):
        if results:
            styles = results[0].data['style']
            for style in styles:
                if not Style.objects.filter(name=style).exists():
                    s = Style.objects.create(name=style)
                else:
                    s = Style.objects.get(name=style)
                self.style.add(s)

    def set_image(self, results):
        if not self.image:
            print 'on set image', results[0]
            artist_name = self.artist.replace(' ', '_')
            filename = artist_name.encode('utf-8') + '.jpg'
            if len(results) == 0:
                # set default image later
                pass
            elif results[0].data['thumb'] != '':
                img_url = str(results[0].data['thumb'])
                image = ContentFile(urllib2.urlopen(img_url).read())
                self.image.save(filename, image)

    @property
    def total_vote_list(self):
        vote_list = Vote.objects.filter(track_id=self)
        my_dict = {}
        for vote in vote_list:
            if vote.user.username in my_dict:
                my_dict[vote.user.username] += 1
            else:
                my_dict[vote.user.username] = 1
        return my_dict

    @property
    def added_username(self):
        return self.added_by.username

    @property
    def votes_count(self):
        return self.votes.count()

    @property
    def votes_assad(self):
        votes = self.votes.all()
        if DefaultValues.objects.first().votes_expire_daily:
            votes = votes.filter(date_added=datetime.date.today())
        return votes.filter(up_vote=True).count() - votes.filter(up_vote=False).count()

    @property
    def total_relative_votes(self):
        votes = self.votes.filter()
        return votes.filter(up_vote=True).count() - votes.filter(up_vote=False).count()

    @property
    def total_relative_votes_today(self):
        votes = self.votes.all()
        if DefaultValues.objects.first().votes_expire_daily:
            votes = votes.filter(date_added=datetime.date.today())
        return votes.filter(up_vote=True).count() - votes.filter(up_vote=False).count()

    @property
    def votes_user_today(self, user):
        votes = self.votes.filter(user=user)
        if DefaultValues.objects.first().votes_expire_daily:
            votes = votes.filter(date_added=datetime.date.today())
        return votes.filter(up_vote=True).count() - votes.filter(up_vote=False).count()

    @property
    def get_image(self):
        if bool(self.image):
            return self.image.url
        else:
            return DefaultValues.objects.get(id=1).song_image.url

    def __unicode__(self):
        return self.title


class Chart(models.Model):
    name = models.CharField(max_length=200, unique=True)
    owned_by = models.ForeignKey('users.User', related_name='user')
    invited_new = models.ManyToManyField('users.User', related_name='user_invited', blank=True, through='UsertoChart')
    track_list = models.ManyToManyField(Track, blank=True, through='TracktoChart', related_name='newTracklist')
    votes_per_day = models.IntegerField(default=25)
    tracks_to_play = models.IntegerField(default=200)

    def __unicode__(self):
        return self.name

    def get_followers(self, instances=False):
        if instances:
            return self.invited_new.all()
        return list(self.invited_new.values_list('id', flat=True))

    @property
    def votes_average(self):
        tracks = self.track_list.all()
        total_votes = 0
        for track in tracks:
            t2c = track.tracktochart_set.get(chart=self)
            total_votes += t2c.total_votes
        if tracks.count() != 0:
            return total_votes / tracks.count()
        else:
            return 0


class Vote(models.Model):
    user = models.ForeignKey('users.User', related_name='vote_user')
    track_id = models.ForeignKey(Track, related_name='votes')
    chart = models.ForeignKey(Chart, related_name='chart', default=1)
    date_added = models.DateField(auto_now=True)
    up_vote = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
            update_fields=None):
        super(Vote, self).save(force_insert, force_update, using, update_fields)
        t2c = TracktoChart.objects.get(track=self.track_id, chart=self.chart)
        t2c.votes.add(self)
        t2c.save()

    def __unicode__(self):
        return self.track_id.title

    @property
    def chart_name(self):
        return self.chart.name  # .encode('utf-8')

    @property
    def track_name(self):
        return self.track_id.title  # .encode('utf-8')

    @property
    def track_artist(self):
        return self.track_id.artist  # .encode('utf-8')

    @property
    def user_name(self):
        return self.user.username.encode('utf-8')

    @property
    def get_avatar(self):
        return str(self.user.get_avatar)


class TracktoChart(models.Model):
    track = models.ForeignKey(Track)
    chart = models.ForeignKey(Chart)
    votes = models.ManyToManyField(Vote, blank=True)
    was_played_today = models.BooleanField(default=False)

    class Meta:
        unique_together = ('track', 'chart',)

    @property
    def total_votes(self):
        votes = self.votes.filter(up_vote=True).count() - self.votes.filter(up_vote=False).count()
        return votes

    @property
    def today_votes_all(self):
        return self.votes.filter(date_added=datetime.date.today())

    @property
    def todays_votes(self):
        votes = self.votes.filter(date_added=datetime.date.today(), up_vote=True).count() - self.votes.filter(
            date_added=datetime.date.today(), up_vote=False).count()
        return votes

    # returns number of positive and negative votes (if there were any) added by followers on this track
    @property
    def users_votes(self):
        users = UsertoChart.objects.filter(chart=self.chart)
        track_votes_list = []
        for user in users:
            votes_up = Vote.objects.filter(user=user.user, chart=self.chart, track_id=self.track, up_vote=True).count()
            votes_down = Vote.objects.filter(user=user.user, chart=self.chart, track_id=self.track,
                up_vote=False).count()
            if votes_up or votes_down:
                track_votes_dict = {}
                track_votes_dict['user'] = user.user.username
                track_votes_dict['up'] = votes_up
                track_votes_dict['down'] = votes_down
                track_votes_list.append(track_votes_dict)
        return track_votes_list

    def __unicode__(self):
        return self.track.title + ' on ' + self.chart.name


class UsertoChart(models.Model):
    user = models.ForeignKey('users.User')
    chart = models.ForeignKey(Chart)

    class Meta:
        unique_together = ('user', 'chart',)

    @property
    def total_votes_chart(self):
        votes = Vote.objects.filter(user=self.user, chart=self.chart, up_vote=True).count() - Vote.objects.filter(
            user=self.user, chart=self.chart, up_vote=False).count()
        return votes

    @property
    def todays_votes_chart(self):

        up_votes = Vote.objects.filter(user=self.user, chart=self.chart, up_vote=True)
        down_votes = Vote.objects.filter(user=self.user, chart=self.chart, up_vote=False)
        if DefaultValues.objects.first().votes_expire_daily:
            up_votes = up_votes.filter(date_added=datetime.date.today())
            down_votes = down_votes.filter(date_added=datetime.date.today())
        votes_balance = up_votes.count() - down_votes.count()
        return votes_balance

    @property
    def votes_left_chart(self):
        votes = Vote.objects.filter(user=self.user, chart=self.chart)
        if DefaultValues.objects.first().votes_expire_daily:
            votes = votes.filter(date_added=datetime.date.today())

        votes_left = self.chart.votes_per_day - votes.count()
        if votes_left > 0:
            return votes_left
        else:
            return 0

    def __unicode__(self):
        return self.user.username + ' on ' + self.chart.name


def validate_only_one_instance(obj):
    """Makes sure that no more than one instance of a given model is created."""
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class DefaultValues(models.Model):
    def clean(self):
        validate_only_one_instance(self)

    user_image = models.ImageField(upload_to='static/images/defaults/', blank=True)
    song_image = models.ImageField(upload_to='static/images/defaults/', blank=True)
    max_user_songs = models.IntegerField(default=10)
    balance_playlist = models.BooleanField(default=False)
    votes_expire_daily = models.BooleanField(default=False)
