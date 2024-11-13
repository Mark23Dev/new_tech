from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Institution, Scholarship, ScholarshipApplication
from django.contrib.auth import get_user_model

User = get_user_model()

class InstitutionsAPITests(APITestCase):
    
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create sample institutions and scholarships
        self.institution1 = Institution.objects.create(name='Institution One', description='First Institution', location='City A')
        self.institution2 = Institution.objects.create(name='Institution Two', description='Second Institution', location='City B')

        self.scholarship1 = Scholarship.objects.create(
            title='Scholarship One',
            description='Description for Scholarship One',
            institution=self.institution1,
            financial_needs=True
        )
        self.scholarship2 = Scholarship.objects.create(
            title='Scholarship Two',
            description='Description for Scholarship Two',
            institution=self.institution2,
            financial_needs=False
        )
    
    def test_list_institutions(self):
        """Test the endpoint to list all institutions."""
        url = reverse('institution-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Expecting two institutions

    def test_institution_detail(self):
        """Test the endpoint to get details of a specific institution."""
        url = reverse('institution-detail', args=[self.institution1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.institution1.name)

    def test_recommend_scholarships(self):
        """Test the endpoint to get recommended scholarships."""
        url = reverse('scholarship-recommend')
        response = self.client.get(url, {'financial_needs': True})  # Assuming financial needs parameter is needed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.scholarship1.title, [scholarship['title'] for scholarship in response.data])

    def test_apply_scholarship(self):
        """Test the endpoint to apply for a specific scholarship."""
        url = reverse('scholarship-apply')
        response = self.client.post(url, {'scholarship_id': self.scholarship1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ScholarshipApplication.objects.count(), 1)

    def test_application_status(self):
        """Test the endpoint to check application status for a scholarship."""
        # Create an application to test the status check
        application = ScholarshipApplication.objects.create(user=self.user, scholarship=self.scholarship1, status='submitted')
        url = reverse('application-status')
        response = self.client.get(url, {'scholarship_id': self.scholarship1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'submitted')

    def test_list_partners(self):
        """Test the endpoint to list all partnered institutions offering scholarships."""
        url = reverse('partnered-institutions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Adjust based on your partnerships
