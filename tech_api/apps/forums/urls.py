from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ForumPostViewSet, ForumCommentViewSet

router = DefaultRouter()
router.register(r'forum-posts', ForumPostViewSet)
# Add basename explicitly since the queryset is dynamically determined
router.register(r'forum-posts/(?P<post_id>\d+)/comments', ForumCommentViewSet, basename='forum-comment')

urlpatterns = [
    path('', include(router.urls)),
]
