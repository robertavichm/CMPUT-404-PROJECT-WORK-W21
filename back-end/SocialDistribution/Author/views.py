from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view

# XXX: viewsets for later refactoring???
from rest_framework import status, viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from .author_serializer import AuthorSerializer, LikeSerializer, FriendshipSerializer
from .models import Author, Post, Like, FriendShip
from .formatters import like_formatter
import json

# Authentication, Registration 
# https://medium.com/swlh/jwt-auth-with-djangorest-api-9fb32b99b33c
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

# this path is mostly for the sake of developing
@api_view(["POST","GET"])
def open_path(request):
    if(request.method == "POST"):
        json_data = request.data
        new_author = Author()
        for k, v in json_data.items():
            #Author(k=v)
            setattr(new_author, k, v)
        url = new_author.host+"/author/"+str(new_author.id)
        new_author.url = url
        new_author.save()
        return HttpResponse(str(new_author.id),status=status.HTTP_200_OK)
    if(request.method == "GET"):
        data = Author.objects.all()
        ser = AuthorSerializer(data,many=True)
        return JsonResponse(ser.data, safe=False)


@api_view(["GET","POST"])
def author_operation(request,pk):
    """
        handles paths authors/{author_id}
    """
    if request.method == "GET":
        instance = get_object_or_404(Author, pk=pk)
        ser = AuthorSerializer(instance, many=False)
        #response["github"] = data.github
        
        
        return JsonResponse(ser.data,safe=False)
    if(request.method == "POST"):
        json_data = request.data
        author = get_object_or_404(Author,pk=pk)
        author(displayName=json_data["displayName"])
        return HttpResponse(json_data["displayName"])
        #useless
        for k, v in json_data.items():
            setattr(author, k, v)
        author.save()
        return HttpResponse(status=status.HTTP_200_OK)  
    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
def get_followers(request,author_id):
    response = {}
    response["type"] = "followers"
    response["items"] = []
    friends = FriendShip.objects.filter(author_primary=author_id, accepted=True)
    for i in range(0,len(friends)):
        ser = AuthorSerializer(friends[i].author_friend)
        response["items"].append(ser.data)
    
    return JsonResponse(response, safe=False)


@api_view(["GET","PUT","DELETE"])
def handle_follow(request,author_id,follow_id):
    if request.method == "GET":
        data = FriendShip.objects.filter(author_primary=author_id, author_friend=follow_id,accepted=True)
        if(data.count() > 0):
            
            return HttpResponse("totally friends")
        return HttpResponse("not friends")
    #kinda bad form probably should be a POST but oh well.
    if request.method == "PUT":
        data = FriendShip.objects.filter(author_primary=author_id, author_friend=follow_id)
        if(data.count() > 0):
            
            instance = FriendShip.objects.get(author_primary=author_id, author_friend=follow_id)
            instance.accepted = True
            instance.save()
            return HttpResponse("request accepted: ",data[0].FriendShipId)
    if request.method == "DELETE":
        data = FriendShip.objects.filter(author_primary=author_id, author_friend=follow_id)
        if(data.count() > 0):
            instance = FriendShip.objects.get(author_primary=author_id, author_friend=follow_id)
            instance.delete()
            return HttpResponse("friendship over")
            


@api_view(["GET"])
def get_likes(request,author_id):
    response = {}
    response["type"] = "liked"
    response["items"] = []
    liked = Like.objects.filter(liker_id=author_id)
    for i in range(0,len(liked)):
        new_like = like_formatter(liked[i],True)
        response["items"].append(new_like)
    return JsonResponse(response, safe=False)




