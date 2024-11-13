from django.urls import path
from .views import (
    ChallengeListView,
    ChallengeDetailView,
    ChallengeSubmitView,
    LeaderboardView,
)

urlpatterns = [
    path('challenges/upcoming/', ChallengeListView.as_view(), name='upcoming_challenges'),
    path('challenges/<int:challenge_id>/', ChallengeDetailView.as_view(), name='challenge_detail'),
    path('challenges/submit/', ChallengeSubmitView.as_view(), name='submit_challenge'),
    path('challenges/leaderboard/', LeaderboardView.as_view(), name='challenge_leaderboard'),
]
