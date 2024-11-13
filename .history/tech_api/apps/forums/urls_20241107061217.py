from django.urls import path
from .views import ForumPostListView, ForumPostDetailView, ForumCommentListView, ForumCommentDetailView

urlpatterns = [
    path('posts/', ForumPostListView.as_view(), name='forum-post-list'),  # List and create forum posts
    path('posts/<int:post_id>/', ForumPostDetailView.as_view(), name='forum-post-detail'),  # Retrieve, update, and delete a specific forum post
    path('posts/<int:post_id>/comments/', ForumCommentListView.as_view(), name='forum-comment-list'),  # List and create comments for a specific post
    path('comments/<int:comment_id>/', ForumCommentDetailView.as_view(), name='forum-comment-detail'),  # Retrieve, update, and delete a specific comment
]
