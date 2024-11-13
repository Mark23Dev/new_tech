from rest_framework import serializers
from .models import Event, EventAttendee, UserActivityLog

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'location', 'created_at', 'updated_at']

class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendee
        fields = ['id', 'user', 'event', 'registered_at']

    def create(self, validated_data):
        # You can add custom behavior here if necessary
        return super().create(validated_data)


class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'event', 'action', 'timestamp']
