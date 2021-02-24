from django.urls import path
from . import views


urlpatterns = [
    path("", views.open_path),
    path('<pk>/', views.author_operation),
    path('<author_id>/followers/', views.get_followers),
    path('<author_id>/followers/<follow_id>/', views.handle_follow),
    path('<author_id>/posts/', views.general_post),
    path('<author_id>/liked/', views.get_likes),
    path('<author_id>/posts/<post_id>/likes/', views.get_post_likes),
    path('<author_id>/posts/<post_id>/', views.post_operation),
    path('<author_id>/posts/<post_id>/comments/', views.general_comments),
    path('<author_id>/posts/<post_id>/comments/likes/', views.get_comment_likes),
    path('<author_id>/posts/<post_id>/comments/<comment_id>/', views.specific_comments),
    path('<author_id>/inbox/', views.handle_inbox),

]
