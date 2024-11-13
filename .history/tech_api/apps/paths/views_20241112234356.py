from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
import requests
from .models import LearningPath, UserPathProgress, Technology, RecommendedCourse
from .serializers import (
    LearningPathSerializer, 
    UserPathProgressSerializer, 
    TechnologySerializer, 
    RecommendedCourseSerializer
)

class LearningPathViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for Learning Paths.
    """
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]


class PathRecommendationsView(generics.ListAPIView):
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        interests = self.request.query_params.getlist('interests')
        skill_level = self.request.query_params.get('skill_level', None)

        queryset = LearningPath.objects.all()

        if interests:
            queryset = queryset.filter(technologies__name__in=interests)
        if skill_level:
            queryset = queryset.filter(difficulty=skill_level)

        return queryset


class GenerateLearningPathView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        goal = request.data.get('goal')
        technologies = request.data.get('technologies', [])
        duration = request.data.get('duration', None)

        try:
            response = requests.post('https://api.gemma.com/generate-path', data={
                'goal': goal,
                'technologies': technologies,
                'duration': duration
            })

            if response.status_code == 200:
                generated_path_data = response.json()
                return Response(generated_path_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Error generating learning path"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProgressView(APIView):
    permission_classes = [IsAuthenticated]

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

class TechnologyViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for Technologies.
    """
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

class TechnologiesListView(generics.ListAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [IsAuthenticated]


class SelfPacedRecommendationsView(generics.ListAPIView):
    serializer_class = RecommendedCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        path_id = self.request.query_params.get('path_id')
        path = get_object_or_404(LearningPath, id=path_id)
        return RecommendedCourse.objects.filter(path=path)

