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