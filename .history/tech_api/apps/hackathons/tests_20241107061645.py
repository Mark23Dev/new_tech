from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Challenge, Submission, LeaderboardEntry
from django.contrib.auth import get_user_model

User = get_user_model()

class ChallengeAPITests(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a challenge
        self.challenge = Challenge.objects.create(
            title='Sample Challenge',
            description='A test challenge',
            start_date='2024-01-01',
            end_date='2024-01-10'
        )

    def test_upcoming_challenges(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('upcoming_challenges'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the created challenge is listed

    def test_challenge_detail(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('challenge_detail', args=[self.challenge.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.challenge.title)

    def test_submit_challenge(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('submit_challenge'), data={'challenge_id': self.challenge.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Submission.objects.count(), 1)  # Check if a submission was created

    def test_leaderboard(self):
        # Create a leaderboard entry
        LeaderboardEntry.objects.create(user=self.user, challenge=self.challenge, score=100)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('challenge_leaderboard', args=[self.challenge.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the leaderboard entry is listed
