from celery import shared_task
from .models import ScholarshipApplication
from django.utils import timezone
from datetime import timedelta

@shared_task
def check_application_status(application_id):
    """Check the status of a scholarship application and notify the user if necessary."""
    try:
        application = ScholarshipApplication.objects.get(id=application_id)
        # Example logic to check if the application is overdue.
        if application.status == 'Pending' and application.created_at < timezone.now() - timedelta(days=30):
            # Logic to notify the user (e.g., send an email)
            notify_user(application.user, application)
    except ScholarshipApplication.DoesNotExist:
        # Handle the case where the application does not exist
        print(f"ScholarshipApplication with id {application_id} does not exist.")

def notify_user(user, application):
    """Notify the user about their scholarship application status."""
    # Implement your notification logic here (e.g., sending an email)
    print(f"Notification sent to {user.email} about application {application.id} status.")
