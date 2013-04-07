from django.test import TestCase
from django.test.client import Client, MULTIPART_CONTENT
import os  

TEST_IMAGE_PATH = os.path.dirname(__file__) + '/static/lib/bootstrap/img/glyphicons-halflings.png'

class PoochDetailTestCase(TestCase):
    
    def post_to_pooch(self, data, expected_status_code=200):
        client = Client()
        attachment = data.get('attachment', None)
        try:
            response = client.post('/api/pooch', data, content_type=MULTIPART_CONTENT)
            self.assertEqual(response.status_code, expected_status_code)
        finally:
            if attachment is not None:
                attachment.close()
                
    def get_pictures(self, term):
        client = Client()
        response = client.get('/search', {'term':term})
        self.assertEqual(response.status_code, 200)
        context = response.context
        pictures = context['pictures']
        return pictures
            
    def test_post_picture_with_dog_name_success(self):
        attachment = open(TEST_IMAGE_PATH)
        data = {'dog_name': 'Fred', 'attachment': attachment}
        self.post_to_pooch(data)
        pictures = self.get_pictures('Fred')
        self.assertEqual(1, len(pictures), "Should be able to see the picture that was posted in search results")
        picture = pictures[0]
        self.assertEqual(None, picture.dog.owner.first_name)
        self.assertEqual(None, picture.dog.owner.middle_name)
        self.assertEqual(None, picture.dog.owner.last_name)
        self.assertEqual('Fred', picture.dog.name)
        
    def test_post_picture_with_person_first_name_success(self):
        attachment = open(TEST_IMAGE_PATH)
        data = {'dog_name': 'Jules', 'person_first_name': 'Georgina', 'attachment': attachment}
        self.post_to_pooch(data)
        pictures = self.get_pictures('Georgina')
        self.assertEqual(1, len(pictures), "Searching by person first name should bring back picture")
        pictures = self.get_pictures('Jules')
        self.assertEqual(1, len(pictures), "Searching by dog name should bring back picture")
        pictures = self.get_pictures('LE')
        self.assertEqual(1, len(pictures), "Searching by fragment of dog name should bring back picture")
        pictures = self.get_pictures('')
        self.assertEqual(0, len(pictures), "Searching by blank shouldn't bring back anything")
        pictures = self.get_pictures('XYZ')
        self.assertEqual(0, len(pictures), "Searching by non-matching shouldn't bring back anything")

    def test_post_picture_with_missing_dog_name_failure(self):
        attachment = open(TEST_IMAGE_PATH)
        data = {'attachment': attachment}
        self.post_to_pooch(data, expected_status_code=400)
        pictures = self.get_pictures('Fred')
        self.assertEqual(0, len(pictures), "Shouldn't be able to find any pictures")




