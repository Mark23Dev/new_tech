from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Challenge, Submission, LeaderboardEntry
from .serializers import ChallengeSerializer, SubmissionSerializer, LeaderboardEntrySerializer

class UpcomingChallengesView(generics.ListAPIView):
    """API endpoint to list all upcoming challenges."""
    queryset = Challenge.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChallengeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating, or deleting a specific challenge."""
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmitChallengeView(generics.CreateAPIView):
    """API endpoint for submitting an entry to a challenge."""
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        challenge_id = self.request.data.get('challenge_id')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        serializer.save(user=self.request.user, challenge=challenge)

class LeaderboardView(generics.ListAPIView):
    """API endpoint to retrieve the leaderboard for a specific challenge."""
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        challenge_id = self.kwargs['challenge_id']
        return LeaderboardEntry.objects.filter(challenge_id=challenge_id).order_by('-score')
