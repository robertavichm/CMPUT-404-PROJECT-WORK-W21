from django.test import TestCase, Client
from rest_framework import status
import json
from Author.models import Author
from Author.author_serializer import AuthorSerializer
from Author.tests.dummy_model_fields import get_author_fields

"""
Testing Creation of an Author 
"""
class AuthorCreationTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_author_fields = get_author_fields()
        self.test_author = Author.objects.create(**self.test_author_fields)

    """ Test successful author creation and GET'ing an author """
    def test_get_author_successful(self):
        response = self.client.get(f'/author/{self.test_author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = AuthorSerializer(Author.objects.get(id=self.test_author.id))
        self.assertEqual(response.json(), serializer.data)
    
    """ Test unsuccessful GET on non-existing /author/authorID/ """
    def test_get_author_unsuccessful(self):
        response = self.client.get('/author/01234567-9ABC-DEF0-1234-56789ABCDEF0/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

""" 
Testing Author Updates
"""
class AuthorUpdateTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_author_fields = get_author_fields()
        self.test_author = Author.objects.create(**self.test_author_fields)

        self.body = {'displayName': 'Clive Bixby'}
    
    """ Test successful POST'ing on an author """
    def test_post_author_successful(self):
        response = self.client.post(
            f'/author/{self.test_author.id}/', 
            data=json.dumps(self.body), 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify displayName has been changed to our payload body 
        serializer = AuthorSerializer(Author.objects.get(id=self.test_author.id))
        self.assertEqual(self.body['displayName'], serializer.data['displayName'])

    """ Test unsuccessful POST'ing on an non-existing author """
    def test_post_author_unsuccessful(self):
        response = self.client.post(
            '/author/01234567-9ABC-DEF0-1234-56789ABCDEF0/',
            data=json.dumps(self.body),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
