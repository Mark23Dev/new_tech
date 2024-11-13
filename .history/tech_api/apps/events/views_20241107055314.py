from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, EventAttendee, UserActivityLog
from .serializers import EventSerializer, EventAttendeeSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404

class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        attendee, created = EventAttendee.objects.get_or_create(user=request.user, event=event)
        
        # Log the registration
        UserActivityLog.objects.create(
            user=request.user,
            event=event,
            action="Registered",
            timestamp=timezone.now()
        )

        serializer = EventAttendeeSerializer(attendee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserEventHistoryView(generics.ListAPIView):
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventAttendee.objects.filter(user=self.request.user)

class EventActivityLogView(generics.ListAPIView):
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return UserActivityLog.objects.filter(event_id=event_id)
    
    class EventCalendarView(generics.ListAPIView):
    queryset = Event.objects.all()  # You can modify this to filter events for the calendar view
    serializer_class = EventSerializer

