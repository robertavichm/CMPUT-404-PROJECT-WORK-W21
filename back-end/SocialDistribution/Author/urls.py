from django.urls import path
from . import views


urlpatterns = [
    path('<pk>/', views.author_operation),
    path('<author_id>/followers/', views.get_followers),
    path('<author_id>/followers/<follow_id>/', views.get_handle_follow),
]
