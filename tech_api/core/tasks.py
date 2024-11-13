# core/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import UserActivityLog

@shared_task
def send_notification_email(subject, message, recipient_list):
    """
    Sends a notification email to the specified recipients.
    """
    send_mail(
        subject,
        message,
        'noreply@yourdomain.com',  # Use your domain email
        recipient_list,
        fail_silently=False,
    )

@shared_task
def log_user_activity(user_id, event, description):
    """
    Logs user activity in the database.
    """
    from .models import UserActivityLog
    activity_log = UserActivityLog.objects.create(
        user_id=user_id,
        event=event,
        description=description,
        timestamp=timezone.now()
    )
    return activity_log.id

@shared_task
def clear_old_activity_logs(days=30):
    """
    Clears user activity logs older than the specified number of days.
    """
    expiration_date = timezone.now() - timedelta(days=days)
    UserActivityLog.objects.filter(timestamp__lt=expiration_date).delete()

# Example usage
# In your views or wherever needed, you can call these tasks asynchronously.
# send_notification_email.delay('Subject', 'Email body', ['user@example.com'])
# log_user_activity.delay(user_id, 'Event Name', 'Description of the event')
# clear_old_activity_logs.delay(days=30)
