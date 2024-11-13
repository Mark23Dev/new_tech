from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChallengeViewSet,
    SubmissionViewSet,  # Add this import if you create SubmissionViewSet
    LeaderboardEntryViewSet
)

# Initialize the router
router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'submissions', SubmissionViewSet, basename='submission')  # Add this line

urlpatterns = [
    path('api/', include(router.urls)),
]
