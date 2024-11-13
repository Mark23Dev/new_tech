from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from .models import Institution, Scholarship, ScholarshipApplication
from .serializers import InstitutionSerializer, ScholarshipSerializer, ScholarshipApplicationSerializer


class InstitutionListView(generics.ListAPIView):
    """
    API endpoint to list all partner institutions.
    Only accessible to authenticated users.
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Override to handle custom response or additional logic if needed.
        """
        return super().get(request, *args, **kwargs)


class InstitutionDetailView(generics.RetrieveAPIView):
    """
    API endpoint to fetch details of a specific institution.
    Only accessible to authenticated users.
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Override to handle the case when institution is not found.
        """
        obj = get_object_or_404(self.queryset, pk=self.kwargs["pk"])
        return obj


class RecommendedScholarshipsView(generics.ListAPIView):
    """
    API endpoint to get recommended scholarships based on user's financial needs and profile.
    Only accessible to authenticated users.
    """
    serializer_class = ScholarshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter scholarships based on user's financial needs or profile.
        For now, it returns scholarships with financial needs defined.
        Replace with custom logic.
        """
        user = self.request.user
        scholarships = Scholarship.objects.all()

        # Placeholder logic: Return scholarships with financial needs defined.
        recommended_scholarships = scholarships.filter(financial_needs__isnull=False)

        if not recommended_scholarships:
            raise NotFound(detail="No recommended scholarships found based on your profile.")

        return recommended_scholarships


class ScholarshipApplicationView(generics.CreateAPIView):
    """
    API endpoint for applying for a specific scholarship.
    Only accessible to authenticated users.
    """
    serializer_class = ScholarshipApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override to associate the current user and scholarship on creation.
        """
        scholarship_id = self.request.data.get('scholarship_id')
        if not scholarship_id:
            raise NotFound(detail="Scholarship ID is required.")

        scholarship = get_object_or_404(Scholarship, id=scholarship_id)
        serializer.save(user=self.request.user, scholarship=scholarship)

    def post(self, request, *args, **kwargs):
        """
        Handle scholarship application creation and provide custom response.
        """
        return super().post(request, *args, **kwargs)


class ApplicationStatusView(generics.ListAPIView):
    """
    API endpoint to check the application status for a scholarship.
    Only accessible to authenticated users.
    """
    serializer_class = ScholarshipApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Fetch the application status for the current user's scholarship applications.
        """
        user = self.request.user
        applications = ScholarshipApplication.objects.filter(user=user)

        if not applications:
            raise NotFound(detail="No applications found for this user.")

        return applications

    def list(self, request, *args, **kwargs):
        """
        Override the list method to handle custom response logic, if needed.
        """
        return super().list(request, *args, **kwargs)
