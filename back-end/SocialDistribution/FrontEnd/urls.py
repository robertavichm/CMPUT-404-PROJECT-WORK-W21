from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('',views.login,name='login'),
    path('register',views.register,name='register'),
    path('home',views.home,name='home'),
    path('friends',views.friends,name='friedns')
]
