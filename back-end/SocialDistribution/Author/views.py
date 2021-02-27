from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Author,Post
import json

# Create your views here.
@api_view(["POST","GET"])
def open_path(request):
    if(request.method == "POST"):
        json_data = request.data
        new_author = Author()
        for k, v in json_data.items():
            setattr(new_author, k, v)
        new_author.save()
        return HttpResponse(status=status.HTTP_200_OK)
    if(request.method == "GET"):
        return HttpResponse("path test")


@api_view(["GET","POST"])
def author_operation(request,pk):
    """
        handles paths authors/{author_id}
    """
    if request.method == "GET":
        data = get_object_or_404(Author, pk=pk)
        response = {}
        response["id"] = data.id
        response["host"] = data.host
        response["displayName"] = data.displayName
        response["url"] = data.url
        #response["github"] = data.github
        
        return JsonResponse(response,safe=False)
    if(request.method == "POST"):
        json = request.data
        author = Author.objects.filter(author_id=pk)
        if(author.count == 1):
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







@api_view(["GET","POST"])
def handle_inbox(request,author_id):
    return HttpResponse("TODO General inbox operation")

@api_view(["GET","POST"])
def get_likes(request,author_id):
    return HttpResponse("TODO get author likes")




