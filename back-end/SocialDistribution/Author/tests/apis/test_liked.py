from django.test import TestCase, Client
from django.core import serializers
from rest_framework import status
import json, base64
from Author.models import Like, Author, Post
from Author.author_serializer import LikeSerializer, AuthorSerializer
from Author.tests.dummy_model_fields import get_like_fields, get_post_fields, get_author_fields, get_test_credentials
# from Author.formatters import post_formater

invalid_uuid = '01234567-9ABC-DEF0-1234-56789ABCDEF0'

"""
Testing GET on /author/{author_ID}/posts/postID/likes
"""
class PostGetLikesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.headers = {
           'HTTP_AUTHORIZATION': 'Basic ' + 
                base64.b64encode(b'user0:123').decode("ascii")
       }

        # Create 3 authors that create 1 post each
        self.test_authors = []
        self.test_posts = []
        for i in range(3):
            self.test_authors.append(Author.objects.create(**get_test_credentials(i=i), 
                                                           **get_author_fields(i=i)))
            
            self.test_posts.append(Post.objects.create(**get_post_fields(i=i),
                                                       author_id=self.test_authors[i]))

        # Create test author to like all 3 posts
        self.test_liker = Author.objects.create(**get_test_credentials(5), 
                                                 **get_author_fields(5))

        self.test_liked_posts = []
        for i in range(3):
            self.test_liked_posts.append(Like.objects.create(**get_like_fields(id=self.test_posts[i].post_id),
                                                             author_id=self.test_authors[i],
                                                             liker_id=AuthorSerializer(self.test_liker).data))

    """ 
    Test successful GET on all existing likes /author/authorID/posts/postID/likes/ 
    """
    def test_get_post_likes_successful(self):
        response = self.client.get(
            f'/author/{self.test_liker.id}/liked/'
        )

        self.assertIsNotNone(response.json())
        self.assertEqual(3, len(response.json()["items"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ 
    Test unsuccessful GET on Author with no likes /author/authorID/posts/postID/likes/ 
    """
    def test_get_post_likes_unsuccessful(self):
        response = self.client.get(
            f'/author/{self.test_authors[0].id}/liked/'
        )

        self.assertIsNotNone(response.json())
        self.assertEqual(0, len(response.json()["items"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    """ 
    Test unsuccessful GET on non-existant Author /author/authorID/posts/postID/likes/ 
    """
    def test_get_invalid_author_post_likes_unsuccessful(self):
        response = self.client.get(
            f'/author/{invalid_uuid}/liked/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

