from django.urls import path
from .Views import post_views
from . import views


urlpatterns = [
    path("", views.open_path),
    path('author/<pk>/', views.author_operation),
    path('author/<author_id>/followers/', views.get_followers),
    path('author/<author_id>/followers/<follow_id>/', views.handle_follow),
    path('author/<author_id>/posts/', post_views.general_post),
    path('author/<author_id>/liked/', views.get_likes),
    path('author/<author_id>/posts/<post_id>/likes/', post_views.get_post_likes),
    path('author/<author_id>/posts/<post_id>/', post_views.post_operation),
    path('author/<author_id>/posts/<post_id>/comments/', post_views.general_comments),
    path('author/<author_id>/posts/<post_id>/comments/likes/', post_views.get_comment_likes),
    path('author/<author_id>/posts/<post_id>/comments/<comment_id>/', post_views.specific_comments),
    path('author/<author_id>/inbox/', views.handle_inbox),
    

]
