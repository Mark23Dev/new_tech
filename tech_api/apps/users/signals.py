from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from .models import User, Profile
from .tasks import send_welcome_email

# Signal to create or update a profile when a User instance is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile for the new user
        Profile.objects.create(user=instance)
        # Send a welcome email (optional)
        send_welcome_email(instance)
    else:
        # Update the user's profile if the user is updated
        instance.profile.save()

# Signal to delete associated profile when a User instance is deleted
@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    # Delete the user's profile when the user is deleted
    if instance.profile:
        instance.profile.delete()

# Helper function to send a welcome email
def send_welcome_email(user):
    subject = "Welcome to Tech API!"
    message = f"Hello {user.username},\n\nThank you for registering at Tech API. We're excited to have you!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
