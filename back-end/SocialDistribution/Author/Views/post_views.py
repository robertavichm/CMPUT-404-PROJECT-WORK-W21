from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Author,Post
import json





@api_view(["GET","POST"])
def general_post(request,author_id):
    if request.method == "POST":
        new_post = Post()
        json_data = request.data
        auth = get_object_or_404(Author, pk=author_id)
        new_post.author_id = auth
        for k,v in json_data.items():
            setattr(new_post, k, v)
        new_post.save()
        return HttpResponse("post_id: "+new_post.post_id,status=status.HTTP_200_OK)
    if request.method == "GET":
        posts = Post.objects.filter(author_id=author_id)
        returned = {}
        for i in range(0,len(posts)):
            returned[i]["title"] = posts[i].title
            returned[i]["type"] = posts[i].type
            returned[i]["description"] = posts[i].description
        return JsonResponse(returned, safe=False)
        
    


@api_view(["GET","POST","PUT","DELETE"])
def post_operation(request,author_id,post_id):
    return HttpResponse("TODO general post operation")


@api_view(["GET"])
def get_post_likes(request,author_id,post_id):
    return HttpResponse("TODO get post likes")


@api_view(["GET","POST"])
def general_comments(request,author_id,post_id):
    return HttpResponse("TODO General comment return")


@api_view(["GET"])
def get_comment_likes(request,author_id,post_id):
    return HttpResponse("TODO get post comment likes")


@api_view(["GET","POST","PUT","DELETE"])
def specific_comments(request,author_id,post_id,comment_id):
    return HttpResponse("TODO specific comment operation")
