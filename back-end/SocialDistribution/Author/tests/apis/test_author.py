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

