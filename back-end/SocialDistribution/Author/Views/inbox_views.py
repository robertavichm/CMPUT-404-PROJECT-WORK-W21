from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from ..author_serializer import AuthorSerializer,PostSerializer,CommentSerializer,LikeSerializer,NotificationSerializer
from ..models import Author, Post, Comment, Like, Notification, FriendShip
from ..formatters import format_notif
import json


@api_view(["GET","POST","DELETE"])
def handle_inbox(request,author_id):
    author = get_object_or_404(Author,pk=author_id)
    if request.method == "POST":
        json_data = request.data
        post_type = json_data["item"]["type"]
        item = json_data["item"]
        return handle_type(post_type,item,author)
    if request.method == "GET":
        all_notif = Notification.objects.filter(author_id=author)
        response = {}
        response["type"] = "inbox"
        response["author"] = author_id
        response["items"] = []
        for i in range(0,len(all_notif)):
            # formated, code = format_notif(all_notif[i])
            # if(code == 500):
            #     return HttpResponse(formated,status=500)
            # if(code == 404):
            #     #delete notification?
            #     pass
            # else:
            #     response["items"].append(formated)
            response["items"].append(all_notif[i].item)
        #ser = NotificationSerializer(all_notif, many=True)
        return JsonResponse(response, safe=False)
    if request.method == "DELETE":
        Notification.objects.filter(author_id=author_id).delete()
        return HttpResponse("inbox cleared")

def handle_type(post_type,data,author):
    new_notification = Notification(author_id=author)
    new_notification(items=data)
    new_notification.save() 
    # if post_type=="post":
    #     if("post_id" in data):
    #         id = data["post_id"]
    #         obj = Post.objects.get(post_id=id)
    #         new_notification.post_id = obj
    #         new_notification.save()
    #         return HttpResponse("post notification sent")
    # if post_type=="follow":
    #     if("author_id" in data):
    #         requestor_path = data["author_id"]
            

    #         new_friendship = FriendShip(author_primary=author,author_remote=obj)
    #         new_friendship.save()
    #         new_notification.request_id = new_friendship
    #         new_notification.save()
    #         return HttpResponse("follow request sent")
    # if post_type=="like":
    #     if "author_id" in data:
    #         liker_id = data["author_id"]
            
    #         new_like = Like(author_id=author, liker_id=liker_id)
    #         if "post_id" in data:
    #             post_id = data["post_id"]
    #             post = Post.objects.get(post_id=post_id)
    #             new_like.post_id = post
    #         if "comment_id" in data:
    #             comment_id = data["comment_id"]
    #             comment = Comment.objects.get(comment_id=comment_id)
    #             new_like.comment_id = comment
    #         new_like.save()
    #         new_notification.like_id = new_like
    #         new_notification.save()
    #         return HttpResponse("like notification sent")
    
    return HttpResponse("invalid post body type")



    
