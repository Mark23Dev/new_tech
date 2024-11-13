from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        """Test user registration."""
        response = self.client.post(reverse('user_register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # One existing user plus the new one
        self.assertEqual(User.objects.last().username, 'newuser')

    def test_user_login(self):
        """Test user login."""
        response = self.client.post(reverse('user_login'), {
            'username': self.user.username,
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Assuming you return a token on successful login

    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials."""
        response = self.client.post(reverse('user_login'), {
            'username': self.user.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_retrieval(self):
        """Test user profile retrieval."""
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.get(reverse('user_profile'))  # Assuming you have a profile endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_user_profile_update(self):
        """Test user profile update."""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('user_profile'), {
            'email': 'updateduser@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_user_deletion(self):
        """Test user deletion."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('user_delete'))  # Assuming you have a delete endpoint
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username=self.user.username).exists())

