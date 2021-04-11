from django.urls import path,re_path
from .Views import post_views,inbox_views
from . import views


urlpatterns = [
    path("login/", views.login),
    path("nodes/", views.get_all_nodes),
    path("nodes/<node_url>/", views.get_node),
    path("posts/",post_views.get_all),
    path("author/", views.open_path),
    path('author/<pk>/', views.author_operation),
    path('author/<author_id>/followers/', views.get_followers),
    path('author/<author_id>/followers/<follow_id>/', views.handle_follow),
    re_path(r'author/(?P<author_id>.*)/posts/$', post_views.general_post),
    path('author/<author_id>/liked/', views.get_likes),
    path('author/<author_id>/posts/<post_id>/likes/', post_views.get_post_likes),
    path('author/<author_id>/posts/<post_id>/', post_views.post_operation),
    re_path(r'author/(?P<author_id>.*)/posts/(?P<post_id>.*)/comments/$', post_views.general_comments),
    path('author/<author_id>/posts/<post_id>/comments/<comment_id>/likes/', post_views.get_comment_likes),
    path('author/<author_id>/posts/<post_id>/comments/<comment_id>/', post_views.specific_comments),
    path('author/<author_id>/inbox/', inbox_views.handle_inbox),
    path('author/<author_id>/inbox/<notif_id>/', inbox_views.delete_item),
    
]
