from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from ..author_serializer import AuthorSerializer,PostSerializer,CommentSerializer,LikeSerializer
from ..models import Author, Post, Comment, Like
from ..formatters import post_formater, comment_formatter, like_formatter
import json

import uuid
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated


@api_view(["GET","POST"])
def general_post(request,author_id):
    if request.method == "POST":
        new_post = Post()
        json_data = request.data
        auth = get_object_or_404(Author, pk=author_id)
        new_post.post_id = uuid.uuid4()
        new_post.author_id = auth
        new_post.id = auth.url +"/posts/"+str(new_post.post_id)
        new_post.source = new_post.id
        new_post.origin = new_post.id
        new_post.commentLink = new_post.id+"/comments/"
        for k,v in json_data.items():
            setattr(new_post, k, v)
        new_post.save()
        formatted = post_formater(new_post,False)
        
        #notify_friends(author_id)
        return JsonResponse(formatted)
    if request.method == "GET":
        # Can't GET post from invalid author
        auth = get_object_or_404(Author, pk=author_id)

        response = {}
        response["type"] = "posts"
        response["items"] = []
        posts = Post.objects.filter(author_id=author_id, visibility="PUBLIC")
        for i in range(0,len(posts)):
            new_formatted = post_formater(posts[i],True)
            response["items"].append(new_formatted)

        return JsonResponse(response, safe=False)
        
@api_view(["GET"])
def get_all(request):
    response = {}
    response["type"] = "posts"
    response["items"] = []
    posts = Post.objects.filter(visibility="PUBLIC")
    for i in range(0, len(posts)):
        formatted = post_formater(posts[i],True)
        response["items"].append(formatted)
    return JsonResponse(response, safe =False)

@api_view(["GET","POST","PUT","DELETE"])
def post_operation(request,author_id,post_id):
    if(request.method == "GET"):
        data = get_object_or_404(Post,pk=post_id)
        formatted = post_formater(data,True)
        return JsonResponse(formatted, safe=False)

    if(request.method == "POST"):
        
        post = get_object_or_404(Post,pk=post_id)
     
        if(post.author_id != request.user):
            #return forbidden
            return HttpResponse("you dont own this post you sneaky devil",status=status.HTTP_403_FORBIDDEN)
        json_data = request.data
        
        for k,v in json_data.items():
            setattr(post, k, v)
        post.save()
        return HttpResponse(status=status.HTTP_200_OK)

    if(request.method == "PUT"):
        pass

    if(request.method == "DELETE"):
        data = get_object_or_404(Post,pk=post_id)
        data.delete()
        return HttpResponse("post deleted",status=status.HTTP_200_OK)
    return HttpResponse("TODO general post operation")


@api_view(["GET"])
def get_post_likes(request, author_id, post_id):
    response = {}
    response["type"] = "liked"
    response["items"] = []
    post = get_object_or_404(Post,pk=post_id)
    object_id = post.id 
    likes = Like.objects.filter(object_id__icontains=object_id)
    #likes = Like.objects.filter(author_id=author_id,post_id=post_id,comment_id=None)
    for i in range(0,len(likes)):
        new_like = like_formatter(likes[i])
        response["items"].append(new_like)
    return JsonResponse(response, safe=False)


@api_view(["GET", "POST"])
def general_comments(request, author_id, post_id):
    #GET
    #queryset
    #comment = Comments.objects.filter(auther_id=author_id,post_id=post_id)
    #for(i in range(0,len(comment)):
    #   Specific instance
    #   comment[i].comment_id
    #ser = CommentSerializer(comment,many=True)
    if(request.method == "GET"):
        comments = Comment.objects.filter(post_id=post_id)
        response = {}
        response["type"] = "comment"
        response["items"] = []
        for i in range(0,len(comments)):
            formatted = comment_formatter(comments[i])
            response["items"].append(formatted)

        return JsonResponse(response,safe=False)
    elif(request.method == "POST"):
        
        json_data = request.data
        commenter_data = json_data["author_id"]
        json_data.pop("author_id")
        
        post = get_object_or_404(Post,pk=post_id)
        new_comment = Comment(author_id=commenter_data,post_id=post)
        for k,v in json_data.items():
            setattr(new_comment, k, v)
        new_comment.save()
        post.commentCount +=1
        post.save()
        return HttpResponse(new_comment.comment_id)    
    return HttpResponse("TODO General comment return")


@api_view(["GET"])
def get_comment_likes(request, author_id, post_id, comment_id):
    response = {}
    response["type"] = "liked"
    response["items"] = []
    post = get_object_or_404(Post,pk=post_id)
    object_id = post.id+"/comments/"+comment_id
    
    #return HttpResponse(object_id) 
    likes = Like.objects.filter(object_id__icontains=object_id)
    for i in range(0,len(likes)):
        new_like = like_formatter(likes[i])
        response["items"].append(new_like)
    return JsonResponse(response, safe=False)


#not sure if this path is even necessary
@api_view(["GET","POST","DELETE"])
def specific_comments(request, author_id, post_id, comment_id):
    if(request.method == "GET"):
        data = get_object_or_404(Comment,pk=comment_id)
        response = {}
        response["type"] = "comment"
        response["items"] = []
        response["items"].append(comment_formatter(data))
        return JsonResponse(response, safe=False)
    if(request.method == "POST"):
        json_data = request.data
        data = get_object_or_404(Comment,pk=comment_id)
        for k,v in json_data.items():
            setattr(data,k,v)
        data.save()
        return HttpResponse("comment updated")        

    if(request.method == "DELETE"):
        data = get_object_or_404(Comment,pk=comment_id)
        data.delete()
        return HttpResponse("comment deleted")

#later need to tie this all in with inbox
def notify_friends(author_id):
    pass
