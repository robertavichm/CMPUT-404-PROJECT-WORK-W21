from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from ..author_serializer import AuthorSerializer,PostSerializer,CommentSerializer,LikeSerializer,NotificationSerializer
from ..models import Author, Post, Comment, Like, Notification, FriendShip
import json


@api_view(["GET","POST"])
def handle_inbox(request,author_id):
    author = get_object_or_404(Author,pk=author_id)
    if request.method == "POST":
        json_data = request.data
        post_type = json_data["type"]
        return handle_type(post_type,json_data,author)
    if request.method == "GET":
        all_notif = Notification.objects.filter(author_id=author)
        ser = NotificationSerializer(all_notif, many=True)
        return JsonResponse(ser.data,safe=False)




def handle_type(post_type,data,author):
    new_notification = Notification(author_id=author) 
    if post_type=="post":
        if("post_id" in data):
            id = data["post_id"]
            obj = Post.objects.get(post_id=id)
            new_notification.post_id = obj
            return HttpResponse("post notification sent")
    if post_type=="follow":
        if("author_id" in data):
            requestor_id = data["author_id"]
            obj = Author.objects.get(id=requestor_id)
            new_friendship = FriendShip(author_primary=author,author_friend=obj)
            new_friendship.save()
            new_notification.request_id = new_friendship
            new_notification.save()
            return HttpResponse("follow request sent")
    if post_type=="like":
        if "author_id" in data:
            liker_id = data["author_id"]
            obj = Author.objects.get(id=liker_id)
            new_like = Like(author_id=author, liker_id=obj)
            if "post_id" in data:
                post_id = data["post_id"]
                post = Post.objects.get(post_id=post_id)
                new_like.post_id = post
            if "comment_id" in data:
                comment_id = data["comment_id"]
                comment = Comment.objects.get(comment_id=comment_id)
                new_like.comment_id = comment
            new_like.save()
            new_notification.like_id = new_like
            new_notification.save()
            return HttpResponse("like notification sent")
    return HttpResponse("invalid post body type")
