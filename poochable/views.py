"""
View functions for responding to http requests. These are using Django Rest Framework annotations
and Response classes to isolate requests on different method types
"""
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.response import SimpleTemplateResponse
from poochable.forms import UploadFileForm
from poochable.models import Dog, Person, Picture, SearchIndex, SearchIndexPicture
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# TODO: Implement paging at some later date and remove this
# Get the max search results from settings, or default it 
try:
    MAX_RESULTS = settings.POOCHABLE_MAX_RESULTS
except AttributeError:
    MAX_RESULTS = 100

# View function that returns the index page for the application
def index(request):
    context = RequestContext(request, {})
    return SimpleTemplateResponse(template='poochable/index.html', context=context)

# View function that returns the search page that shows all the thumbnails and dog names
def search(request):
    pictures = do_search(request)
    context = RequestContext(request, {'pictures': pictures})
    return SimpleTemplateResponse(template='poochable/search.fhtml', context=context)

# View function that returns the detail page for the lightbox
def detail(request, picture_id):
    picture = get_object_or_404(Picture, pk=picture_id)
    context = RequestContext(request, {'picture': picture})
    return SimpleTemplateResponse(template='poochable/detail.fhtml', context=context)

# API function to handle POST and return JSON/XML/etc... for AJAX from client    
@api_view(['POST'])
def api_pooch_create(request):
    try:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_new_post(form)
            return Response()
                 
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Helper function to perform search
def do_search(request):
    term = request.GET.get('term', '')
    
    pictures = list()
    if term != '':
        term = term.lower()
        # TODO: Determine if this is going to be sufficiently efficient for the expected table sizes, using a relational database.
        #       Might want to investigate using Haystack instead
        #
        # This query results in three separate database statements -- the first is a join between SearchIndexPicture and SearchIndex.
        # The other two are SELECT IN on primary keys for Picture and Dog 
        indices = SearchIndexPicture.objects.filter(search_index__term__contains=term).prefetch_related('picture').prefetch_related('picture__dog')[:MAX_RESULTS]
        for index in indices:
            pictures.append(index.picture)

    return pictures

# Helper function to get the value of a form field that has been submitted by the end user
def extract_form_field_value(form, field_name):
    # Since the end user could input a blank string, let's handle no input the same
    value = form.cleaned_data.get(field_name, '')
    # But still, we don't want to put empty strings in the database, make them null    
    if value == '':
        value = None
        
    return value

# TODO: Think about whether it's worth making this all happen in a single transaction, which may 
#       lead to database connections being held longer but would obviously ensure transactional 
#       consistency and avoid orphaned records (particularly problematic for the indexes)
#
# Helper function to take user form input and persist
def handle_new_post(form):
    # Since the end user could input a blank string, let's handle no input the same
    person_first_name = extract_form_field_value(form, 'person_first_name')
    person_middle_name = extract_form_field_value(form, 'person_middle_name')
    person_last_name = extract_form_field_value(form, 'person_last_name')
    dog_name = extract_form_field_value(form, 'dog_name')
    attachment = form.files.get('attachment', None)

    person = Person()
    person.first_name = person_first_name
    person.middle_name = person_middle_name
    person.last_name = person_last_name
    # TODO: add modified_by for the current logged in user if a user is logged in
    person.save()
    
    dog = Dog()
    dog.name = dog_name
    dog.owner = person
    # TODO: add modified_by for the current logged in user if a user is logged in
    dog.save()

    picture = Picture()
    picture.dog = dog
    picture.image = attachment
    # TODO: add modified_by for the current logged in user if a user is logged in
    picture.save()
    
    if dog.search_index is not None:
        dog_index_picture = SearchIndexPicture()
        dog_index_picture.picture = picture
        dog_index_picture.search_index = dog.search_index
        dog_index_picture.save()

    if person.search_index is not None:
        person_index_picture = SearchIndexPicture()
        person_index_picture.picture = picture
        person_index_picture.search_index = person.search_index
        person_index_picture.save()    



