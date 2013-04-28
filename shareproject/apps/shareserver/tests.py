from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client, MULTIPART_CONTENT
from shareproject.apps.shareserver.models import Share, Person
from shareproject.apps.shareserver.serializers import PictureSerializer
from os.path import join

import mock

TEST_IMAGE_PATH = join(settings.DJANGO_ROOT, 'assets/lib/bootstrap/img/glyphicons-halflings.png')

class ModelTest(TestCase):
    
    def _create_share(self):
        share = Share()
        share.title = 'A post about me!'
        share.owner = self._create_person()
        share.save()
        return share
        
    def _create_person(self):
        person = Person()
        person.first_name = 'John'
        person.middle_name = 'Q'
        person.last_name = 'Tester'
        person.save()
        return person

    def test_share_owner_id_not_null(self):
        share = Share()
        share.owner = Person()
        self.assertRaises(IntegrityError, share.save)
        
    def test_share_requires_name(self):
        share = Share()
        share.title = None
        share.owner = self._create_person()
        self.assertRaises(IntegrityError, share.save)
    
    def test_share_has_index(self):
        share = self._create_share()
        self.assertIsNotNone(share.search_index)
        
    def test_person_has_index(self):
        person = self._create_person()
        self.assertIsNotNone(person.search_index)        
        
class FormTest(TestCase):
    # TODO add form tests
    pass        
            
class InterfaceLevelTest(TestCase):
    
    def _post_share(self, data, expected_status_code=200):
        client = Client()
        share_attachment = data.get('share_attachment', None)
        try:
            response = client.post('/api/share', data, content_type=MULTIPART_CONTENT)
            self.assertEqual(response.status_code, expected_status_code)
        finally:
            if share_attachment is not None:
                share_attachment.close()
                
    def _get_pictures(self, term):
        client = Client()
        response = client.get('/api/share', {'term':term})
        self.assertEqual(response.status_code, 200)
        serializer = PictureSerializer(data=response.data, many=True)
        if not serializer.is_valid():
            errors = serializer.errors
        
        return serializer.object
            
    @mock.patch('storages.backends.s3boto.S3BotoStorage', FileSystemStorage)
    def test_post_picture_with_share_title_success(self):
        # Important to point to a different media root otherwise we fill up our 
        # media root with test data
        with(self.settings(MEDIA_ROOT='/tmp')):
            attachment = open(TEST_IMAGE_PATH)
            data = {'share_title': 'A post from me!', 'share_attachment': attachment}
            self._post_share(data)
            pictures = self._get_pictures('post')
            self.assertEqual(1, len(pictures), "Should be able to see the picture that was posted in search results")
        
    @mock.patch('storages.backends.s3boto.S3BotoStorage', FileSystemStorage)
    def test_post_picture_with_person_first_name_success(self):
        with(self.settings(MEDIA_ROOT='/tmp')):
            try:
                attachment = open(TEST_IMAGE_PATH)
                data = {'share_title': 'Something', 'person_first_name': 'Georgina', 'share_attachment': attachment}
                self._post_share(data)
                pictures = self._get_pictures('Georgina')
                self.assertEqual(1, len(pictures), "Searching by person first name should bring back picture")
                pictures = self._get_pictures('Something')
                self.assertEqual(1, len(pictures), "Searching by title should bring back picture")
                pictures = self._get_pictures('thin')
                self.assertEqual(1, len(pictures), "Searching by fragment of title should bring back picture")
                pictures = self._get_pictures('')
                self.assertEqual(0, len(pictures), "Searching by blank shouldn't bring back anything")
                pictures = self._get_pictures('XYZ')
                self.assertEqual(0, len(pictures), "Searching by non-matching shouldn't bring back anything")
            finally:
                if attachment is not None:
                    attachment.close()

    def test_post_picture_with_missing_share_title_failure(self):
        with(self.settings(MEDIA_ROOT='/tmp')):
            try:
                attachment = open(TEST_IMAGE_PATH)
                data = {'share_attachment': attachment}
                self._post_share(data, expected_status_code=400)
                pictures = self._get_pictures('post')
                self.assertEqual(0, len(pictures), "Shouldn't be able to find any pictures")
            finally:
                if attachment is not None:
                    attachment.close()


    def test_post_pictures_tagged_twice_same_term(self):
        try:
            attachment = open(TEST_IMAGE_PATH)
            data = {'share_title': 'Jules', 'person_first_name': 'Juliana', 'share_attachment': attachment}
            self._post_share(data)
            pictures = self._get_pictures('Jul')
            self.assertEqual(1, len(pictures), "Should only get 1 picture back, found %d" % len(pictures))
        finally:
            if attachment is not None:
                attachment.close()



