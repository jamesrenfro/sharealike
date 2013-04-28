"""
View functions for responding to http requests. These are using Django Rest Framework annotations
and Response classes to isolate requests on different method types
"""
from celery import task
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.response import SimpleTemplateResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from shareproject.apps.shareserver.forms import PictureForm
from shareproject.apps.shareserver.models import Share, Person, Picture, SearchIndexPicture
from shareproject.apps.shareserver.serializers import PictureSerializer
from shareproject.apps.shareserver.tasks import handle_new_post

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# TODO: Implement paging at some later date and remove this
# Get the max search results from settings, or default it 
try:
    MAX_RESULTS = settings.POOCHABLE_MAX_RESULTS
except AttributeError:
    MAX_RESULTS = 100

# Check to see if we should be using Celery for task queuing
try:
    USE_CELERY = settings.USE_CELERY
except AttributeError:
    USE_CELERY = False

# View function that returns the index page for the application
def index(request):
    pictures = Picture.objects.filter(width__gte=1000).order_by('-score').order_by('-last_modified')[:1]
    context = RequestContext(request, {'pictures': pictures})
    return SimpleTemplateResponse(template='shareserver/index.html', context=context)

# API view class (see http://django-rest-framework.org/api-guide/views.html) 
class ShareList(APIView):

    def get(self, request):
        pictures = do_search(request)
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            form = PictureForm(request.POST, request.FILES)
            if form.is_valid():
                if USE_CELERY:
                    handle_new_post.apply_async(args=[form])
                else: 
                    handle_new_post(form)
                    
                return Response()
            
            logger.debug('Bad request error %s' % form.errors)  
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            logger.exception('Internal server error!')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
# Helper function to perform search
def do_search(request):
    term = request.GET.get('term', None)
    
    pictures = list()
    if term is None:
        pictures = Picture.objects.all().order_by('-score').order_by('-last_modified')[:100]
    elif term != '':
        term = term.lower()
        # TODO: Determine if this is going to be sufficiently efficient for the expected table sizes, using a relational database.
        #       Might want to investigate using Haystack instead
        #
        # This query results in three separate database statements -- the first is a join between SearchIndexPicture and SearchIndex.
        # The other two are SELECT IN on primary keys for Picture and Dog 
        indices = SearchIndexPicture.objects.filter(search_index__term__contains=term).prefetch_related('picture').prefetch_related('picture__share')[:MAX_RESULTS]
        picture_ids = set()
        for index in indices:
            picture = index.picture
            picture_id = picture.pk
            if picture_id not in picture_ids:
                pictures.append(index.picture)
                picture_ids.add(picture_id)

    return pictures



   



