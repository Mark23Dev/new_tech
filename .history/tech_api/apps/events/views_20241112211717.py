from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Event, EventAttendee, UserActivityLog
from .serializers import EventSerializer, EventAttendeeSerializer, UserParticipationSerializer, UserActivityLogSerializer

# List and Create Events
class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # You can add additional logic before saving the event
        serializer.save(created_by=self.request.user)

# Retrieve, Update, and Delete an Event
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Add logic for updating if necessary
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        # Handle deletion logic, logging, etc. before deleting the event
        instance.deleted_by = self.request.user
        instance.deleted_at = timezone.now()
        instance.save()
        instance.delete()

# Register User for an Event
class RegisterEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        # Get the event or return 404
        event = get_object_or_404(Event, id=event_id)

        # Register the user for the event (create EventAttendee record)
        attendee, created = EventAttendee.objects.get_or_create(user=request.user, event=event)

        # Log the registration action
        UserActivityLog.objects.create(
            user=request.user,
            event=event,
            action="Registered",
            timestamp=timezone.now()
        )

        # Serialize and return the attendee data
        serializer = EventAttendeeSerializer(attendee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# View User's Event Participation History
class UserEventHistoryView(generics.ListAPIView):
    serializer_class = UserParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return all events the user has participated in
        return EventAttendee.objects.filter(user=self.request.user)

# View Activity Log for a Specific Event
class EventActivityLogView(generics.ListAPIView):
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        # Get the event_id from URL and filter the logs related to that event
        event_id = self.kwargs['event_id']
        return UserActivityLog.objects.filter(event_id=event_id)

# View to display the event calendar (list of events formatted for a calendar)
class CalendarView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Format the events to be displayed on a calendar
        # Example: Return upcoming events within the next 30 days
        return Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')

# View to list and create EventAttendee records for an event (view all attendees)
class EventAttendeeView(generics.ListCreateAPIView):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Additional logic if needed when a user registers for an event
        serializer.save()

# Event ViewSet for CRUD operations (if you prefer using ViewSets)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Add any custom logic for saving an event
        serializer.save(created_by=self.request.user)

class EventAttendeeViewSet(viewsets.ModelViewSet):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Additional logic for attendee creation
        serializer.save()

class UserActivityLogViewSet(viewsets.ModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAdminUser]

