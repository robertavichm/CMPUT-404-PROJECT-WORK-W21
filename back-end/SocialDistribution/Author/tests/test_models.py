from django.test import TestCase
from django.core import serializers
from Author.models import *
from Author.tests.dummy_model_fields import *
import json

class AuthorModelsTestCase(TestCase):
    def setUp(self):
        # Create and initialize test Author model
        self.test_author_fields = get_author_fields()
        self.author = Author.objects.create(**self.test_author_fields)

        # Create and initialize test Post model
        self.test_post_fields = get_post_fields()
        self.post = Post.objects.create(**self.test_post_fields, author_id=self.author)

        # Create and initialize test friend (Author) and FriendShip model
        self.test_author_friend_fields = get_author_fields(1)
        self.author_friend = Author.objects.create(**self.test_author_friend_fields)
        self.friendship = FriendShip.objects.create(author_local=self.author, 
                                                    author_remote=serializers.serialize('json', [self.author_friend]),
                                                    accepted=True)
        
        # Create and initialize test Comment model
        self.test_comment_fields = get_comment_fields()
        self.comment = Comment.objects.create(**self.test_comment_fields,
                                               post_id=self.post, 
                                               author_id=serializers.serialize('json', [self.author]))

        # Create and initialize Like model
        self.test_like_fields = get_like_fields()
        self.like = Like.objects.create(**self.test_like_fields,
                                        author_id=self.author,
                                        liker_id=serializers.serialize('json', [self.author_friend]))

        # Create and initialize Notification model
        self.notification = Notification.objects.create(author_id=self.author)
        self.notification.items.append(serializers.serialize('json', [self.author_friend]))
        self.notification.items.append(serializers.serialize('json', [self.comment]))
        self.notification.items.append(serializers.serialize('json', [self.post]))
        self.notification.save()
        
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
        self.assertTrue(self.friendship.author_local)
        self.assertTrue(self.friendship.accepted)
        
    def test_create_comment(self):
        self.assertTrue(self.comment.comment_id)
        self.assertTrue(self.comment.post_id)
        self.assertTrue(self.comment.author_id)
        self.assertEqual(self.comment.contentType, self.test_comment_fields["contentType"])
        self.assertTrue(self.comment.published)
        self.assertEqual(self.comment.comment, self.test_comment_fields["comment"])
        self.assertEqual(self.comment.type, "comment")

    def test_create_like(self):
        self.assertTrue(self.like.like_id)
        self.assertTrue(self.like.author_id)
        self.assertTrue(self.like.liker_id)
        self.assertTrue(self.like.object_id)

    def test_create_notification(self):
        self.assertTrue(self.notification.notification_id)
        self.assertTrue(self.notification.author_id)
        self.assertTrue(self.notification.items)
