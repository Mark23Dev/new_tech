from rest_framework import serializers
from .models import LearningPath, UserProgress, Technology

class LearningPathSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and displaying learning path details."""
    class Meta:
        model = LearningPath
        fields = ['id', 'title', 'description', 'difficulty', 'duration', 'technologies', 'self_paced']

class PathRecommendationSerializer(serializers.Serializer):
    """Serializer for generating and recommending learning paths based on user profile."""
    interests = serializers.ListField(child=serializers.CharField(), required=False, default=[])
    skill_level = serializers.CharField(max_length=50, required=False, default=None)
    preferred_duration = serializers.IntegerField(required=False, default=None)


class GenerateLearningPathSerializer(serializers.Serializer):
    """Serializer for generating learning paths through Gemma/Gemini API."""
    goal = serializers.CharField(max_length=255, required=True)
    technologies = serializers.ListField(child=serializers.CharField(), required=False, default=[])
    duration = serializers.IntegerField(required=False, default=None)

class UpdateProgressSerializer(serializers.ModelSerializer):
    """Serializer for updating user progress on a learning path."""
    class Meta:
        model = UserProgress
        fields = ['path', 'progress', 'last_accessed']

class TechnologySerializer(serializers.ModelSerializer):
    """Serializer for listing technologies associated with learning paths."""
    class Meta:
        model = Technology
        fields = ['id', 'name', 'description']

class SelfPacedRecommendationSerializer(serializers.Serializer):
    """Serializer for self-paced course recommendations."""
    path_id = serializers.IntegerField()
    pace = serializers.CharField(max_length=50, required=True)
