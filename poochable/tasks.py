from celery import task, Celery
from poochable.models import Dog, Person, Picture, SearchIndexPicture

celery = Celery('tasks')

# TODO: Posting a new picture is very slow with S3 on EC2 -- probably combination of data
#       transfer to application server and then from application server to S3, and 
#       also thumbnail generation (the thumbnail generation could easily be async using Celery) 
#       but it might also be possible to handle this whole function as a Celery.task 
#
# TODO: Think about whether it's worth making this all happen in a single transaction, which may 
#       lead to database connections being held longer but would obviously ensure transactional 
#       consistency and avoid orphaned records (particularly problematic for the indexes)
#
# Helper function to take user form input and persist
@celery.task
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
        
        
# Helper function to get the value of a form field that has been submitted by the end user
def extract_form_field_value(form, field_name):
    # Since the end user could input a blank string, let's handle no input the same
    value = form.cleaned_data.get(field_name, '')
    # But still, we don't want to put empty strings in the database, make them null    
    if value == '':
        value = None
        
    return value