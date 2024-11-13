from rest_framework import serializers
from .models import Challenge, Submission, LeaderboardEntry

class ChallengeSerializer(serializers.ModelSerializer):
    """Serializer for the Challenge model."""
    class Meta:
        model = Challenge
        fields = '__all__'  # or you can specify fields explicitly

class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for the Submission model."""
    class Meta:
        model = Submission
        fields = ['id', 'user', 'challenge', 'submission_data', 'created_at']  # Adjust fields as necessary
        read_only_fields = ['user', 'created_at']  # User and created_at should be read-only

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    """Serializer for the LeaderboardEntry model."""
    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'challenge', 'user', 'score']  # Adjust fields as necessary
        read_only_fields = ['id']  # ID is read-only and should not be set by the user
