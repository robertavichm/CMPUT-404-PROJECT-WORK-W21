from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.TextField()
    host = models.TextField()
    url = models.TextField()
    type = models.TextField()
    github = models.TextField(null=True)


class Post(models.Model):

    class ContentTypeChoice(models.TextChoices):
        choice1 = "text/plain"
        choice2 = "text/markdown"

    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    title = models.TextField()
    Type = models.TextField()
    description = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    contentType = models.TextField(choices=ContentTypeChoice.choices)
    content = models.TextField()
    categories = models.TextField()
    commentLink = models.TextField()
    commentCount = models.IntegerField()
    pageSize = models.IntegerField()
    published = models.DateTimeField(default=timezone.now, editable=False)
    visibility = models.TextField()
    unlisted = models.BooleanField()


class FriendShip(models.Model):
    FriendShipId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_primary = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="primary")
    author_friend = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="friend")
    accepted = models.BooleanField(default=False)
 

class Like(models.Model):
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="likee")
    object_id = models.TextField()
    recipient_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="liker") 
    type = "likes"


class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    contentType = models.TextField()
    published = models.DateTimeField(default=timezone.now, editable=False)
    comment = models.TextField()
    type = 'comment'


#general inbox check
class Notification(models.Model):
    #unique id
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #author its sent to
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    #isntances of what is sent
    request_id = models.ForeignKey(FriendShip, on_delete=models.CASCADE, null=True)
    like_id = models.ForeignKey(Like, on_delete=models.CASCADE, null=True)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
