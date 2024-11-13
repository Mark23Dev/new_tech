from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import LearningPath, UserPathProgress, Technology, RecommendedCourse
from .serializers import (
    LearningPathSerializer, 
    UserPathProgressSerializer, 
    TechnologySerializer, 
    RecommendedCourseSerializer
)

class PathRecommendationsView(generics.ListAPIView):
    """
    API endpoint to get personalized learning path recommendations based on the user's profile and preferences.
    """
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Placeholder for recommendation logic based on user profile and preferences
        # For example, filter by user interests or skills
        return LearningPath.objects.all()

class GenerateLearningPathView(APIView):
    """
    API endpoint to generate a learning path using the Gemma/Gemini API.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Logic to connect with the Gemma/Gemini API to generate a learning path
        # For now, this just returns a placeholder response
        generated_path_data = {
            'title': 'AI and Machine Learning Path',
            'description': 'A custom path generated to learn AI and ML.',
            'is_self_paced': True
        }
        return Response(generated_path_data, status=status.HTTP_201_CREATED)

class PathDetailView(generics.RetrieveAPIView):
    """
    API endpoint to fetch details of a specific learning path.
    """
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]

class UpdateProgressView(APIView):
    """
    API endpoint to update user progress for a specific path.
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        path_id = request.data.get('path_id')
        progress = request.data.get('progress')
        
        path = get_object_or_404(LearningPath, id=path_id)
        user_progress, created = UserPathProgress.objects.get_or_create(user=request.user, path=path)
        
        user_progress.progress = progress
        user_progress.last_updated = timezone.now()
        user_progress.save()

        serializer = UserPathProgressSerializer(user_progress)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TechnologiesListView(generics.ListAPIView):
    """
    API endpoint to list technologies associated with specific learning paths.
    """
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [permissions.IsAuthenticated]

class SelfPacedRecommendationsView(generics.ListAPIView):
    """
    API endpoint to recommend self-paced courses and timelines for a selected path.
    """
    serializer_class = RecommendedCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        path_id = self.request.query_params.get('path_id')
        path = get_object_or_404(LearningPath, id=path_id)
        return RecommendedCourse.objects.filter(path=path)
