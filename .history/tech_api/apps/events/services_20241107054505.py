from datetime import datetime
from .models import Event
from django.utils import timezone

def create_event(name, description, start_time, end_time, created_by):
    """
    Creates a new event.
    """
    event = Event(
        name=name,
        description=description,
        start_time=start_time,
        end_time=end_time,
        created_by=created_by,
    )
    event.save()
    return event

def get_upcoming_events():
    """
    Retrieves upcoming events that haven't started yet.
    """
    now = timezone.now()
    return Event.objects.filter(start_time__gte=now).order_by('start_time')

def update_event(event_id, **kwargs):
    """
    Updates an existing event with the given parameters.
    """
    try:
        event = Event.objects.get(id=event_id)
        for key, value in kwargs.items():
            setattr(event, key, value)
        event.save()
        return event
    except Event.DoesNotExist:
        return None

def delete_event(event_id):
    """
    Deletes an event by its ID.
    """
    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        return True
    except Event.DoesNotExist:
        return False

def get_event_by_id(event_id):
    """
    Retrieves a single event by its ID.
    """
    try:
        return Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return None
