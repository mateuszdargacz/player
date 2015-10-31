# -*- coding: utf-8 -*- 

from rest_framework_nested import routers

from django.conf.urls import patterns, url, include

from apps.api.views.users import LoginView, LogoutView, UserViewSet
from apps.api.views.tracks import TrackView
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
accounts_router = routers.NestedSimpleRouter(
    router, r'users', lookup='user'
)


urlpatterns = patterns('',
                       url(r'^v1/', include(router.urls)),
                       url(r'^v1/', include(accounts_router.urls)),
                       url(r'^v1/auth/login/$', LoginView.as_view(), name='login'),
                       url(r'^v1/auth/logout/$', LogoutView.as_view(), name='logout'),
                       url(r'^v1/music/add/$', TrackView.as_view(), name='addtrack'),
                       )
