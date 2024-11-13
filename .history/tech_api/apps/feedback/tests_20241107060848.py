from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Feedback, Testimonial
from django.contrib.auth import get_user_model

User = get_user_model()

class FeedbackTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.feedback_url = reverse('submit_feedback')
        self.add_testimonial_url = reverse('add_testimonial')
        self.list_testimonials_url = reverse('list_testimonials')

    def test_submit_feedback(self):
        data = {
            'message': 'This is a test feedback.',
            'rating': 5
        }
        response = self.client.post(self.feedback_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(Feedback.objects.get().message, 'This is a test feedback.')

    def test_add_testimonial(self):
        data = {
            'user': self.user.id,
            'content': 'This is a testimonial.'
        }
        response = self.client.post(self.add_testimonial_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Testimonial.objects.count(), 1)
        self.assertEqual(Testimonial.objects.get().content, 'This is a testimonial.')

    def test_list_testimonials(self):
        Testimonial.objects.create(user=self.user, content='First testimonial.')
        Testimonial.objects.create(user=self.user, content='Second testimonial.')
        
        response = self.client.get(self.list_testimonials_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

