from django.test import TestCase, Client
from rest_framework import status
import json

from Author.models import Author,FriendShip
from Author.author_serializer import AuthorSerializer, FriendshipSerializer
from Author.tests.dummy_model_fields import get_author_fields, get_follow_fields

"""
Testing GET on a follow request on /author/{authorID}/followers/{followID}
"""
class FollowGetTest():
    def setUp(self):
        self.client = Client()

        self.test_sender_fields = get_author_fields()
        self.test_sender = Author.objects.create(**self.test_sender_fields)

        self.test_receiver_fields = get_author_fields()
        self.test_sender = Author.objects.create(**self.test_receiver_fields)