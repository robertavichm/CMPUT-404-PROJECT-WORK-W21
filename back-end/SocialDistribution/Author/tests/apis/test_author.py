from django.test import TestCase, Client
from rest_framework import status
import json, base64
from Author.models import Author
from Author.author_serializer import AuthorSerializer
from Author.tests.dummy_model_fields import get_author_fields, get_test_credentials
from Author.formatters import post_formater

invalid_uuid = '01234567-9ABC-DEF0-1234-56789ABCDEF0'

"""
Testing GET on /author/{author_ID}/
"""
class GetAuthorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.headers = {
           'HTTP_AUTHORIZATION': 'Basic ' + 
                base64.b64encode(b'user0:123').decode("ascii")
       }

        self.test_credentials = get_test_credentials()
        self.test_author_fields = get_author_fields()
        self.test_author = Author.objects.create(**self.test_author_fields, 
                                                 **self.test_credentials)
        self.test_author.set_password("123")
        self.test_author.save()

    """ Test successful author creation and GET'ing a Author by id """
    def test_get_author_successful(self):
        response = self.client.get(
            f'/author/{self.test_author.id}/'
        )
        author = Author.objects.get(id=self.test_author.id)
        serializer = AuthorSerializer(author)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
    
    """ Test unsuccessful GET on non-existing /author/authorID/"""
    def test_get_author_unsuccessful(self):
        response = self.client.get(
            f'/author/{invalid_uuid}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

"""
Testing POST (update) on /author/{author_ID}/
"""
class PostAuthorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.headers = {
           'HTTP_AUTHORIZATION': 'Basic ' + 
                base64.b64encode(b'user0:123').decode("ascii")
       }

        self.test_credentials = get_test_credentials()
        self.test_author_fields = get_author_fields()
        self.test_author = Author.objects.create(**self.test_author_fields, 
                                                 **self.test_credentials)
        self.test_author.set_password("123")
        self.test_author.save()

        self.payload = {
            'github': 'updatedname'
        }

    """ Test successful Post update and POST'ing on a Post by id """
    def test_delete_author_successful(self):
        response = self.client.post(
            f'/author/{self.test_author.id}/',
            data=json.dumps(self.payload),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that author object's github was updated to match the payload
        author = Author.objects.get(id=self.test_author.id)
        serializer = AuthorSerializer(author)
        self.assertEqual(serializer.data['github'], self.payload['github'])
    
    """ Test unsuccessful POST on non-existing /author/authorID/"""
    def test_delete_author_unsuccessful(self):
        response = self.client.post(
            f'/author/{invalid_uuid}/',
            data=self.payload,
            **self.headers    
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)