from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client, MULTIPART_CONTENT
from poochable.forms import PictureForm
from poochable.models import Dog, Person, Picture

import mock
import os  

TEST_IMAGE_PATH = os.path.dirname(__file__) + '/static/lib/bootstrap/img/glyphicons-halflings.png'

class ModelTest(TestCase):
    
    def _create_dog(self):
        dog = Dog()
        dog.name = 'Rover'
        dog.owner = self._create_person()
        dog.save()
        return dog
        
    def _create_person(self):
        person = Person()
        person.first_name = 'John'
        person.middle_name = 'Q'
        person.last_name = 'Tester'
        person.save()
        return person

    def test_dog_owner_id_not_null(self):
        dog = Dog()
        dog.owner = Person()
        self.assertRaises(IntegrityError, dog.save)
        
    def test_dog_requires_name(self):
        dog = Dog()
        dog.name = None
        dog.owner = self._create_person()
        self.assertRaises(IntegrityError, dog.save)
    
    def test_dog_has_index(self):
        dog = self._create_dog()
        self.assertIsNotNone(dog.search_index)
        
    def test_person_has_index(self):
        person = self._create_person()
        self.assertIsNotNone(person.search_index)        
        
class FormTest(TestCase):
    # TODO add form tests
    pass        
            
class InterfaceLevelTest(TestCase):
    
    def _post_to_pooch(self, data, expected_status_code=200):
        client = Client()
        attachment = data.get('attachment', None)
        try:
            response = client.post('/api/pooch', data, content_type=MULTIPART_CONTENT)
            self.assertEqual(response.status_code, expected_status_code)
        finally:
            if attachment is not None:
                attachment.close()
                
    def _get_pictures(self, term):
        client = Client()
        response = client.get('/search', {'term':term})
        self.assertEqual(response.status_code, 200)
        context = response.context
        pictures = context['pictures']
        return pictures
            
    @mock.patch('storages.backends.s3boto.S3BotoStorage', FileSystemStorage)
    def test_post_picture_with_dog_name_success(self):
        # Important to point to a different media root otherwise we fill up our 
        # media root with test data
        with(self.settings(MEDIA_ROOT='/tmp')):
            attachment = open(TEST_IMAGE_PATH)
            data = {'dog_name': 'Fred', 'attachment': attachment}
            self._post_to_pooch(data)
            pictures = self._get_pictures('Fred')
            self.assertEqual(1, len(pictures), "Should be able to see the picture that was posted in search results")
            picture = pictures[0]
            self.assertEqual(None, picture.dog.owner.first_name)
            self.assertEqual(None, picture.dog.owner.middle_name)
            self.assertEqual(None, picture.dog.owner.last_name)
            self.assertEqual('Fred', picture.dog.name)
        
    @mock.patch('storages.backends.s3boto.S3BotoStorage', FileSystemStorage)
    def test_post_picture_with_person_first_name_success(self):
        with(self.settings(MEDIA_ROOT='/tmp')):
            attachment = open(TEST_IMAGE_PATH)
            data = {'dog_name': 'Jules', 'person_first_name': 'Georgina', 'attachment': attachment}
            self._post_to_pooch(data)
            pictures = self._get_pictures('Georgina')
            self.assertEqual(1, len(pictures), "Searching by person first name should bring back picture")
            pictures = self._get_pictures('Jules')
            self.assertEqual(1, len(pictures), "Searching by dog name should bring back picture")
            pictures = self._get_pictures('LE')
            self.assertEqual(1, len(pictures), "Searching by fragment of dog name should bring back picture")
            pictures = self._get_pictures('')
            self.assertEqual(0, len(pictures), "Searching by blank shouldn't bring back anything")
            pictures = self._get_pictures('XYZ')
            self.assertEqual(0, len(pictures), "Searching by non-matching shouldn't bring back anything")

    def test_post_picture_with_missing_dog_name_failure(self):
        with(self.settings(MEDIA_ROOT='/tmp')):
            attachment = open(TEST_IMAGE_PATH)
            data = {'attachment': attachment}
            self._post_to_pooch(data, expected_status_code=400)
            pictures = self._get_pictures('Fred')
            self.assertEqual(0, len(pictures), "Shouldn't be able to find any pictures")







