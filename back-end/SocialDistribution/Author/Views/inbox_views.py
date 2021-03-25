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

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework import permissions

class InboxPermissions(permissions.BasePermission):
    def __init__(self):
        self.Allowed = ["POST"]
    def has_permission(self,request,view):
        if request.method in self.Allowed:
            return True
        return request.user.is_authenticated

#need authentication that allows 
@api_view(["GET","POST","DELETE"])
@permission_classes([InboxPermissions])
def handle_inbox(request,author_id):
    author = get_object_or_404(Author,pk=author_id)

    if request.method == "POST":
        json_data = request.data
        post_type = json_data["type"]
        
        return handle_type(post_type,json_data,author)
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
            response["items"].append(all_notif[i].items)
        #ser = NotificationSerializer(all_notif, many=True)
        return JsonResponse(response, safe=False)
    if request.method == "DELETE":
        Notification.objects.filter(author_id=author_id).delete()
        return HttpResponse("inbox cleared")

def handle_type(post_type,data,author):
    new_notification = Notification(author_id=author)
    new_notification.items = data
    
    if post_type=="follow":
        if("author_id" in data):
            requestor_data = data["author_id"]
            
            new_friendship = FriendShip(author_primary=author,author_remote=requestor_data)
            new_friendship.save()
            new_notification.save() 
            return HttpResponse("follow request sent")
    if post_type=="like":
        if "author_id" in data:
            liker_id = data["author_id"]
            
            new_like = Like(author_id=author, liker_id=liker_id)
            if "post_id" in data:
                post_id = data["post_id"]
                post = get_object_or_404(Post,pk=post_id)
                new_like.post_id = post
            if "comment_id" in data:
                comment_id = data["comment_id"]
                comment = get_object_or_404(Comment , pk=comment_id)
                new_like.comment_id = comment
            new_like.save()
            new_notification.save() 
            return HttpResponse("like notification sent")
    
    return HttpResponse("invalid post body type")



    
