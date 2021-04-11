from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import uuid
# Create your models here.


class Author(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.TextField(null=True, unique = True)
    host = models.TextField(null=True)
    url = models.TextField(null=True)
    type = models.TextField(default="author")
    github = models.TextField(null=True)
    


class Post(models.Model):

    class ContentTypeChoice(models.TextChoices):
        choice1 = "text/plain"
        choice2 = "text/markdown"
        choice3 = "application/base64"
        choice4 = "image/png;base64"
        choice5 = "image/jpeg;base64"

    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.TextField(null=True)
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
    author_local = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="primary")   # local
    author_remote = models.JSONField()  # one author has to be local & another CAN be remote, hence the JSONFeild. 
    accepted = models.BooleanField(default=False)
    #author_friend = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="friend")    
 
#good?
class Comment(models.Model):
    class comment_choices(models.TextChoices):
        choice1 = "text/plain"
        choice2 = "text/markdown"
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    #post_id = models.TextField()
    #liker
    author_id = models.JSONField()
    contentType = models.TextField(choices=comment_choices.choices,default = "text/plain")
    published = models.DateTimeField(default=timezone.now, editable=False)
    comment = models.TextField()
    type = models.TextField(default="comment")


class Like(models.Model):
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    #author_id = TextField()
    #author of post or comment on our local server
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="likee")
    
    #where's the person liking this?
    #store json data incase author is on a different server
    liker_id = models.JSONField()
    #link to comment or post that was liked
    object_id = models.TextField(null=False)
    #type = "likes"

#general inbox check
class Notification(models.Model):
    #unique id
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #author its sent to
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    #isntances of what is sent
    #request_id = models.ForeignKey(Author, on_delete=models.CASCADE, null=True,related_name="requester")

    # request_id = models.ForeignKey(FriendShip, on_delete=models.SET_NULL, null=True)
    # like_id = models.ForeignKey(Like, on_delete=models.SET_NULL, null=True)
    # comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    # post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    items = models.JSONField(default=list)

#data to connect to another server
class Node(models.Model):
    #host of server
    host = models.TextField(primary_key=True,null=False)
    #user information for that server
    username = models.TextField(null=True)
    password = models.TextField(null=True)
    token = models.TextField(null=True)
    recieve = models.BooleanField(default=False)
#if we send like objects to foreign servers we cant look them up locally in author/{author_id}/liked
#hence we need a custom api to store where those foreign likes are stored.
# class ForeginLike(models.Model):
#     author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
#     object_id = models.TextField(null=False)
