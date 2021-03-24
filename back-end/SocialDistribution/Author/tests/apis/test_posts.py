from django.test import TestCase, Client
from rest_framework import status
import json
from Author.models import Author, Post
from Author.author_serializer import AuthorSerializer
from Author.tests.dummy_model_fields import get_author_fields, get_post_fields
from Author.formatters import post_formater

invalid_uuid = '01234567-9ABC-DEF0-1234-56789ABCDEF0'

"""
Testing GET on /author/{author_ID}/posts/{post_ID}/
"""
class PostGetTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_author_fields = get_author_fields()
        self.test_author = Author.objects.create(**self.test_author_fields)

        self.test_post_fields = get_post_fields()
        self.test_post = Post.objects.create(**self.test_post_fields, author_id=self.test_author)

    """ Test successful Post creation and GET'ing a Post by id """
    def test_get_post_successful(self):
        response = self.client.get(f'/author/{self.test_author.id}/posts/{self.test_post.post_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # TODO: Think about serializer change to avoid using post_formatter
        serializer = post_formater(Post.objects.get(post_id=self.test_post.post_id), True)
        self.assertEqual(response.json(), serializer)
    
    """ Test unsuccessful GET on non-existing /author/authorID/posts/{post_ID}/"""
    def test_get_post_unsuccessful(self):
        response = self.client.get(f'/author/{invalid_uuid}/posts/{invalid_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

"""
Testing update with POST on /author/{author_ID}/posts/{post_ID}/
"""
class PostUpdateTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_author_fields = get_author_fields()
        self.test_author = Author.objects.create(**self.test_author_fields)

        self.test_post_fields = get_post_fields()
        self.test_post = Post.objects.create(**self.test_post_fields, author_id=self.test_author)

        self.body = {
            "visibility": "FRIENDS",
            "unlisted": True
        }

    """ Test successful Post update and POST'ing on a Post by id """
    def test_post_update_successful(self):
        response = self.client.post(
            f'/author/{self.test_author.id}/posts/{self.test_post.post_id}/',
            data=json.dumps(self.body),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # TODO: Think about change in serializer rather than needing post_formatter?
        serializer = post_formater(Post.objects.get(post_id=self.test_post.post_id), True)
        
        for key in self.body:
            self.assertEqual(self.body[key], serializer[key])
    
    """ Test unsuccessful POST on non-existing /author/authorID/posts/{post_ID}/"""
    def test_post_update_unsuccessful(self):
        response = self.client.post(
            f'/author/{invalid_uuid}/posts/{invalid_uuid}/',
            data=json.dumps(self.body),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

"""
TODO - XXX
Testing Post Creation with PUT on /author/{author_ID}/posts/{post_ID}/
"""
class PostPutTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_author_fields = get_author_fields()
        self.test_author = Author.objects.create(**self.test_author_fields)

        self.test_post_fields = get_post_fields()
        self.test_post = Post.objects.create(**self.test_post_fields, author_id=self.test_author)

    """ Test successful Post update and POST'ing on a Post by id """
    def test_post_put_successful(self):
        pass
    
    """ Test unsuccessful POST on non-existing /author/authorID/posts/{post_ID}/"""
    def test_post_put_unsuccessful(self):
        pass

"""
Testing Post Deletion with DELETE on /author/{author_ID}/posts/{post_ID}/
"""
class PostDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_author_fields = get_author_fields()
        self.test_author = Author.objects.create(**self.test_author_fields)

        self.test_post_fields = get_post_fields()
        self.test_post = Post.objects.create(**self.test_post_fields, author_id=self.test_author)

    """ Test successful Post update and POST'ing on a Post by id """
    def test_post_delete_successful(self):
        response = self.client.delete(f'/author/{self.test_author.id}/posts/{self.test_post.post_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    """ Test unsuccessful POST on non-existing /author/authorID/posts/{post_ID}/"""
    def test_post_delete_unsuccessful(self):
        response = self.client.delete(f'/author/{invalid_uuid}/posts/{invalid_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)