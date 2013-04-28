from celery import task, Celery
from shareproject.apps.shareserver.models import Share, Person, Picture, SearchIndexPicture

celery = Celery('tasks')

# TODO: Posting a new picture is still very slow with S3 on EC2 -- probably data
#       transfer to application server, but also the data does not seem to be streaming
#       directly to S3 yet. 
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
    share_title = extract_form_field_value(form, 'share_title')
    share_content = extract_form_field_value(form, 'share_content')
    share_attachment = form.files.get('share_attachment', None)

    person = Person()
    person.first_name = person_first_name
    person.middle_name = person_middle_name
    person.last_name = person_last_name
    # TODO: add modified_by for the current logged in user if a user is logged in
    person.save()
    
    share = Share()
    share.title = share_title
    share.content = share_content
    share.owner = person
    # TODO: add modified_by for the current logged in user if a user is logged in
    share.save()

    picture = Picture()
    picture.share = share
    picture.image = share_attachment
    picture.thumbnail = share_attachment
    # TODO: add modified_by for the current logged in user if a user is logged in
    picture.save()
    
    if share.search_index is not None:
        share_index_picture = SearchIndexPicture()
        share_index_picture.picture = picture
        share_index_picture.search_index = share.search_index
        share_index_picture.save()

    if person.search_index is not None:
        person_index_picture = SearchIndexPicture()
        person_index_picture.picture = picture
        person_index_picture.search_index = person.search_index
        person_index_picture.save() 
        
        
# Helper function to get the value of a form field that has been submitted by the end user
def extract_form_field_value(form, field_name):
    # Since the end user could input a blank string, let's handle no input the same
    value = form.cleaned_data.get(field_name, '')
        
    return value