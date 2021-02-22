from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view


# Create your views here.
@api_view(["GET"])
def open_path(request):
    """
        handles paths courses/
        adds a course and gets a list of courses
    """
    return HttpResponse("Hello word")
