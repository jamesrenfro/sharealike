from django.conf.urls import patterns, include, url
from django.contrib import admin
from poochable import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'poochable.views.home', name='home'),
    # url(r'^poochable/', include('poochable.foo.urls')),
    url(r'^$', views.pooch_list, name='pooch-list'),
    url(r'^pooch$', views.pooch_detail, name='pooch-detail'),
    #url(r'^/pooch/')
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
