from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ForumPostViewSet, ForumCommentViewSet

router = DefaultRouter()
router.register(r'forum-posts', ForumPostViewSet)
router.register(r'forum-comments', ForumCommentViewSet, basename='forum-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('forum-posts/<int:post_id>/comments/', ForumCommentViewSet.as_view({'get': 'list', 'post': 'create'})),  # Add this line to register the post_id in the URL
]
