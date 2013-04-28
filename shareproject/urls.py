""" Top level configuration file to forward url configuration to applications """
from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'', include('shareserver.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # Django can serve media files in the development environment, but this will not be used 
    # when deployed to the server, since Apache (or AWS CloudFront) will take care of distributing
    # media files
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
