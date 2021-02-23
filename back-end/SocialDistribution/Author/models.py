from django.db import models

# Create your models here.





class Author(models.Model):

    author_id = models.AutoField(primary_key=True)
    display_name = models.TextField()
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
