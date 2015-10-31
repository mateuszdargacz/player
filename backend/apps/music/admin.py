# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.music.models import Track, Vote, Chart, TracktoChart, UsertoChart, DefaultValues, Style
from apps.users.models import User


class TrackInline(admin.TabularInline):
    model = Track


class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'added_by']

    def save_model(self, request, obj, form, change):
        del form.cleaned_data['category']
        del form.cleaned_data['style']
        del form.cleaned_data['image']
        del form.cleaned_data['type']
        del form.cleaned_data['year']
        if not obj.pk:
            Track.objects.create(**form.cleaned_data)
        else:
            obj.save()


class VoteAdmin(admin.ModelAdmin):
    list_display = ['track_id', 'date_added', 'user']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    inlines = [TrackInline]


class TrackMiddleModel(admin.TabularInline):
    model = TracktoChart


class ChartInline(admin.TabularInline):
    model = UsertoChart


class ChartAdmin(admin.ModelAdmin):
    inlines = (ChartInline, TrackMiddleModel,)
    list_display = ['id', 'name', 'owned_by']


class TracktoChartAdmin(admin.ModelAdmin):
    model = TracktoChart


class UsertoChartAdmin(admin.ModelAdmin):
    model = UsertoChart


admin.site.register(Track, TrackAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Chart, ChartAdmin)
admin.site.register(TracktoChart, TracktoChartAdmin)
admin.site.register(UsertoChart, UsertoChartAdmin)
admin.site.register(DefaultValues)
admin.site.register(Style)
