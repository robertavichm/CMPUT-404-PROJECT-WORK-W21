from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from .author_serializer import AuthorSerializer, LikeSerializer, FriendshipSerializer, NodeSerializer
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


# if the response autheticates return persons data
@api_view(["GET"])
def login(request):
    if(request.user.is_authenticated):
        if(request.user.is_active):
            ser = AuthorSerializer(request.user, many=False)
            return JsonResponse(ser.data, safe=False)
        else:
            return HttpResponseBadRequest("not active account")


@api_view(["POST", "GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def open_path(request):
    """
        handles paths authors/
    """
    if(request.method == "POST"):
        json_data = request.data
        new_author = Author(is_active=False)
        # Creating new user login information
        if "password" in json_data:
            password = json_data["password"]
            json_data.pop("password")
            new_author.set_password(password)
            new_author.username = json_data["username"]
        for k, v in json_data.items():
            setattr(new_author, k, v)
        new_author.host = HOST_URL
        url = new_author.host + "author/" + str(new_author.id)
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
        ser = AuthorSerializer(data, many=True)
        return JsonResponse(ser.data, safe=False)


@api_view(["GET", "POST"])
#@authentication_classes([BasicAuthentication])
#@permission_classes([IsAuthenticated])
def author_operation(request,pk):
    """
        handles paths authors/{author_id}
    """
    if request.method == "GET":
        instance = get_object_or_404(Author, pk=pk)
        ser = AuthorSerializer(instance, many=False)
        return JsonResponse(ser.data, safe=False)
    if(request.method == "POST"):
        json_data = request.data
        author = get_object_or_404(Author, pk=pk)
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
    # where author_id is local
    friend_local = FriendShip.objects.filter(author_local=author_id, accepted=True)
    for i in range(0,len(friend_local)):
        response["items"].append(friend_local[i].author_remote)
    return JsonResponse(response, safe=False)


@api_view(["GET", "PUT", "DELETE"])
def handle_follow(request,author_id,follow_id):
    """
        handles paths authors/{author_id}/followers/{follower_id}
    """
    if request.method == "GET":
        response = {}
        author = get_object_or_404(Author,pk=author_id)
        data = FriendShip.objects.filter(author_local=author_id, author_remote__id__icontains=follow_id)
        recipricol = FriendShip.objects.filter(author_local=follow_id, author_remote__id__icontains=author_id)
        first = False
        second = False
        for i in range(0, len(data)):
            response["accepted"] = data[i].accepted
            if data[i].accepted:
                first = True
        for i in range(0,len(recipricol)):
            if recipricol[i].accepted:
                second = True
        if(second == True and first == True):
            response["friends"] = True
        else:
            response["friends"] = False
        return JsonResponse(response,safe =False)
    # kinda bad form probably should be a POST but oh well.
    if request.method == "PUT":
        data = FriendShip.objects.filter(author_local=author_id, author_remote__id__icontains=follow_id)
        if(data.count() > 0):

            instance = FriendShip.objects.get(author_local=author_id, author_remote__id__icontains=follow_id)
            instance.accepted = True
            instance.save()
            return HttpResponse("request accepted: ", data[0].FriendShipId)
        return HttpResponseBadRequest()
    if request.method == "DELETE":
        data = FriendShip.objects.filter(author_local=author_id, author_remote__id__icontains=follow_id)
        if(data.count() > 0):
            instance = FriendShip.objects.get(author_local=author_id, author_remote__id__icontains=follow_id)
            instance.delete()
            return HttpResponse("friendship over")


@api_view(["GET", "POST"])
def get_likes(request, author_id):
    """
        handles paths authors/{author_id}/liked
    """
    if request.method == "GET":
        get_object_or_404(Author, pk=author_id)
        response = {}
        response["type"] = "liked"
        response["items"] = []
        liked = Like.objects.filter(liker_id__id=author_id)
        for i in range(0, len(liked)):
            new_like = like_formatter(liked[i])
            response["items"].append(new_like)
        return JsonResponse(response, safe=False)
    else:
        author = get_object_or_404(Author, pk=author_id)
        liker = request.data["author"]
        object_id = request.data["object"]

        new_like = Like(author_id=author, liker_id=liker, object_id=object_id)
        existing = Like.objects.filter(author_id=author, liker_id=liker, object_id=object_id)
        if(existing.count() > 0):
            return HttpResponseBadRequest("like object")
        new_like.save()
        return("like saved")

@api_view(["GET","DELETE"])
@permission_classes([IsAuthenticated])
def get_node(request, node_url):
    if(request.method == "GET"):
        node = get_object_or_404(Node, pk=node_url)
        ser = NodeSerializer(node, many=False)
        return JsonResponse(ser.data, safe=False)
    if(request.method == "DELETE"):
        host = request.data["host"]
        node = get_object_or_404(Node, pk=host)
        node.delete()
        return HttpResponse("node deleted")


@api_view(["GET","POST","DELETE"])
@permission_classes([IsAuthenticated])
def get_all_nodes(request):
    if(request.method== "GET"):
        response = {}
        response["type"] = "nodes"
        response["items"] = []
        nodes = Node.objects.all()
        for node in nodes:
            ser = NodeSerializer(node,many=False)
            response["items"].append(ser.data)
        return JsonResponse(response, safe=False)
    if(request.method == "DELETE"):
        host = request.data["host"]
        node = get_object_or_404(Node, pk=host)
        node.delete()
        return HttpResponse("node deleted")
    else:
        if(request.method == "POST"):
            new_node = Node()
            for k,v in request.data.items():
                setattr(new_node, k ,v)
            new_node.save()
            return JsonResponse(NodeSerializer(new_node, many=False).data, safe=False)
