from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
import logging

# Set up logging for the signal actions
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def log_user_activity(sender, instance, created, **kwargs):
    if created:
        logger.info(f'New user created: {instance.username} at {timezone.now()}')
    else:
        logger.info(f'User updated: {instance.username} at {timezone.now()}')

@receiver(pre_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    logger.info(f'User deleted: {instance.username} at {timezone.now()}')
