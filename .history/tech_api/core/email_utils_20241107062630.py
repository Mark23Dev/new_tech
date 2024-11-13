# core/email_utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user_email, user_name):
    """
    Sends a welcome email to the new user.
    
    Args:
        user_email (str): The email address of the user.
        user_name (str): The name of the user.
    """
    subject = 'Welcome to Our STEM Platform!'
    message = f'Hi {user_name},\n\nThank you for joining our STEM community! We are excited to have you.\n\nBest regards,\nThe STEM Team'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)

def send_password_reset_email(user_email, reset_link):
    """
    Sends a password reset email to the user.
    
    Args:
        user_email (str): The email address of the user.
        reset_link (str): The link to reset the user's password.
    """
    subject = 'Password Reset Request'
    message = f'Hi,\n\nYou requested to reset your password. Click the link below to reset it:\n{reset_link}\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nThe STEM Team'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)

def send_feedback_notification_email(admin_email, feedback_content):
    """
    Sends an email notification to the admin regarding new feedback.
    
    Args:
        admin_email (str): The email address of the admin.
        feedback_content (str): The content of the feedback.
    """
    subject = 'New Feedback Received'
    message = f'You have received new feedback:\n\n{feedback_content}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [admin_email]

    send_mail(subject, message, email_from, recipient_list)

# Example usage:
# send_welcome_email('user@example.com', 'John Doe')
