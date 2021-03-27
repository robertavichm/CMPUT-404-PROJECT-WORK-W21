from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError

from .author_serializer import AuthorSerializer, LikeSerializer, FriendshipSerializer,NodeSerializer
from .models import Author, Post, Like, FriendShip, Node
from .formatters import like_formatter
import json

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
# this path is mostly for the sake of developing
from SocialDistribution.settings import HOST_URL

#if the response autheticates return persons data
@api_view(["GET"])
def login(request):
    if(request.user.is_authenticated):
        ser = AuthorSerializer(request.user,many=False)
        return JsonResponse(ser.data,safe=False)

@api_view(["POST","GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def open_path(request):
    """
        handles paths authors/
    """
    if(request.method == "POST"):
        json_data = request.data

        new_author = Author()
        
        # Creating new user login information
        if "password" in json_data:
            password = json_data["password"]
            json_data.pop("password")
            new_author.set_password(password)
            new_author.username = json_data["username"]

        for k, v in json_data.items():
            #Author(k=v)
            setattr(new_author, k, v)
        new_author.host = HOST_URL
        url = new_author.host+"author/"+str(new_author.id)
        new_author.url = url
        
        # Try creating user, 
        # if duplicate user, return Bad Request
        try:
            new_author.save()
        except IntegrityError:
            return HttpResponseBadRequest("username taken")

        return HttpResponse(str(new_author.id), status=status.HTTP_200_OK)

    if(request.method == "GET"):
        
        data = Author.objects.all()
        ser = AuthorSerializer(data,many=True)
        return JsonResponse(ser.data, safe=False)


@api_view(["GET","POST"])
#@authentication_classes([BasicAuthentication])
#@permission_classes([IsAuthenticated])
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

        # XXX: Commented this out, unsure if useful?
        # author(displayName=json_data["displayName"])
        # return HttpResponse(json_data["displayName"])

        #useless
        for k, v in json_data.items():
            setattr(author, k, v)
        author.save()
        return HttpResponse(status=status.HTTP_200_OK)  
    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
def get_followers(request,author_id):
    """
        handles paths authors/{author_id}/followers/
    """
    response = {}
    response["type"] = "followers"
    response["items"] = []
    #where author_id is local
    friend_local = FriendShip.objects.filter(author_local=author_id, accepted=True)    
    
    for i in range(0,len(friend_local)):
        #little bit of response cooking
        ser = AuthorSerializer(friend_local[i].author_local,many=False)
        response["items"].append(ser.data)
    
    
    return JsonResponse(response, safe=False)


@api_view(["GET","PUT","DELETE"])
def handle_follow(request,author_id,follow_id):
    """
        handles paths authors/{author_id}/followers/{follower_id}
    """
    if request.method == "GET":
        data = FriendShip.objects.filter(author_local=author_id,author_remote__id=follow_id,accepted=True)
        if(data.count() > 0):
            
            return HttpResponse("totally friends")
        return HttpResponse("not friends")
    #kinda bad form probably should be a POST but oh well.
    if request.method == "PUT":
        data = FriendShip.objects.filter(author_local=author_id, author_remote__id=follow_id)
        if(data.count() > 0):
            
            instance = FriendShip.objects.get(author_local=author_id, author_remote__id=follow_id)
            instance.accepted = True
            instance.save()
            return HttpResponse("request accepted: ",data[0].FriendShipId)
        return HttpResponseBadRequest()
    if request.method == "DELETE":
        data = FriendShip.objects.filter(author_local=author_id, author_remote=follow_id)
        if(data.count() > 0):
            instance = FriendShip.objects.get(author_local=author_id, author_remote=follow_id)
            instance.delete()
            return HttpResponse("friendship over")
            


@api_view(["GET"])
def get_likes(request,author_id):
    """
        handles paths authors/{author_id}/liked
    """
    response = {}
    response["type"] = "liked"
    response["items"] = []
    liked = Like.objects.filter(liker_id__id=author_id)
    #return HttpResponse(liked.count())
    for i in range(0,len(liked)):
        new_like = like_formatter(liked[i])
        response["items"].append(new_like)
    return JsonResponse(response, safe=False)


@api_view(["GET","POST","DELETE"])
def get_node(request,node_url):
    if(request.method == "GET"):
        node = get_object_or_404(Node, pk=node_url)
        ser = NodeSerializer(node, many=False)
        return JsonResponse(ser.data, safe=False)
    if(request.method == "POST"):
        new_node = Node(host=node_url)
        for k,v in request.data.items():
            setattr(new_node, k ,v)
        new_node.save()
        return JsonResponse(NodeSerializer(new_node, many=False).data, safe=False)
    if(request.method == "DELETE"):
        node = get_object_or_404(Node, pk=node_url)
        node.delete()
        return HttpResponse("node deleted")
