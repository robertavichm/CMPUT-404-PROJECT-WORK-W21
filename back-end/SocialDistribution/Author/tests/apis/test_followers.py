from django.test import TestCase, Client
from rest_framework import status
import json, base64

from Author.models import Author, FriendShip
from Author.author_serializer import AuthorSerializer, FriendshipSerializer
from Author.tests.dummy_model_fields import get_author_fields, get_follow_fields, get_test_credentials

invalid_uuid = '01234567-9ABC-DEF0-1234-56789ABCDEF0'

"""
Testing GET on a follow request on /author/{authorID}/followers
"""
class FollowGetTest(TestCase):
    def setUp(self):
        self.client = Client()
        # self.headers = {
        #    'HTTP_AUTHORIZATION': 'Basic ' + 
        #         base64.b64encode(b'user1:123').decode("ascii")
        # }

        # Create an author that will receive a request
        self.test_receiver = Author.objects.create(**get_test_credentials(),
                                                   **get_author_fields())
        self.test_receiver.set_password("123")
        self.test_receiver.save()

                # Create an author that will send a request
        self.test_sender1 = Author.objects.create(**get_test_credentials(1),
                                                 **get_author_fields(1))
        self.test_sender1.set_password("123")
        self.test_sender1.save()

        # Create an author that will send a request
        self.test_sender2 = Author.objects.create(**get_test_credentials(2),
                                                 **get_author_fields(2))
        self.test_sender2.set_password("123")
        self.test_sender2.save()

        # Create follow connections
        FriendShip.objects.create(
            author_local=self.test_receiver, 
            author_remote=AuthorSerializer(self.test_sender1).data, 
            accepted=True
        )

        FriendShip.objects.create(
            author_local=self.test_receiver, 
            author_remote=AuthorSerializer(self.test_sender2).data, 
            accepted=True
        )
    
        self.senders = [self.test_sender1, self.test_sender2]

    def test_get_followers_successful(self):
        response = self.client.get(
            f'/author/{self.test_receiver.id}/followers/'
        )

        serializer = AuthorSerializer(self.senders, many=True) 
        serializer_dict = []
        for i in serializer.data:
            serializer_dict.append(dict(i))

        # print(f'aa = {(serializer.data)}')
        # print('\n\n\n')
        # print(f'aa = {response.json()["items"][0]}')

        self.assertEquals(response.json()['type'], 'followers'),
        self.assertEqual(response.json()['items'], serializer_dict)