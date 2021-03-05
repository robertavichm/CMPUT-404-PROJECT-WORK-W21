from django.test import TestCase
from Author.models import *
from Author.tests.dummy_model_fields import get_author_fields

class AuthorModelsTestCase(TestCase):
    def setUp(self):
        # Create and initialize test author model
        self.test_author = get_author_fields()
        self.author = Author.objects.create(**self.test_author)

        # Create and initialize test friend (author) and friendship model
        self.test_author_friend = get_author_fields()
        self.author_friend = Author.objects.create(**self.test_author_friend)
        self.friendship = FriendShip.objects.create(author_primary=self.author, 
                                                    author_friend=self.author_friend,
                                                    accepted=True)
        
    def test_create_author(self):
        self.assertTrue(self.author.id)
        self.assertEqual(self.author.displayName, self.test_author["displayName"])
        self.assertEqual(self.author.host, self.test_author["host"])
        self.assertTrue(self.author.url, self.test_author["url"])
        self.assertTrue(self.author.type, self.test_author["type"])
        self.assertTrue(self.author.github, self.test_author["github"])

    def test_create_post(self):
        pass

    def test_create_friendship_true(self):
        self.assertTrue(self.friendship.FriendShipId)
        self.assertTrue(self.friendship.author_primary)
        self.assertTrue(self.friendship.author_friend)
        self.assertTrue(self.friendship.accepted)
        
    def test_create_comment(self):
        pass

    def test_create_like(self):
        pass

    def test_create_notification(self):
        pass
