"""
URLconf to control which urls map to which view functions (or view classes)
"""
from django.conf import settings
from django.conf.urls import patterns, url
from poochable import views

urlpatterns = patterns('',
    # Top level index page for the application
    url(r'^$', views.index, name='index'),
    # Browse a collection of photos
    url(r'^browse$', views.browse, name='browse'),
    # Search for photos that match dog and/or owner names
    url(r'^search$', views.search, name='search'),
    # Detail page for a specific photo (shown in lightbox)
    url(r'^pooch/(\d+)$', views.detail, name='detail'),
    # REST API resource 'pooch' maps to a class-based view (to handle GET, POST, DELETE, etc...)
    url(r'^api/pooch$', views.PoochList.as_view()),
    
    # Django can serve media files in the development environment, but this will not be used 
    # when deployed to the server, since Apache (or AWS CloudFront) will take care of distributing
    # media files
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
