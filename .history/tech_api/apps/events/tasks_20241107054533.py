from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import Event
from .services import get_upcoming_events
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_event_reminder(event_id):
    """
    Sends a reminder email for a specific event.
    """
    try:
        event = Event.objects.get(id=event_id)
        subject = f"Reminder: Upcoming Event - {event.name}"
        message = f"Hello,\n\nThis is a reminder that the event '{event.name}' is scheduled to start at {event.start_time}.\n\nBest regards,\nThe Events Team"
        recipient_list = [event.created_by.email]
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Reminder sent for event '{event.name}' to {event.created_by.email}"
    except Event.DoesNotExist:
        return f"Event with ID {event_id} does not exist."

@shared_task
def send_reminders_for_upcoming_events():
    """
    Sends reminders for all events starting within the next hour.
    """
    upcoming_events = get_upcoming_events()
    now = timezone.now()
    soon = now + timedelta(hours=1)
    
    for event in upcoming_events:
        if now <= event.start_time <= soon:
            send_event_reminder.delay(event.id)

@shared_task
def delete_past_events():
    """
    Deletes events that have ended in the past.
    """
    now = timezone.now()
    past_events = Event.objects.filter(end_time__lt=now)
    count = past_events.count()
    past_events.delete()
    return f"Deleted {count} past events."
