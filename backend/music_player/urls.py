from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^api/', include('apps.api.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url("", include('django_socketio.urls')),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                                  document_root=settings.STATIC_ROOT)
