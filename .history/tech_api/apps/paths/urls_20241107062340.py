from django.urls import path
from .views import (
    PathRecommendationsView,
    GenerateLearningPathView,
    PathDetailView,
    UpdateProgressView,
    TechnologiesListView,
    SelfPacedRecommendationsView
)

urlpatterns = [
    path('recommendations/', PathRecommendationsView.as_view(), name='path-recommendations'),
    path('generate/', GenerateLearningPathView.as_view(), name='generate-learning-path'),
    path('detail/<int:pk>/', PathDetailView.as_view(), name='path-detail'),
    path('update-progress/', UpdateProgressView.as_view(), name='update-progress'),
    path('technologies/', TechnologiesListView.as_view(), name='technologies-list'),
    path('self-paced-recommend/', SelfPacedRecommendationsView.as_view(), name='self-paced-recommend')
]
