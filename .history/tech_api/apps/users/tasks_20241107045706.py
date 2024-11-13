from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, username):
    """
    Asynchronously send a welcome email to the user upon registration.
    
    Args:
    - user_email: The email address of the user.
    - username: The username of the user.
    """
    subject = "Welcome to Tech API!"
    message = f"Hello {username},\n\nThank you for registering at Tech API. We're excited to have you!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_password_reset_email(user_email, reset_link):
    """
    Asynchronously send a password reset email to the user.
    
    Args:
    - user_email: The email address of the user.
    - reset_link: The link for resetting the password.
    """
    subject = "Password Reset Requested"
    message = f"Please click the link below to reset your password:\n\n{reset_link}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
