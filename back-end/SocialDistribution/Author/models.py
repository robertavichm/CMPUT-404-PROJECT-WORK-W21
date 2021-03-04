from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Author(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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
        choice3 = "application/base64"
        choice4 = "image/png;base64"
        choice5 = "image/jpeg;base64"

    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    title = models.TextField()
    type = models.TextField(default="post")
    description = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    contentType = models.TextField(choices=ContentTypeChoice.choices)
    content = models.TextField()
    categories = ArrayField(models.CharField(max_length=20),default=list)
    commentLink = models.TextField()
    commentCount = models.IntegerField(default=0)
    pageSize = models.IntegerField()
    published = models.DateTimeField(default=timezone.now, editable=False)
    visibility = models.TextField()
    unlisted = models.BooleanField()


class FriendShip(models.Model):
    FriendShipId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_primary = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="primary")
    author_friend = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="friend")
    accepted = models.BooleanField(default=False)
 

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    contentType = models.TextField()
    published = models.DateTimeField(default=timezone.now, editable=False)
    comment = models.TextField()
    type = models.TextField(default="comment")

class Like(models.Model):
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="likee")
    object_id = models.TextField()
    liker_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="liker")
    
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    #type = "likes"

#general inbox check
class Notification(models.Model):
    #unique id
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #author its sent to
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    #isntances of what is sent
    #request_id = models.ForeignKey(Author, on_delete=models.CASCADE, null=True,related_name="requester")
    request_id = models.ForeignKey(FriendShip, on_delete=models.SET_NULL, null=True)
    like_id = models.ForeignKey(Like, on_delete=models.SET_NULL, null=True)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
