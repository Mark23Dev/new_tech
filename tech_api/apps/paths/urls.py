from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LearningPathViewSet,
    PathRecommendationsView,
    GenerateLearningPathView,
    UpdateProgressView,
    TechnologiesListView,
    SelfPacedRecommendationsView,
)

router = DefaultRouter()
router.register(r'learning-paths', LearningPathViewSet, basename='learning-paths')

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/', PathRecommendationsView.as_view(), name='path-recommendations'),
    path('generate/', GenerateLearningPathView.as_view(), name='generate-learning-path'),
    path('update-progress/', UpdateProgressView.as_view(), name='update-progress'),
    path('technologies/', TechnologiesListView.as_view(), name='technologies-list'),
    path('self-paced-recommend/', SelfPacedRecommendationsView.as_view(), name='self-paced-recommend'),
]
