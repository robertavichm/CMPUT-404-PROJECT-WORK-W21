from django.db import models

# Create your models here.





class Author(models.Model):

    id = models.AutoField(primary_key=True)
    displayName = models.TextField()
    host = models.TextField()
    url = models.TextField()
    Type = models.TextField()



class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.TextField()
    Type = models.TextField()
    description = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    contentType = models.TextField()
    content = models.TextField()
    categories = models.TextField()
    commentLink = models.TextField()
    commentCount = models.IntegerField()
    pageSize = models.IntegerField()
    published = models.BooleanField()
    visibility = models.TextField()
    unlisted = models.BooleanField()

# class FriendShip(models.Model):
#     FriendShipId = models.AutoField(primary_key=True)
#     author_primary = models.ForeignKey(Author, on_delete=models.CASCADE)
#     author_friend = models.ForeignKey(Author, on_delete=models.CASCADE)

 

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    object_id = models.TextField()
    recipient_id = models.ForeignKey(Author, on_delete=models.CASCADE) 

