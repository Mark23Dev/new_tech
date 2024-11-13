from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import LearningPath, UserProgress, Technology
from django.contrib.auth import get_user_model

User = get_user_model()

class LearningPathTests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create a learning path
        self.learning_path = LearningPath.objects.create(
            title='Data Science',
            description='Learn Data Science from scratch.',
            difficulty='Intermediate',
            duration=30,
            self_paced=True
        )

        # Create technologies
        self.tech = Technology.objects.create(name='Python', description='Programming Language')

    def test_get_learning_paths(self):
        """Test retrieving all learning paths."""
        response = self.client.get(reverse('learningpath-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_learning_path_detail(self):
        """Test retrieving a specific learning path."""
        response = self.client.get(reverse('learningpath-detail', args=[self.learning_path.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.learning_path.title)

    def test_create_learning_path(self):
        """Test creating a new learning path."""
        data = {
            'title': 'Web Development',
            'description': 'Learn how to build websites.',
            'difficulty': 'Beginner',
            'duration': 25,
            'self_paced': True,
        }
        response = self.client.post(reverse('learningpath-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LearningPath.objects.count(), 2)

    def test_update_learning_path(self):
        """Test updating an existing learning path."""
        data = {
            'title': 'Data Science Advanced',
            'description': 'Advanced topics in Data Science.',
        }
        response = self.client.put(reverse('learningpath-detail', args=[self.learning_path.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.learning_path.refresh_from_db()
        self.assertEqual(self.learning_path.title, 'Data Science Advanced')

    def test_delete_learning_path(self):
        """Test deleting a learning path."""
        response = self.client.delete(reverse('learningpath-detail', args=[self.learning_path.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(LearningPath.objects.count(), 0)

    def test_user_progress(self):
        """Test submitting user progress for a learning path."""
        progress_data = {
            'user': self.user.id,
            'path': self.learning_path.id,
            'progress': 50,
        }
        response = self.client.post(reverse('userprogress-list'), progress_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProgress.objects.count(), 1)

    def test_technology_list(self):
        """Test listing technologies associated with learning paths."""
        response = self.client.get(reverse('technology-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_generate_learning_path(self):
        """Test generating a learning path via the API."""
        generate_data = {
            'goal': 'Become a Data Scientist',
            'technologies': ['Python', 'Machine Learning'],
        }
        response = self.client.post(reverse('generate-learning-path'), generate_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_self_paced_recommendation(self):
        """Test getting self-paced course recommendations."""
        recommendation_data = {
            'path_id': self.learning_path.id,
            'pace': 'fast',
        }
        response = self.client.get(reverse('self-paced-recommendation'), recommendation_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

