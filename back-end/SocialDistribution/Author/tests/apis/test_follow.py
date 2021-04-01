from django.test import TestCase, Client
from rest_framework import status
import json, base64

from Author.models import Author, FriendShip
from Author.author_serializer import AuthorSerializer, FriendshipSerializer
from Author.tests.dummy_model_fields import get_author_fields, get_follow_fields, get_test_credentials

from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth.models import User

invalid_uuid = '01234567-9ABC-DEF0-1234-56789ABCDEF0'

"""
Testing GET on a follow request on /author/{authorID}/followers/{followID}
"""
class FollowGetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.headers = {
           'HTTP_AUTHORIZATION': 'Basic ' + 
                base64.b64encode(b'user1:123').decode("ascii")
        }

        # Create an author that will send a request
        self.test_sender = Author.objects.create(**get_test_credentials(),
                                                 **get_author_fields())
        self.test_sender.set_password("123")
        self.test_sender.save()

        # Create an author that will receive a request
        self.test_receiver = Author.objects.create(**get_test_credentials(1),
                                                   **get_author_fields(1))
        self.test_receiver.set_password("123")
        self.test_receiver.save()

        self.follow = FriendShip.objects.create(author_local=self.test_receiver, author_remote=AuthorSerializer(self.test_sender).data)
        self.follow_serialized = FriendshipSerializer(self.follow)

    def test_get_follow_successful(self):
        response = self.client.get(
            f'/author/{self.test_receiver.id}/followers/{self.test_sender.id}/',
            **self.headers
        )
        # Test request exists
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test request data matches 
        for key in self.follow_serialized.data.keys():
            self.assertEqual(response.json()["accepted"], self.follow_serialized.data["accepted"])

    def test_get_follow_unsuccessful(self):
        response = self.client.get(
            f'/author/{self.test_receiver.id}/followers/xdthisisnotarealid/',
            **self.headers
        )
        # Test request exists
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# TODO: Finish PUT tests and maybe update DELETE
# """
# Testing PUT on a follow request on /author/{authorID}/followers/{followID}
# """
# class FollowPutTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.headers = {
#            'HTTP_AUTHORIZATION': 'Basic ' + 
#                 base64.b64encode(b'user1:123').decode("ascii")
#         }

#         # Create an author that will send a request
#         self.test_sender = Author.objects.create(**get_test_credentials(),
#                                                  **get_author_fields())
#         self.test_sender.set_password("123")
#         self.test_sender.save()

#         # Create an author that will receive a request
#         self.test_receiver = Author.objects.create(**get_test_credentials(1),
#                                                    **get_author_fields(1))
#         self.test_receiver.set_password("123")
#         self.test_receiver.save()

#         # self.follow = FriendShip.objects.create(author_local=self.test_receiver, author_remote=AuthorSerializer(self.test_sender).data)
#         # self.follow_serialized = FriendshipSerializer(self.follow)
    
#     def test_put_follow_successful(self):
#         response = self.client.put(
#             f'/author/{self.test_receiver.id}/followers/{self.test_sender.id}/',
#             data=json.dumps(get_test_credentials()),
#             content_type='application/json',
#             **self.headers
#         )

#         print(f'aaa = {response.data}')

#         # Test request DNE since nothing is put in yet
#         # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

"""
Testing DELETE on a follow request on /author/{authorID}/followers/{followID}
"""
class FollowDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.headers = {
           'HTTP_AUTHORIZATION': 'Basic ' + 
                base64.b64encode(b'user1:123').decode("ascii")
        }

        # Create an author that will send a request
        self.test_sender = Author.objects.create(**get_test_credentials(),
                                                 **get_author_fields())
        self.test_sender.set_password("123")
        self.test_sender.save()

        # Create an author that will receive a request
        self.test_receiver = Author.objects.create(**get_test_credentials(1),
                                                   **get_author_fields(1))
        self.test_receiver.set_password("123")
        self.test_receiver.save()

        self.follow = FriendShip.objects.create(author_local=self.test_receiver, author_remote=AuthorSerializer(self.test_sender).data)
        self.follow_serialized = FriendshipSerializer(self.follow)
    
    def test_delete_follow_successful(self):
        response = self.client.delete(
            f'/author/{self.test_receiver.id}/followers/{self.test_sender.id}/',
            **self.headers
        )
        # Test request DNE since deleted
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    