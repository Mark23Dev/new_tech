from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ForumPostViewSet, ForumCommentViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'forum-posts', ForumPostViewSet)
router.register(r'forum-posts/(?P<post_id>\d+)/comments', ForumCommentViewSet, basename='forumcomment')

# Define the urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include all the routes registered by the router
]
