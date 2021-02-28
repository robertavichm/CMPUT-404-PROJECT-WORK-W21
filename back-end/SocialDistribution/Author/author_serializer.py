from rest_framework import serializers
from . import models 


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ["id", "displayName", "host", "url", "type"]
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ["post_id", "author_id","title", "type", "description", 
                  "source", "origin", "contentType", "content", "categories",
                  "commentLink", "commentCount", "pageSize", "published",
                  "visibility", "unlisted"]

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FriendShip
        fields = ["FriendshipId", "author_primary", "author_friend", "accepted"]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ["like_id", "author_id", "object_id", "recipient_id", "type"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["comment_id", "post_id", "author_id", "contentType", "published",
                  "comment", "type"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ["notification_id", "author_id", "request_id", "liked_id", 
                  "comment_id", "post_id"]
