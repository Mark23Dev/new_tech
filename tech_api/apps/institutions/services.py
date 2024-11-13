from .models import Institution, ScholarshipApplication
from django.shortcuts import get_object_or_404
from django.db.models import Q

class InstitutionService:
    @staticmethod
    def get_all_institutions():
        """Fetch all partner institutions."""
        return Institution.objects.all()

    @staticmethod
    def get_institution_details(institution_id):
        """Fetch details of a specific institution."""
        return get_object_or_404(Institution, id=institution_id)

    @staticmethod
    def get_partnered_institutions():
        """Fetch all partnered institutions offering scholarships."""
        return Institution.objects.filter(partnered=True)

class ScholarshipService:
    @staticmethod
    def recommend_scholarships(user_profile):
        """Recommend scholarships based on user's financial needs and profile."""
        # Example logic for scholarship recommendation based on user profile.
        # This would likely involve filtering scholarships based on user attributes.
        recommended_scholarships = Scholarship.objects.filter(
            Q(financial_needs__lte=user_profile.financial_needs) & 
            Q(eligibility_criteria__contains=user_profile.eligibility)
        )
        return recommended_scholarships

    @staticmethod
    def apply_for_scholarship(user, scholarship_id):
        """Apply for a specific scholarship."""
        scholarship = get_object_or_404(Scholarship, id=scholarship_id)
        application, created = ScholarshipApplication.objects.get_or_create(
            user=user,
            scholarship=scholarship
        )
        return application

    @staticmethod
    def check_application_status(application_id):
        """Check the application status for a scholarship."""
        return get_object_or_404(ScholarshipApplication, id=application_id)
