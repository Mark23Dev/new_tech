from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import SomeModel  # Import any models you need to work with

@shared_task
def send_notification_email(user_email, subject, message):
    """
    Send an email notification to a user.
    """
    send_mail(
        subject,
        message,
        'admin@example.com',  # Replace with your sender email address
        [user_email],
        fail_silently=False,
    )
    print(f"Notification email sent to {user_email}")

@shared_task
def update_data():
    """
    Periodically update some data in the database.
    """
    # Sample logic to update records
    records = SomeModel.objects.filter(status='pending')
    for record in records:
        record.status = 'processed'
        record.updated_at = timezone.now()
        record.save()
    print(f"Updated {records.count()} records")

@shared_task
def generate_report(user_email):
    """
    Generate a report and send it to the user.
    """
    # Logic to generate a report
    report_data = "This is a sample report."
    
    # Send report via email
    send_mail(
        "Your Report",
        report_data,
        'admin@example.com',
        [user_email],
        fail_silently=False,
    )
    print(f"Report sent to {user_email}")
