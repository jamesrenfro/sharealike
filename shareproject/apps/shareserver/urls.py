""" Configuration file to control which urls map to which view functions (or view classes) """
from django.conf.urls import patterns, url
from shareproject.apps.shareserver import views

urlpatterns = patterns('',
    # Top level index page for the application
    url(r'^$', views.index, name='index'),
    # Browse a collection of photos
#     url(r'^browse$', views.browse, name='browse'),
#     # Search for photos that match dog and/or owner names
#     url(r'^search$', views.search, name='search'),
#     # Detail page for a specific photo (shown in lightbox)
#     url(r'^share/(\d+)$', views.detail, name='detail'),
    # REST API resource 'pooch' maps to a class-based view (to handle GET, POST, DELETE, etc...)
    url(r'^api/share', views.ShareList.as_view()),
)
