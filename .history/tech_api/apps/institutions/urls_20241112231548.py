from django.urls import path
from apps.institutions.views import (
    InstitutionListView,
    InstitutionDetailView,
    RecommendedScholarshipsView,
    ScholarshipApplicationView,
    ApplicationStatusView,
)

urlpatterns = [
    path('institutions/', InstitutionListView.as_view(), name='institution-list'),
    path('institutions/<int:pk>/', InstitutionDetailView.as_view(), name='institution-detail'),
    path('scholarships/recommended/', RecommendedScholarshipsView.as_view(), name='recommended-scholarships'),
    path('scholarships/apply/', ScholarshipApplicationView.as_view(), name='scholarship-application'),
    path('scholarships/application-status/', ApplicationStatusView.as_view(), name='application-status'),
]
