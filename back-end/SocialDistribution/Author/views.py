from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Author,Post


# Create your views here.
@api_view(["GET","POST"])
def author_operation(request,pk):
    """
        handles paths authors/
        adds a course and gets a list of courses
    """
    if request.method == "GET":
        #data = get_object_or_404(Author, pk=author_id, deleted=False)
        return HttpResponse(pk)
    if(request.method == "POST"):
        json = request.data

        author = get_object_or_404(Author,pk=pk)
        for k, v in json_data.items():
                setattr(author, k, v)
        author.save()

    return HttpResponse("Hello word")

@api_view(["GET"])
def get_followers(request,author_id):
    return HttpResponse("follower path")

@api_view(["GET"])
def get_handle_follow(request,author_id,follow_id):
    return HttpResponse("follower operation path")
