from rest_framework import generics, permissions, status, viewsets, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Challenge, Submission, LeaderboardEntry
from .serializers import ChallengeSerializer, SubmissionSerializer, LeaderboardEntrySerializer
from django.utils import timezone
from rest_framework.decorators import action

# Challenge Views
class SubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing submission instances."""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


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

    def perform_update(self, serializer):
        # Add any custom update logic if needed, for instance, validating if updates are allowed
        serializer.save()

    def perform_destroy(self, instance):
        # Optionally handle any custom delete behavior before calling the default delete
        instance.delete()

# Submission Views

class SubmitChallengeView(generics.CreateAPIView):
    """API endpoint for submitting an entry to a challenge."""
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        challenge_id = self.request.data.get('challenge_id')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        # Ensure the user isn't submitting to a past challenge
        if challenge.end_date < timezone.now():
            raise serializers.ValidationError("You cannot submit to a past challenge.")
        serializer.save(user=self.request.user, challenge=challenge)

# Leaderboard Views

class LeaderboardView(generics.ListAPIView):
    """API endpoint to retrieve the leaderboard for a specific challenge."""
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        challenge_id = self.kwargs['challenge_id']
        return LeaderboardEntry.objects.filter(challenge_id=challenge_id).order_by('-score')

# Custom ViewSet to allow more flexible operations for Challenges

class ChallengeViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing challenge instances."""
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Custom action for submitting a challenge."""
        challenge = self.get_object()
        submission_data = {
            'user': request.user.id,
            'challenge': challenge.id,
            **request.data
        }
        serializer = SubmissionSerializer(data=submission_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Custom action for retrieving the leaderboard for a specific challenge."""
        challenge = self.get_object()
        leaderboard = LeaderboardEntry.objects.filter(challenge=challenge).order_by('-score')
        serializer = LeaderboardEntrySerializer(leaderboard, many=True)
        return Response(serializer.data)

