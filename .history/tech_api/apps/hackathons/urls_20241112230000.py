from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.hackathons.views import (
    ChallengeViewSet,
    SubmissionViewSet,
    LeaderboardView,
    SubmitChallengeView,
    UpcomingChallengesView,
    ChallengeDetailView,
    LeaderboardView
)

# Initialize the router
router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'submissions', SubmissionViewSet, basename='submission')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upcoming-challenges/', UpcomingChallengesView.as_view(), name='upcoming-challenges'),
    path('api/challenge/<int:pk>/', ChallengeDetailView.as_view(), name='challenge-detail'),
    path('api/challenge/<int:challenge_id>/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('api/submit-challenge/', SubmitChallengeView.as_view(), name='submit-challenge')
]
