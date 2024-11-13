from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ForumPostViewSet, ForumCommentViewSet

router = DefaultRouter()
router.register(r'forum-posts', ForumPostViewSet)
# Specify a basename for forum-comments, since it's a dynamic queryset
router.register(r'forum-posts/(?P<post_id>\d+)/comments', ForumCommentViewSet, basename='forum-comments')

urlpatterns = [
    path('', include(router.urls)),
]
