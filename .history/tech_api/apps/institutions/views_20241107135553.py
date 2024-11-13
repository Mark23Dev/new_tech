from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Institution, Scholarship, ScholarshipApplication
from .serializers import InstitutionSerializer, ScholarshipSerializer, ScholarshipApplicationSerializer


class InstitutionListView(generics.ListAPIView):
    """API endpoint to list all partner institutions."""
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated]


class InstitutionDetailView(generics.RetrieveAPIView):
    """API endpoint to fetch details of a specific institution."""
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated]


class RecommendedScholarshipsView(generics.ListAPIView):
    """API endpoint to get recommended scholarships based on user’s financial needs and profile."""
    serializer_class = ScholarshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Logic for recommending scholarships based on user profile
        user = self.request.user
        # For demonstration, we'll return all scholarships. Replace with real logic.
        return Scholarship.objects.filter(financial_needs__isnull=False)


class ScholarshipApplicationView(generics.CreateAPIView):
    """API endpoint for applying for a specific scholarship."""
    serializer_class = ScholarshipApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        scholarship_id = self.request.data.get('scholarship_id')
        scholarship = get_object_or_404(Scholarship, id=scholarship_id)
        serializer.save(user=self.request.user, scholarship=scholarship)


class ScholarshipApplicationStatusView(generics.ListAPIView):
    """API endpoint to check the application status for a scholarship."""
    serializer_class = ScholarshipApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch application status for the current user's applications
        return ScholarshipApplication.objects.filter(user=self.request.user)
