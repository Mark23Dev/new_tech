from django.urls import path
from .views import (
    InstitutionListView,
    InstitutionDetailView,
    RecommendedScholarshipsView,
    ScholarshipApplicationView,
    ApplicationStatusView,
    PartneredInstitutionsView,
)

urlpatterns = [
    path('all/', InstitutionListView.as_view(), name='institution-list'),
    path('<int:institution_id>/', InstitutionDetailView.as_view(), name='institution-detail'),
    path('scholarships/recommend/', RecommendedScholarshipsView.as_view(), name='scholarship-recommend'),
    path('scholarships/apply/', ScholarshipApplicationView.as_view(), name='scholarship-apply'),
    path('scholarships/status/', ApplicationStatusView.as_view(), name='application-status'),
    path('partners/', PartneredInstitutionsView.as_view(), name='partnered-institutions'),
]
