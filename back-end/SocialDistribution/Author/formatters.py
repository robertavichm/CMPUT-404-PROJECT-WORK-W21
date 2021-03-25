from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .author_serializer import AuthorSerializer,PostSerializer,CommentSerializer,LikeSerializer,NotificationSerializer
from .models import Author, Post, Comment, Like, Notification, FriendShip
import json
from SocialDistribution.settings import HOST_URL

def format_notif(notif):
    if(notif.request_id != None):
        response = {}
        response["type"] = "Follow"
        response["summary"] = (notif.request_id.author_friend.displayName+"wants to be friends with "+notif.request_id.author_primary.displayName,)
        primaryser = AuthorSerializer(notif.request_id.author_primary, many=False)
        friendser = AuthorSerializer(notif.request_id.author_friend, many=False)
        response["requester"] = friendser.data
        response["requestee"] = primaryser.data
        return response, 200

    if(notif.like_id != None):
        response = {}
        response["type"] = "Like"
        if(notif.like_id.comment_id != None and notif.like_id.post_id != None):
            response["summary"] = (notif.like_id.liker_id.displayName+" likes comment on post "+notif.like_id.post_id.title)
            response["liker"] = AuthorSerializer(notif.like_id.liker_id,many=False).data
            response["object"] = HOST_URL+"author/"+str(notif.like_id.author_id.id)+"/posts/"+ \
            str(notif.like_id.post_id.post_id)+"/comments/"+str(notif.like_id.comment_id.comment_id)

        elif(notif.like_id.comment_id != None and notif.like_id.post_id == None):
            return "like object comment id exists without a post id. shouldnt have gotten this far.",500 
        else:
            response["summary"] = (notif.like_id.liker_id.displayName+" likes post "+notif.like_id.post_id.title)
            response["liker"] = AuthorSerializer(notif.like_id.liker_id,many=False).data
            response["object"] = HOST_URL+"author/"+str(notif.like_id.author_id.id)+"/posts/"+ \
            str(notif.like_id.post_id.post_id)
        return response,200
    if(notif.post_id != None):
        return post_formater(notif.post_id,False), 200
    return "empty notification",404



def post_formater(post,comments):
    ser = {}
    ser_temp = PostSerializer(post, many=False)
    ser.update(ser_temp.data)
    author = get_object_or_404(Author, pk=post.author_id.id)
    author_ser = AuthorSerializer(author, many=False) 
    ser["author"] = author_ser.data
    ser["id"] = HOST_URL+"author/"+str(author.id)+"/posts/"+str(post.post_id)
    if(comments):
        ser["comments"] = []
        
        all_comments = Comment.objects.filter(post_id=post.post_id)
        for i in range(0,len(all_comments)):
            formatted_comm = comment_formatter(all_comments[i])
            ser["comments"].append(formatted_comm)
    return ser




def comment_formatter(comment):
    ser = {}
   
    
    comment_ser = CommentSerializer(comment, many=False)
    ser.update(comment_ser.data)
    #ser.update(ser_tem.data)
    ser["id"] = HOST_URL+"author/"+str(comment.post_id.author_id.id)+"/posts/"+str(comment.post_id.post_id)+"/comments/"+str(comment.comment_id)
    #ser_author = AuthorSerializer(author,many=False)
    #ser["author"] = comment.author_id
    return ser

def like_formatter(like,liker):
    ser = {}
    if liker:

        if(like.comment_id !=None and like.post_id !=None):
            ser["summary"] = like.author_id.displayName+ " likes a comment"
            ser["object"] = "author/"+str(like.author_id.id)+"/posts/"+str(like.post_id.post_id) + \
            "/comments/"+str(like.comment_id.comment_id)
        elif like.comment_id == None and like.post_id != None:
            ser["summary"] = liker.displayName+ " likes a post"
            ser["object"] = "http://localhost:8000/author/"+str(like.author_id.id)+"/posts/"+str(like.post_id.post_id)
        else:
            return 501
        ser["author"] =  like.liker_id
        return ser
    else:
        liker = get_object_or_404(Author, pk=like.author.id)
        
        ser["author"] =  AuthorSerializer(liker).data
        if(like.comment_id !=None and like.post_id !=None):
            ser["summary"] = liker["displayName"]+ " likes a comment"
            ser["object"] = "http://localhost:8000/author/"+str(like.author_id.id)+"/posts/"+str(like.post_id.post_id) + \
            "/comments/"+str(like.comment_id.comment_id)
        elif like.comment_id == None and like.post_id != None:
            ser["summary"] = liker.displayName+ " likes your post!"
            ser["object"] = "http://localhost:8000/author/"+str(like.author_id.id)+"/posts/"+str(like.post_id.post_id)
        else:
            return 501
        return ser
