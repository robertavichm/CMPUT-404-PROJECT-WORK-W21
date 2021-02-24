from rest_framework import serializers
from . import models



class AuthorSerializer(serializers.ModelSerializer):
    class:
        model.Author
        fields = {"id", "displayName", "host", "url", "type"}
