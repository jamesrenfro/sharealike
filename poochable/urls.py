from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from poochable import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'poochable.views.home', name='home'),
    # url(r'^poochable/', include('poochable.foo.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search, name='pooch-list'),
    url(r'^pooch/(\d+)$', views.detail, name='pooch-detail'),
    url(r'^api/pooch$', views.api_pooch_create, name='pooch-create'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
