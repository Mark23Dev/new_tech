# apps/events/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event

@receiver(post_save, sender=Event)
def my_handler(sender, instance, created, **kwargs):
    if created:
        print(f'New event created: {instance}')
