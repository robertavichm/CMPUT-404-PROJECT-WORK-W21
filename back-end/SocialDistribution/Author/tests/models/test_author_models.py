from django.test import TestCase
from Author.models import *
from Author.tests.dummy_model_fields import *

class AuthorModelsTestCase(TestCase):
    def setUp(self):
        # Create and initialize test author model
        self.test_author_fields = get_author_fields()
        self.author = Author.objects.create(**self.test_author_fields)

        # Create and initialize test post
        self.test_post_fields = get_post_fields()
        self.post = Post.objects.create(**self.test_post_fields, author_id=self.author)

        # Create and initialize test friend (author) and friendship model
        self.test_author_friend_fields = get_author_fields()
        self.author_friend = Author.objects.create(**self.test_author_friend_fields)
        self.friendship = FriendShip.objects.create(author_primary=self.author, 
                                                    author_friend=self.author_friend,
                                                    accepted=True)

        self.test_like_fields = get_like_fields()
        self.like = Like.objects.create(**self.test_like_fields,
                                        author_id=self.author,
                                        liker_id=self.author_friend,
                                        comment_id=self.comment,
                                        post_id=self.post)

    def test_create_author(self):
        self.assertTrue(self.author.id)
        self.assertEqual(self.author.displayName, self.test_author_fields["displayName"])
        self.assertEqual(self.author.host, self.test_author_fields["host"])
        self.assertTrue(self.author.url, self.test_author_fields["url"])
        self.assertTrue(self.author.type, self.test_author_fields["type"])
        self.assertTrue(self.author.github, self.test_author_fields["github"])

    def test_create_post(self):
        self.assertTrue(self.post.post_id)
        self.assertTrue(self.post.author_id)
        self.assertEqual(self.post.type, "post")
        self.assertEqual(self.post.description, self.test_post_fields["description"])
        self.assertEqual(self.post.source, self.test_post_fields["source"])
        self.assertEqual(self.post.origin, self.test_post_fields["origin"])
        self.assertEqual(self.post.contentType, self.test_post_fields["contentType"])
        self.assertEqual(self.post.content, self.test_post_fields["content"])
        self.assertEqual(self.post.categories, self.test_post_fields["categories"])
        self.assertEqual(self.post.commentLink, self.test_post_fields["commentLink"])
        self.assertEqual(self.post.commentCount, self.test_post_fields["commentCount"])
        self.assertEqual(self.post.pageSize, self.test_post_fields["pageSize"])
        self.assertTrue(self.post.published)
        self.assertEqual(self.post.visibility, self.test_post_fields["visibility"])
        self.assertFalse(self.post.unlisted)


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
