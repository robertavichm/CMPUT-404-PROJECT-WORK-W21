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

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_item(request,author_id,notif_id):
    notif = get_object_or_404(Notification,pk=notif_id)
    notif.delete()
    return HttpResponse("Deleted inbox item")

#need authentication that allows 
@api_view(["GET","POST","DELETE"])
@permission_classes([IsAuthenticated])
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
            all_notif[i].items["notif_id"] = all_notif[i].notification_id
            response["items"].append(all_notif[i].items)
        #ser = NotificationSerializer(all_notif, many=True)
        return JsonResponse(response, safe=False)
    if request.method == "DELETE":
        Notification.objects.filter(author_id=author_id).delete()
        return HttpResponse("inbox cleared")

def handle_type(post_type,data,author):
    new_notification = Notification(author_id=author)
    #new_notification.items = data
    if post_type == "post":
        new_notification.items = data
        new_notification.save()
    if post_type=="follow":
        if("author_id" in data):
            requestor_data = data["author_id"]
            ser = AuthorSerializer(author, many=False)
            data["summary"] = data["author_id"]["displayName"]+ " wants to be "+author.displayName+"'s friend"
            if(FriendShip.objects.filter(author_local=author, author_remote__id=data["author_id"]["id"])):
                return HttpResponseBadRequest("request already sent")
            new_friendship = FriendShip(author_local=author,author_remote=requestor_data)
            new_friendship.save()

            new_notification.items = data 
            new_notification.save()
            return HttpResponse("follow request sent")
    if post_type=="like":
        existing = Like.objects.filter(author_id=author)
        if "author_id" in data:
            new_like = Like(author_id=author)
            if("author_id" in data):

                data["summary"] = data["author_id"]["displayName"]," likes your activity"
                new_like.liker_id  = data["author_id"]
            else:
                return HttpResponseBadRequest("need to specify author_id")

            
            
            if("object_id" in data):
                new_like.object_id = data["object_id"]
            else:
                return HttpResponseBadRequest("need to specify object_id")
            existing = Like.objects.filter(author_id=author,liker_id=data["author_id"],object_id=data["object_id"])
            if(existing.count() == 0):
                #return HttpResponseBadRequest("like with this data already exists")
                new_like.save()
            notif_check = Notification.objects.filter(author_id=author,items=data)
            if(notif_check.count() >0):
                return HttpResponseBadRequest("identical notification sent already")
            new_notification.items = data
            new_notification.save() 
            return HttpResponse("like notification sent")
    
    return HttpResponse("invalid post body type")



    
