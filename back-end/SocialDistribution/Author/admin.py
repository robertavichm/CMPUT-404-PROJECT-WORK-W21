from django.contrib import admin
from .models import Author, Post, FriendShip, Comment, Like, Notification

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(FriendShip)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Notification)
