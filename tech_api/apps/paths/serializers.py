from rest_framework import serializers
from .models import LearningPath, UserPathProgress, Technology, RecommendedCourse

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
        model = UserPathProgress
        fields = ['path', 'progress', 'last_accessed']

    def validate_progress(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Progress must be between 0 and 100.")
        return value


class TechnologySerializer(serializers.ModelSerializer):
    """Serializer for listing technologies associated with learning paths."""
    class Meta:
        model = Technology
        fields = ['id', 'name', 'description']

class SelfPacedRecommendationSerializer(serializers.Serializer):
    """Serializer for self-paced course recommendations."""
    path_id = serializers.IntegerField()
    pace = serializers.CharField(max_length=50, required=True)

class RecommendedCourseSerializer(serializers.ModelSerializer):
    """Serializer for recommended courses for a specific learning path."""
    class Meta:
        model = RecommendedCourse
        fields = ['id', 'title', 'description', 'path', 'duration', 'difficulty', 'platform']

class UserPathProgressSerializer(serializers.ModelSerializer):
    """Serializer for user progress on a learning path."""
    class Meta:
        model = UserPathProgress
        fields = ['user', 'path', 'progress', 'last_updated']

    def validate_progress(self, value):
        """Ensure progress is between 0 and 100."""
        if value < 0 or value > 100:
            raise serializers.ValidationError("Progress must be between 0 and 100.")
        return value