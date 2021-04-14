from django.test import TestCase, Client
from django.core import serializers
from rest_framework import status
import json, base64
from Author.models import Author, Post, Comment
from Author.author_serializer import CommentSerializer, AuthorSerializer
from Author.tests.dummy_model_fields import get_post_fields, get_author_fields, get_test_credentials, get_comment_fields, post_comment_fields

invalid_uuid = '01234567-9ABC-DEF0-1234-56789ABCDEF0'

"""
Testing GET on /author/{author_ID}/posts/postID/Comments
"""
class PostGetCommentsTest(TestCase):
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

        # Create a test post 
        self.test_post = Post.objects.create(
            **get_post_fields(),
            author_id=self.test_author
        )

        self.test_commenters = []
        for i in range(5):
            # Create test commentor to comment on posts
            self.test_commenters.append(
                Author.objects.create(**get_test_credentials(i+1), 
                                      **get_author_fields(i+1))
            )
            self.test_author.set_password("123")
            self.test_author.save()

        for i in range(5):
            Comment.objects.create(
                **get_comment_fields(),
                post_id=self.test_post,
                author_id=AuthorSerializer(self.test_author).data
            )

    """ 
    Test successful GET on all existing comments /author/authorID/posts/postID/comments/ 
    """
    def test_get_post_comments_successful(self):
        response = self.client.get(
            f'/author/{self.test_author.id}/posts/{self.test_post.post_id}/comments/'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json())
        self.assertEqual(5, len(response.json()["items"]))

    """ 
    Test unsuccessful GET on all non-existant post /author/authorID/posts/postID/comments/ 
    """
    def test_get_post_comments_unsuccessful(self):
        response = self.client.get(
            f'/author/{self.test_author.id}/posts/{invalid_uuid}/comments/'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(response.json()["items"]))

"""
Testing POST on /author/{author_ID}/posts/postID/Comments
"""
class PostPOSTCommentsTest(TestCase):
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

        # Create a test post 
        self.test_post = Post.objects.create(
            **get_post_fields(),
            author_id=self.test_author
        )

        self.test_commenter = Author.objects.create(**get_test_credentials(20), 
                                                    **get_author_fields(20))
            
        self.test_author.set_password("123")
        self.test_author.save()

        self.payload = post_comment_fields(id=self.test_author)
        # self.payload = get_comment_fields()

    """ 
    Test successful POST comment on a post /author/authorID/posts/postID/comments/ 
    """
    def test_get_post_comments_successful(self):
        response = self.client.post(
            f'/author/{self.test_author.id}/posts/{self.test_post.post_id}/comments/',
            data=json.dumps(self.payload),
            content_type='application/json',
            **self.headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    """ 
    Test unsuccessful POST comment on a post /author/authorID/posts/postID/comments/ 
    """
    def test_get_post_comments_unsuccessful(self):
        response = self.client.post(
            f'/author/{self.test_author.id}/posts/{self.test_post.post_id}/comments/',
            data=json.dumps(self.payload),
            content_type='application/json',
        )
    
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
