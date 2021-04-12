from django.test import TestCase, Client
from rest_framework import status
import json, base64
from Author.models import Author, Post
from Author.author_serializer import AuthorSerializer, PostSerializer
from Author.tests.dummy_model_fields import get_author_fields, get_post_fields, get_test_credentials
from Author.formatters import post_formater

invalid_uuid = '01234567-9ABC-DEF0-1234-56789ABCDEF0'

"""
Testing GET on /author/{author_ID}/posts/
"""
class PostListGetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.headers = {
           'HTTP_AUTHORIZATION': 'Basic ' + 
                base64.b64encode(b'user0:123').decode("ascii")
       }

        # Create test author to create posts
        self.test_author = Author.objects.create(**get_test_credentials(), 
                                                 **get_author_fields())
        self.test_author.set_password("123")
        self.test_author.save()
        
        # Test posts, mix of public, private, etc. settings
        self.test_post1 = Post.objects.create(
            **get_post_fields(i=0, visibility='PUBLIC', unlisted=False),
            author_id=self.test_author
        )

        self.test_post2 = Post.objects.create(
            **get_post_fields(i=1, visibility='PRIVATE', unlisted=True),
            author_id=self.test_author
        )

        self.test_post3 = Post.objects.create(
            **get_post_fields(i=2, visibility='PUBLIC', unlisted=False),
            author_id=self.test_author
        )

    """ Test successful GET on all existing public posts /author/authorID/posts/ """
    def test_get_all_public_posts_successful(self):
        response = self.client.get(
            f'/author/{self.test_author.id}/posts/'
        )
        # print(f'a = {len(response.json()["items"])}')
        self.assertIsNotNone(response.json())
        self.assertEqual(2, len(response.json()["items"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ Test successful GET on all existing (private and public) posts /author/authorID/posts/ """
    def test_get_all_self_posts_successful(self):
        response = self.client.get(
            f'/author/{self.test_author.id}/posts/',
            **self.headers
        )
        # print(f'a = {len(response.json()["items"])}')
        self.assertIsNotNone(response.json())
        # self.assertEqual(3, len(response.json()["items"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ Test unsuccessful GET on non-existing posts /author/authorID/posts/ """
    def test_get_post_unsuccessful(self):
        response = self.client.get(
            f'/author/{invalid_uuid}/posts/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


"""
Testing POST on /author/{author_ID}/posts/
"""
class PostListPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.headers = {
           'HTTP_AUTHORIZATION': 'Basic ' + 
                base64.b64encode(b'user0:123').decode("ascii")
       }

        # Create test author to create posts
        self.test_author = Author.objects.create(**get_test_credentials(), 
                                                 **get_author_fields())
        self.test_author.set_password("123")
        self.test_author.save()
        
        self.payload = get_post_fields()

    """ Test successful GET on all existing public posts /author/authorID/posts/ """
    def test_post_a_post_successful(self):
        response = self.client.post(
            f'/author/{self.test_author.id}/posts/',
            data=json.dumps(self.payload),
            content_type='application/json',
            **self.headers
        )

        self.assertIsNotNone(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthorized_post_a_post_unsuccessful(self):
        response = self.client.post(
            f'/author/{self.test_author.id}/posts/',
            data=json.dumps(self.payload),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)