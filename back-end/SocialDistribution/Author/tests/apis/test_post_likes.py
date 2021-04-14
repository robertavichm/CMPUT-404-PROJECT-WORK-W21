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

        # Create test author to like post
        self.test_liker = Author.objects.create(**get_test_credentials(1), 
                                                 **get_author_fields(1))
        # self.test_liker.set_password("123")
        # self.test_liker.save()

        self.test_like = Like.objects.create(**get_like_fields(id=self.test_post.post_id),
                                              author_id=self.test_author,
                                              liker_id=AuthorSerializer(self.test_liker).data)

        # print(f"NANANA = {serializers.serialize('json', [self.test_like])}")
        # print(f"NANANA = {self.test_like}")
            
        # for i in range(3):
        #     Like.objects.create(**get_like_fields(id=self.test_post.id),
        #                         author_id=self.test_author,
        #                         liker_id=serializers.serialize('json', [self.test_liker]))
        
        # print(f"NANANA = {self.test_post.post_id}")
        # print(f"NANANA = {self.test_author.id}")

    """ 
    Test successful GET on all existing likes /author/authorID/posts/postID/likes/ 
    """
    def test_get_post_likes(self):
        response = self.client.get(
            f'/author/{self.test_author.id}/posts/{self.test_post.post_id}/likes/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

