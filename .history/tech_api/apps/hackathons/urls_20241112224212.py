from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UpcomingChallengesView,
    ChallengeDetailView,
    SubmitChallengeView,
    LeaderboardView,
    ChallengeViewSet
)

# Initialize the router
router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')

urlpatterns = [
    # Challenge-related URLs
    path('challenges/upcoming/', UpcomingChallengesView.as_view(), name='upcoming-challenges'),
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge-detail'),
    path('challenges/<int:challenge_id>/submit/', SubmitChallengeView.as_view(), name='submit-challenge'),
    
    # Leaderboard-related URLs
    path('challenges/<int:challenge_id>/leaderboard/', LeaderboardView.as_view(), name='challenge-leaderboard'),
    
    # Include ChallengeViewSet URLs
    path('api/', include(router.urls)),
]
