from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .author_serializer import AuthorSerializer, LikeSerializer
from .models import Author, Post, Like
import json

# Create your views here.
@api_view(["POST"])
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
    return HttpResponse("TODO follower path")


@api_view(["GET","PUT","DELETE"])
def handle_follow(request,author_id,follow_id):
    return HttpResponse("TODO follower operation path")




@api_view(["GET"])
def get_likes(request,author_id):
    liked = Like.objects.filter(liker_id=author_id)
    ser = LikeSerializer(liked, many=True)
    return JsonResponse(ser.data, safe=False)




