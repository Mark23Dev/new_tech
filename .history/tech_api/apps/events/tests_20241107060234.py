from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Event, EventAttendee
from django.contrib.auth import get_user_model

User = get_user_model()

class EventAPITests(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Create an event
        self.event = Event.objects.create(
            title='Test Event',
            description='A test event description.',
            date='2024-11-05T10:00:00Z',
            location='Test Location',
            organizer=self.user
        )
        self.client.login(username='testuser', password='testpass')

    def test_event_list(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure we have one event

    def test_event_detail(self):
        url = reverse('event-detail', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')

    def test_register_event(self):
        url = reverse('event-register', args=[self.event.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventAttendee.objects.count(), 1)  # Ensure attendee is created

    def test_user_event_history(self):
        # Register the user for the event
        self.event.attendees.create(user=self.user)

        url = reverse('user-event-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure we get one event in history

    def test_event_activity_log(self):
        # Create an event attendee to log the action
        self.event.attendees.create(user=self.user)

        url = reverse('event-activity-log', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # No admin rights yet

        # Add admin permission for the user
        self.user.is_staff = True
        self.user.save()
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
